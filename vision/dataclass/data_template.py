import numpy as np
import torch
from torch.utils.data import Dataset


class Mnist(Dataset):
    def __init__(self, data_dir, mode: str = 'train', transform=None):
        if mode == 'train':
            self.data = None
        elif mode == 'val':
            self.data = None
        elif mode == 'test':
            self.data = None
        else:
            raise Exception("unknown mode.")

    def __len__(self):
        return None

    def __getitem__(self, item):
        return None, None
