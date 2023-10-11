import utils
import torch
import numpy as np


def test_tensor_bank():
    # [torch.Tensor, torch.Tensor] -> torch.Tensor
    cnt = 5
    tmp = []
    for i in range(cnt):
        tmp.append(torch.rand(5, 10, device='cuda'))
    
    tensor_bank = utils.Bank(type_=torch.Tensor, device='cuda')
    for i in range(cnt):
        tensor_bank.append(tmp[i])
    
    assert tensor_bank.concat().shape == (25, 10)
    assert str(tensor_bank.device) == 'cuda'

    # [[torch.Tensor, torch.Tensor], ..., [torch.Tensor, torch.Tensor]] -> 
    # [torch.Tensor, torch.Tensor]
    tmp = []
    for _ in range(cnt):
        view = []
        for _ in range(cnt):
            view.append(torch.rand(5, 10, device='cpu'))
        tmp.append(view)
    
    tensor_bank = utils.Bank(it_num=cnt, type_=torch.Tensor, device='cpu')
    for i in range(len(tmp)):
        tensor_bank.append(tmp[i])

    tensor_list = tensor_bank.concat()
    assert len(tensor_list) == cnt
    for i in range(cnt):
        assert str(tensor_list[i].device) == 'cpu'
        assert tensor_list[i].shape == (25, 10)


def test_ndarray_bank():
    # [np.ndarray, np.ndarray] -> np.ndarray
    cnt = 5
    tmp = []
    for i in range(cnt):
        tmp.append(np.random.rand(10, 10))
    
    arr_bank = utils.Bank()
    for i in range(cnt):
        arr_bank.append(tmp[i])
    
    assert arr_bank.concat().shape == (50, 10)

    # [[np.ndarray, np.ndarray], ..., [np.ndarray, np.ndarray]] -> 
    # [np.ndarray, np.ndarray]
    tmp = []
    for _ in range(cnt):
        view = []
        for _ in range(cnt):
            view.append(np.random.rand(10, 10))
        tmp.append(view)
    
    arr_bank = utils.Bank(it_num=cnt)
    for i in range(len(tmp)):
        arr_bank.append(tmp[i])

    arr_list = arr_bank.concat()
    assert len(arr_list) == cnt
    for i in range(cnt):
        assert arr_list[i].shape == (50, 10)

