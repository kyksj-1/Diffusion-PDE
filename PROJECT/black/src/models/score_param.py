import torch
import torch.nn as nn
from src.models.unet_1d import UNet1D

class StandardScore(nn.Module):
    """
    Standard EDM parameterization: D_theta(x, sigma) 
    predicts the denoised x_0, from which score is derived.
    """
    def __init__(self, in_channels=1, sigma_data=0.5):
        super().__init__()
        self.net = UNet1D(in_channels=in_channels, out_channels=in_channels)
        self.sigma_data = sigma_data

    def forward(self, x, sigma):
        """
        EDM preconditions.
        c_skip * x + c_out * F_theta(c_in * x, c_noise(sigma))
        """
        c_skip = self.sigma_data**2 / (sigma**2 + self.sigma_data**2)
        c_out = sigma * self.sigma_data / (sigma**2 + self.sigma_data**2)**0.5
        c_in = 1 / (self.sigma_data**2 + sigma**2)**0.5
        c_noise = sigma.log() / 4.0

        F_x = self.net(c_in[:, None, None] * x, c_noise)
        
        D_x = c_skip[:, None, None] * x + c_out[:, None, None] * F_x
        return D_x

class BVAwareScore(nn.Module):
    """
    BV-aware Score Parameterization for EntroDiff Theory validation.
    Placeholder for future extension (Parameterization C in paper).
    """
    def __init__(self, in_channels=1):
        super().__init__()
        # For the MVP, we just use Standard Score logic here or a simplified version
        self.base = StandardScore(in_channels)
        
    def forward(self, x, sigma):
        # We will add softplus(tanh(...)) logic per paper here in future.
        # For now, it defaults to standard EDM approach.
        return self.base(x, sigma)
