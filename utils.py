import torch
from torch import nn
import os
import argparse
import numpy as np
import random
import json
import json
from typing import List


def get_parser():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--seed', type=int, default=42, help="random seed")

    # train related
    parser.add_argument('--epochs', type=int, default=30, help='# of epoch')
    parser.add_argument('--base_epoch', default=0, type=int, help='start epoch number, used for ckp')
    parser.add_argument('--batch_size', type=int, default=1024, help='# samples in batch')
    parser.add_argument('--test_ratio', type=int, default=0.2, help='# samples in batch')
    parser.add_argument('--device', type=str, default='cuda:2', help='cpu, mps, cuda:0, cuda:x')
    parser.add_argument('--use_pretrained_emb', type=bool, default=False, help='')

    # optimizer ralated
    parser.add_argument('--lr', type=float, default=0.1, help='initial learning rate for adam')
    parser.add_argument('--weight_decay', type=float, default=1e-4, help='checkpoint path')
    parser.add_argument('--use_sched_ckp', type=bool, default=False, help='if use the checkpoint of scheduler')

    # path related
    parser.add_argument('--data_path', type=str, default='./data/feature/', help='data path')
    parser.add_argument('--dict_prop_file', type=str, default='./data/dict_prop.json')
    parser.add_argument('--ckp_path', type=str, default=None, help='checkpoint path')
    parser.add_argument('--out_ckp_path', type=str, default='./ckps/demo', help='checkpoint path')
    parser.add_argument('--log_dir', type=str, default='./log/demo', help='checkpoint path')
    
    return parser.parse_args()


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
    info = f'[info] loaded from {path_dir}, for model'
    model.load_state_dict(torch.load(os.path.join(path_dir, 'model.pth')))

    if opt is not None:
        opt.load_state_dict(torch.load(os.path.join(path_dir, 'opt.pth')))
        info += ', for opt'
    if sched is not None:
        sched.load_state_dict(torch.load(os.path.join(path_dir, 'sched.pth')))
        info += ', for sched'

    with open(os.path.join(path_dir, 'config.json'), 'r') as f:
        config = json.load(f)
    print(info)
    return config


def setup_seed(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    random.seed(seed)
    torch.backends.cudnn.deterministic = True


def tensor_to_device(tensor_x, device):
    def _list_to_device(tensor_x: List[torch.Tensor], device):
        for i in range(len(tensor_x)):
            tensor_x[i] = tensor_x[i].to(device)

    def _dict_to_device(fea_dict: dict, device):
        for k, v in fea_dict.items():
            if isinstance(v, torch.Tensor):
                fea_dict[k] = v.to(device)
    
    if isinstance(tensor_x, list):
        _list_to_device(tensor_x, device)
    elif isinstance(tensor_x, dict):
        _dict_to_device(tensor_x, device)
    elif isinstance(tensor_x, torch.Tensor):
        return tensor_x.to(device)
    else:
        raise ValueError(f"unsupported type {type(tensor_x)}")    
    return tensor_x
