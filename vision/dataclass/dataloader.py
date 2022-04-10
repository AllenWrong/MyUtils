from transforms import base_transform
from data_template import Mnist


def fetch_dataloader(args, types, params):
    """
    Fetches the DataLoader object for each type in types from data_dir.

    Args:
        args:
        types (list): has one or more of 'train', 'val', 'test' depending on which data is required
        params (Params): hyperparameters
    Returns:
        data: (dict) contains the DataLoader object for each type in types
    """
    dataloaders = {}

    for split in ['train', 'val', 'test']:
        if split in types:
            if args.data == "mnist":
                dataclass = Mnist
            else:
                raise Exception("Unknown data name.")

            # use the train_transformer if training data, else use eval_transformer without random flip
            if split == 'train':
                dl = DataLoader(
                    dataclass(path, mode=split, train_transformer),
                    batch_size=params.batch_size,
                    shuffle=True,
                    num_workers=params.num_workers,
                    pin_memory=params.cuda
                )
            else:
                dl = DataLoader(
                    dataclass(path, mode=split, eval_transformer),
                    batch_size=params.batch_size,
                    shuffle=False,
                    num_workers=params.num_workers,
                    pin_memory=params.cuda
                )

            dataloaders[split] = dl

    return dataloaders
