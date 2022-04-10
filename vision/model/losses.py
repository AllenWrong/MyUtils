import torch
from torch import nn
import torch.nn.functional as F
from .whitening import Whitening2d
import math
from .layers import SinkhornDistance


def norm_mse_loss(x0, x1):
    """
    Args:
        x0 (torch.Tensor): shape is (batch_size, latent_dim)
        x1 (torch.Tensor): shape is (batch_size, latent_dim)
    """
    x0 = F.normalize(x0)
    x1 = F.normalize(x1)
    return 2 - 2 * (x0 * x1).sum(dim=-1).mean()


def euclidean_dist(x0, x1):
    """
    Args:
        x0 (torch.Tensor): shape is (batch_size, latent_dim)
        x1 (torch.Tensor): shape is (batch_size, latent_dim)
    """
    return torch.sqrt(torch.sum((x0 - x1)**2, dim=1)).mean()

