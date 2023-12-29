import os
import torch
from torch import nn
import os


def save_torch_model(model_state, opt_state, path_dir):
    os.makedirs(path_dir, exist_ok=True)
    model_save_path = os.path.join(path_dir, 'model.pth')
    opt_save_path = os.path.join(path_dir, 'opt.pth')
    torch.save(model_state, model_save_path)
    torch.save(opt_state, opt_save_path)
    print(f'saved model in {path_dir}')


def load_torch_model(model: nn.Module, opt, path_dir):
    model.load_state_dict(torch.load(os.path.join(path_dir, 'model.pth')))
    if opt is not None:
        opt.load_state_dict(torch.load(os.path.join(path_dir, 'opt.pth')))

    print(f'loaded from {path_dir}')