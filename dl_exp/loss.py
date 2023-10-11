from torch.nn import CrossEntropyLoss
import torch.nn.functional as F
import torch
from torch import nn
import kernel


def log_softmax(sim_z, sim_ema):
    return -torch.sum(F.log_softmax(sim_z, dim=-1) * sim_ema, dim=1).mean()


def soft_contrastive_loss(zs, ema_zs, tau=1.0, soft=False):
    loss = 0.0
    fn = CrossEntropyLoss()
    for v in range(len(zs)):
        for u in range(v+1, len(zs)):
            a = F.normalize(zs[v], dim=-1)
            b = F.normalize(zs[u], dim=-1)
            sim_z = (a @ b.T) / tau
            if soft:
                sim_ema = (F.normalize(ema_zs[v], dim=-1) @ F.normalize(ema_zs[u], dim=-1).T) / 10
                loss += log_softmax(sim_z, sim_ema)
            else:
                loss += fn.forward(sim_z, torch.arange(0, sim_z.shape[0], device=sim_z.device))
    loss /= (len(zs) * (len(zs) - 1))
    return loss



class DDCLoss(nn.Module):
    """Adopted from https://github.com/Gasteinh/DSMVC/blob/main/loss.py"""

    def __init__(self, batch_size: int, class_num: int, device: str):
        """Devergence Based Loss

        Args:
            batch_size (int):
            class_num (int):
            device (str): 'cpu' or 'cuda' or 'cuda:x'
        """
        super(DDCLoss, self).__init__()
        self.batch_size = batch_size
        self.class_num = class_num
        self.device = device
        self.eps = 1e-9

    def forward_cluster(self, hidden, output, print_sign=False):
        hidden_kernel = kernel.vector_kernel(hidden, rel_sigma=0.15)
        l1 = self.DDC1(output, hidden_kernel, self.class_num)
        l2 = self.DDC2(output)
        l3 = self.DDC3(self.class_num, output, hidden_kernel)
        if print_sign:
            print(l1.item())
            print(l2.item())
            print(l3.item())
        return l1+l2+l3, l1.item() + l2.item() + l3.item()

    def triu(self, X):
        # Sum of strictly upper triangular part
        return torch.sum(torch.triu(X, diagonal=1))

    def _atleast_epsilon(self, X, eps):
        return torch.where(X < eps, X.new_tensor(eps), X)

    def d_cs(self, A, K, n_clusters):
        """Cauchy-Schwarz divergence."""

        nom = torch.t(A) @ K @ A
        dnom_squared = torch.unsqueeze(torch.diagonal(nom), -1) @ torch.unsqueeze(torch.diagonal(nom), 0)

        nom = self._atleast_epsilon(nom, self.eps)
        dnom_squared = self._atleast_epsilon(dnom_squared, eps=self.eps ** 2)

        d = 2 / (n_clusters * (n_clusters - 1)) * self.triu(nom / torch.sqrt(dnom_squared))
        return d

    def DDC1(self, output, hidden_kernel, n_clusters):
        """L_1 loss from DDC"""
        return self.d_cs(output, hidden_kernel, n_clusters)

    def DDC2(self, output):
        """L_2 loss from DDC"""
        n = output.size(0)
        return 2 / (n * (n - 1)) * self.triu(output @ torch.t(output))

    def DDC2Flipped(self, output, n_clusters):
        """Flipped version of the L_2 loss from DDC. Used by EAMC"""
        return 2 / (n_clusters * (n_clusters - 1)) * self.triu(torch.t(output) @ output)

    def DDC3(self, n_clusters, output, hidden_kernel):
        """L_3 loss from DDC"""
        eye = torch.eye(n_clusters, device=self.device)

        m = torch.exp(-kernel.cdist(output, eye))
        return self.d_cs(m, hidden_kernel, n_clusters)
