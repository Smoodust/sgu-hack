from torch.utils.data import TensorDataset, DataLoader
import torch

w = torch.rand((10, 10)) * 2 - 1


def get_train_dataloader():
    x = torch.rand((40, 10)) * 2 - 1
    y = x @ w + torch.rand((40, 10)) / 10
    train_dataset = TensorDataset(x, y)
    return DataLoader(train_dataset, batch_size=8, shuffle=True)


def get_test_dataloader():
    x = torch.rand((40, 10)) * 2 - 1
    y = x @ w + torch.rand((40, 10)) / 10
    train_dataset = TensorDataset(x, y)
    return DataLoader(train_dataset, batch_size=8, shuffle=True)
