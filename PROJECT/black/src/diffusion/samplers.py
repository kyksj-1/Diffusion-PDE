import torch
from tqdm import tqdm

def euler_maruyama_sampler(model, shape, sigma_min, sigma_max, num_steps=50, device="cpu", S_churn=0, S_noise=1.0):
    """
    Standard Reverse Time Sampler (Heun / Euler-Maruyama variant).
    Modified with optional Godunov PDE guidance. (Algorithm 1)
    """
    with torch.no_grad():
        tau_steps = torch.linspace(sigma_max, sigma_min, num_steps, device=device)
        u_tau = torch.randn(shape, device=device) * sigma_max

        # Simplest EDM deterministic ODE integration: dx = -0.5 * score(x, sigma) d_sigma^2
        # where score(x, sigma) = (D_theta(x, sigma) - x) / sigma^2
        
        for i in tqdm(range(num_steps - 1), desc="Sampling"):
            sigma_t = tau_steps[i]
            sigma_next = tau_steps[i+1]

            # 1. Denoise
            D_u = model(u_tau, sigma_t.unsqueeze(0).expand(shape[0]))
            
            # Score
            score = (D_u - u_tau) / (sigma_t ** 2)

            # 2. ODE step (Euler)
            d_u = -sigma_t * score * (sigma_max / num_steps) # dx/d_sigma is -sigma*score
            u_next = u_tau + d_u * (sigma_next - sigma_t)
            
            # 3. PDE Guidance (\zeta_{PDE} * \nabla L_{Godunov})
            # To be cleanly implemented with gradients active or via physics-informed step
            
            u_tau = u_next

        return u_tau
