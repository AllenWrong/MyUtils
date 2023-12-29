import os
import torch
from torch import nn
import os


def save_torch_model(model_state, opt_state, sched_state, path_dir):
    os.makedirs(path_dir, exist_ok=True)

    torch.save(model_state, os.path.join(path_dir, 'model.pth'))
    torch.save(opt_state, os.path.join(path_dir, 'opt.pth'))
    if sched_state is not None:
        torch.save(sched_state, os.path.join(path_dir, 'sched.pth'))
    print(f'saved model in {path_dir}')


def load_torch_model(model: nn.Module, opt, sched, path_dir):
    model.load_state_dict(torch.load(os.path.join(path_dir, 'model.pth')))
    if opt is not None:
        opt.load_state_dict(torch.load(os.path.join(path_dir, 'opt.pth')))
    if sched is not None:
        sched.load_state_dict(torch.load(os.path.join(path_dir, 'sched.pth')))

    print(f'loaded from {path_dir}')