
"""
Defines the neural network, losses function and metrics
"""

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from utils import Params
from torchvision import models


class Net(nn.Module):
    """
    Some information about this module...
    """

    def __init__(self, params):
        """
        Args:
            params (Params): contains num_channels
        """
        super(Net, self).__init__()
        self.backbone = models.AlexNet()
        self.backbone.classifier[-1] = nn.Linear(4096, 10)
        self.backbone.features[0] = nn.Conv2d(1, 64, kernel_size=(11, 11), stride=(4, 4), padding=(2, 2))

    def forward(self, s):
        """
        This function defines how we use the components of our network to operate on an input batch.

        Args:
            s (torch.Tensor): contains a batch of data, of dimension batch_size x 3 x 64 x 64 .
        Returns:
            out (torch.Tensor): dimension (, ), means that

        Note: the dimensions after each step are provided
        """

        # log softmax is numerically more stable than softmax.
        return self.backbone.forward(s)


def loss_fn(outputs, labels) -> torch.Tensor:
    """
    Here, write the dimension of the input.

    Args:
        outputs (torch.Tensor): dimension (batch_size x 6 - output of the model)
        labels (torch.Tensor): dimension (batch_size,) where each element is a value in [0, 1, 2, ..., L]

    Returns:
        loss (torch.Tensor): cross entropy loss for all images in the batch

    Note:
    """
    num_examples = outputs.size()[0]
    return -torch.sum(outputs[range(num_examples), labels])/num_examples


def accuracy(outputs, labels) -> float:
    """
    Compute the accuracy, given the outputs and labels for all images.

    Args:
        outputs (np.ndarray): dimension (batch_size,)
        labels (np.ndarray): dimension (batch_size,) where each element is a value in [0, 1, 2, ..., L]

    Returns (float): accuracy in [0,1]
    """
    outputs = np.argmax(outputs, axis=1)
    return np.sum(outputs == labels) / float(labels.size)


# maintain all metrics required in this dictionary- these are used in the training and evaluation loops
metrics = {
    'accuracy': accuracy,
    # could add more metrics such as accuracy for each token type
}
