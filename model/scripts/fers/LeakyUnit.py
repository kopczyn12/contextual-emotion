"""
@INPROCEEDINGS{Zhao2020,
    author={R. {Zhao} and T. S. {Liu} and J. {Xiao} and D. P. K. {Lun} and K. {Lam}},
    booktitle={International Conference on Pattern Recognition (ICPR)},
    title={Deep Multi-task Learning For Facial Expression Recognition and Synthesis based on Selective Feature Sharing},
    year={2020}}

Leaky Unit definition from paper: https://arxiv.org/pdf/2007.04514.pdf
Most of the code comes from the FERSNet github repository
"""
import torch
import torch.nn as nn
import torch.nn.functional as F

KERNEL_SIZE: int = 1
PADDING: int = 0


class LeakyUnit(nn.Module):
    """ Leaky Unit used in the FERS network, inspired by the GRU unit. This unit is responsible
    for the selective feature sharing described in the paper """
    def __init__(self, n_features):
        """
        Constructor of the LeakyUnit
        :param n_features: Number of input features (emotions to be recognized and synthesized)
        """
        super(LeakyUnit, self).__init__()
        self.W_r = nn.Conv2d(2*n_features, n_features, kernel_size=KERNEL_SIZE, padding=PADDING, stride=1, bias=False)
        self.W = nn.Conv2d(n_features, n_features, kernel_size=KERNEL_SIZE, padding=PADDING, stride=1, bias=False)
        self.U = nn.Conv2d(n_features, n_features, kernel_size=KERNEL_SIZE, padding=PADDING, stride=1, bias=False)
        self.W_z = nn.Conv2d(2*n_features, n_features, kernel_size=KERNEL_SIZE, padding=PADDING, stride=1, bias=False)
        self.sigma = nn.Sigmoid()

    def forward(self, f_m, f_n):
        """
        Forward pass of the leaky unit
        :param f_m: First input of the leaky unit
        :param f_n: Second input of the leaky unit
        :return: Transformed input values
        """
        f_mn = torch.cat((f_m, f_n), dim=1)
        r_mn = self.sigma(self.W_r(f_mn))
        f_mn_hat = torch.tanh(self.U(f_m) + self.W(r_mn.expand_as(f_n) * f_n))
        z_mn = self.sigma(self.W_z(f_mn))
        f_m_out = z_mn.expand_as(f_m) * f_m + (1 - z_mn.expand_as(f_mn_hat)) * f_mn_hat

        return f_m_out, r_mn, z_mn
