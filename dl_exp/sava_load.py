import os
import torch
from torch import nn
import os
import json


def save_torch_model(model_state, opt_state, sched_state, path_dir, cfg: dict):
    """
    Args:
        model_state: could not be None
        opt_state: could not be None
        sched_state: None or not.
        path_dir: directory of ckp path. format `expflag_epoch-{base_epoch}-{cur_epoch}`
            is recommended.
    """
    os.makedirs(path_dir, exist_ok=True)

    torch.save(model_state, os.path.join(path_dir, 'model.pth'))
    torch.save(opt_state, os.path.join(path_dir, 'opt.pth'))
    if sched_state is not None:
        torch.save(sched_state, os.path.join(path_dir, 'sched.pth'))
    
    with open(os.path.join(path_dir, 'config.json'), 'w') as f:
        json.dump(cfg, f)

    print(f'saved model in {path_dir}')


def load_torch_model(model: nn.Module, opt, sched, path_dir) -> dict:
    """load state and return checkpoint config"""
    model.load_state_dict(torch.load(os.path.join(path_dir, 'model.pth')))
    if opt is not None:
        opt.load_state_dict(torch.load(os.path.join(path_dir, 'opt.pth')))
    if sched is not None:
        sched.load_state_dict(torch.load(os.path.join(path_dir, 'sched.pth')))

    with open(os.path.join(path_dir, 'config.json'), 'r') as f:
        config = json.load(f)
    print(f'loaded from {path_dir}')
    return config