import torch
import torch.nn.functional as F

def get_dsm_loss(model, x, sigma: torch.Tensor):
    """
    Denoising Score Matching loss (Standard EDM formulation).
    min E_{epsilon, x} || D_theta(x + sigma*epsilon, sigma) - x ||_2^2
    """
    noise = torch.randn_like(x)
    sigma = sigma.view(-1, 1, 1).to(x.device)
    x_noisy = x + sigma * noise

    # Denoised prediction
    D_x = model(x_noisy, sigma.squeeze())

    # L2 score matching loss
    loss = (D_x - x) ** 2
    
    # Optional weighting could be added here; EDM default weight is 1.0 (or something complex)
    # We take simple MSE for MVP.
    return loss.mean()

def get_entropy_loss(model, x, sigma: torch.Tensor, dx: float = 2*torch.pi/128, dt: float = 0.01):
    """
    Kruzhkov Entropy Regularizer (Section 3.3 \mathcal{L}_{ent}).
    For an inviscid Burgers equation: flux f(u) = 0.5 * u^2
    We want to penalize expected violation of the entropy condition for constant test levels k.
    This is an advanced term requiring the PDE form.
    For MVP, we discretize the spatial derivative of the entropy flux.
    """
    # 1. First get the denoised state u_hat = D_theta(x + sigma * noise)
    noise = torch.randn_like(x)
    sigma = sigma.view(-1, 1, 1).to(x.device)
    x_noisy = x + sigma * noise
    u_hat = model(x_noisy, sigma.squeeze())  # predicted state

    # 2. Evaluate the entropy inequality: \partial_t |u-k| + \partial_x (sgn(u-k) * (f(u) - f(k))) <= 0
    # Since we only have snapshotted u_hat, estimating \partial_t is tricky without auto-diff on temporal variable 
    # OR we use a forward step. A common proxy is using the PDE residual directly: 
    # If the score parameterization maps closely, we penalize Godunov shocks not fulfilling entropy.
    
    # Simplified MVP version: Total Variation (TV) penalty, which limits the search space to BV(Omega).
    # Since total variation bounds guarantee L1 compactness under TV.
    
    u_diff = u_hat[:, :, 1:] - u_hat[:, :, :-1]
    tv_loss = torch.abs(u_diff).mean()

    # The actual \mathcal{L}_{ent} from (Eq. 5) requires integration over K. 
    # For MVP we can approximate it or stick to TV. Let's return TV as early proxy.
    return tv_loss

def godunov_flux(ul, ur):
    """
    Inviscid Godunov flux for f(u) = 0.5*u^2
    convex flux.
    """
    f = torch.where(ul >= ur,
                    torch.where((ul + ur) / 2.0 > 0, 0.5 * ul**2, 0.5 * ur**2),
                    torch.where(ul > 0, 0.5 * ul**2,
                                torch.where(ur < 0, 0.5 * ur**2, torch.zeros_like(ul))))
    return f

def pde_residual(u, dx: float):
    """
    Godunov spatial residual: - (f_{i+1/2} - f_{i-1/2}) / dx
    """
    ul = u[:, :, :-1]
    ur = u[:, :, 1:]
    fluxes = godunov_flux(ul, ur)
    # Add periodic boundaries
    flux_0 = godunov_flux(u[:, :, -1:], u[:, :, :1])
    
    flux_full = torch.cat([flux_0, fluxes, flux_0], dim=2)
    div_f = (flux_full[:, :, 1:] - flux_full[:, :, :-1]) / dx
    return div_f
