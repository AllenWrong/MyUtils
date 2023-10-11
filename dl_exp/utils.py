import pickle
import numpy as np
from sklearn.manifold import TSNE
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Union
import os
import torch


def atleast_epsilon(X, eps=1e-8):
    """Ensure that all elements are >= `eps`.
    src: https://github.com/DanielTrosten/mvc/blob/main/src/lib/loss.py

    Args:
        X (torch.Tensor): input tensor
        eps (float, optional): min value. Defaults to 1e-8.

    Returns:
        torch.Tensor: New version of X where elements smaller 
        than `eps` have been replaced with `eps`.
    """
    return torch.where(X < eps, X.new_tensor(eps), X)


def write_list(obj: list, file: str) -> None:
    """Write a list object to file

    Args:
        obj (list): need to write
        file (str): file path
    """
    print('write list to', file)
    with open(file, 'wb') as f:
        pickle.dump(obj, f)


def load_list(file: str) -> list:
    """load a list from file

    Args:
        file (str): file path

    Returns:
        list: loaded list
    """
    print('load list from', file)
    with open(file, 'rb') as f:
        return pickle.load(f)
    

def list_tensor_to(device, tensors: List[torch.Tensor]) -> None:
    """move the tensor is a list to deivce

    Args:
        device (str):
        tensors (List[torch.Tensor]): list of tensor
    """
    for i in range(len(tensors)):
        tensors[i] = tensors[i].to(device)
    

def concat_nest_list(nest_list: List[List[np.ndarray]], axis=0) -> List[np.ndarray]:
    """concate the element of a list

    Args:
        nest_list (List[List[np.ndarray]]): list need to be concated
        axis (int, optional): . Defaults to 0.

    Returns:
        List[np.ndarray]: a list of np.ndarray
    """
    for i in range(len(nest_list)):
        nest_list[i] = np.concatenate(nest_list[i], axis=axis)
    return nest_list


def plot(data: np.ndarray, label: np.ndarray, save_img_path: str) -> None:
    """plot scatter figure. generally for feature embedding visualization.

    Args:
        data (np.ndarray): shape (n, d)
        label (np.ndarray): shape (n, 1)
        save_img_path (str): save the figure to this path
    """
    tsne = TSNE(n_components=2) 
    X_tsne = tsne.fit_transform(data) 
    X_tsne_data = np.vstack((X_tsne.T, label)).T 
    df_tsne = pd.DataFrame(X_tsne_data, columns=['Dim1', 'Dim2', 'class'])
    
    plt.figure(figsize=(8, 8)) 
    plt.scatter(c=df_tsne['class'], x=df_tsne['Dim1'], y=df_tsne['Dim2']) 
    plt.savefig(save_img_path)
    plt.show()


def plot_mv_emb(
    mv_emb: List[np.ndarray], label: np.ndarray, save_img_root: str,
    save_img_prefix: str = None
) -> None:
    """plot a list feature embedding.

    Args:
        mv_emb (List[np.ndarray]): feature embedding list.
        label (np.ndarray): shape (n, 1)
        save_img_root (str): parent directory if the result figure.
        save_img_prefix (str, optional): prefix of result figure 
            filenames. Defaults to None.
    """
    for i in range(len(mv_emb)):
        prefix = "view" if save_img_prefix is None else save_img_prefix
        save_path = os.path.join(save_img_root, f"{prefix}_{i}.png")
        plot(mv_emb[i], label, save_path)


class Bank:
    """A data bank. When you want to collect the output or data of each batch, you
    will need this class. Finaly, by call `concat`you can get the concated result.
    """
    def __init__(self, it_num: int = 0, type_=np.ndarray, device=None) -> None:
        """

        Args:
            it_num (int, optional): number of element in this bank. Defaults to 0.
            type_ (_type_, optional): only supported np.ndarray or torch.Tensor. Defaults to np.ndarray.
            device (_type_, optional): torch.Tensor will use this argument. Defaults to None.
        """
        self.it_num = it_num
        self.bank_type = type_
        if self.bank_type is torch.Tensor:
            assert device is not None, "You must set the device, when using tensor bank."
            self.device = device

        self.bank = [[] for _ in range(it_num)]

    def _to_bank_type(self, it: Union[np.ndarray, torch.Tensor]) -> Union[np.ndarray, torch.Tensor]:
        """convert the element to the type this bank supported.

        Args:
            it (Union[np.ndarray, torch.Tensor]): element data

        Raises:
            ValueError: it is not np.ndarray or torch.Tensor.

        Returns:
            Union[np.ndarray, torch.Tensor]: element have the consistent bank type
            with bank.
        """
        if isinstance(it, self.bank_type):
            if self.bank_type is torch.Tensor:
                it = it.to(self.device)
            return it
        
        if self.bank_type is np.ndarray:
            return it.detach().cpu().numpy()
        
        if self.bank_type is torch.Tensor:
            return torch.tensor(it, device=self.device)
        
        raise ValueError(f"unsupported type {type(it)}, \
                         supported type is {self.bank_type}")

    def _append(self, idx: int, it: Union[np.ndarray, torch.Tensor]) -> None:
        """append an element to bank. this will be call when the bank
        is a nest list.

        Args:
            idx (int): index of inner list.
            it (Union[np.ndarray, torch.Tensor]): element.
        """
        self.bank[idx].append(self._to_bank_type(it))

    def append(self, it):
        if isinstance(it, self.bank_type):
            assert self.it_num == 0
            self.bank.append(it)
        
        elif isinstance(it, list):
            assert len(it) == len(self.bank)
            for i in range(len(it)):
                self._append(i, it[i])
        else:
            self.bank.append(self._to_bank_type(it))
        
    def concat(self, axis=0):
        if self.it_num == 0:
            if self.bank_type is np.ndarray:
                return np.concatenate(self.bank, axis=axis)
            else:
                return torch.concat(self.bank, axis=axis)
        else:
            if self.bank_type is np.ndarray:
                for i in range(len(self.bank)):
                    self.bank[i] = np.concatenate(self.bank[i], axis=axis)
                return self.bank
            else:
                for i in range(len(self.bank)):
                    self.bank[i] = torch.concat(self.bank[i], dim=axis)
                return self.bank
    
    def save(self, save_path: str):
        write_list(self.bank, save_path)
