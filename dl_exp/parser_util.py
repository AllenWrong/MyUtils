import argparse
import torch
import random
import numpy as np


def get_parser():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--seed', type=int, default=42, help="random seed")

    # train related
    parser.add_argument('--epochs', type=int, default=30, help='# of epoch')
    parser.add_argument('--base_epoch', default=0, type=int, help='start epoch number, used for ckp')
    parser.add_argument('--batch_size', type=int, default=2058, help='# samples in batch')
    parser.add_argument('--device', type=str, default='cpu', help='cpu, mps, cuda:0, cuda:x')

    # optimizer ralated
    parser.add_argument('--lr', type=float, default=0.1, help='initial learning rate for adam')
    parser.add_argument('--weight_decay', type=float, default=1e-4, help='checkpoint path')

    # path related
    parser.add_argument('--user_data_path', type=str, default=None, help='checkpoint path')
    parser.add_argument('--item_data_path', type=str, default=None, help='checkpoint path')
    parser.add_argument('--ckp_path', type=str, default=None, help='checkpoint path')
    parser.add_argument('--out_ckp_path', type=str, default=None, help='checkpoint path')
    parser.add_argument('--log_dir', type=str, default='./log/demo', help='checkpoint path')
    
    return parser.parse_args()


def setup_seed(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    random.seed(seed)
    torch.backends.cudnn.deterministic = True