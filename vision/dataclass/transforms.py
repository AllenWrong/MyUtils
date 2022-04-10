import numpy as np
from torchvision import transforms


base_transform = transforms.Compose([
    transforms.ToTensor()
])


def normalize(x: np.ndarray):
    """Min-Max Normalization"""
    x = (x - np.min(x)) / (np.max(x) - np.min(x))
    return x


def random_crop(output_size):
    return transforms.RandomResizedCrop(output_size)


def random_color_distortion(s=1.0):
    color_jitter = transforms.ColorJitter(0.8*s, 0.8*s, 0.8*s, 0.2*s)
    rnd_color_jitter = transforms.RandomApply([color_jitter], p=0.8)
    rnd_gray = transforms.RandomGrayscale(p=0.2)
    return transforms.Compose([
        rnd_color_jitter,
        rnd_gray
    ])


def simclr_data_aug(output_size, s=1.0):
    """Standard data augmentation from SimCLR
    Args:
        output_size: same as the input size.
        s:
    """
    return transforms.Compose([
        random_crop(output_size),
        random_color_distortion(s),
        transforms.ToTensor()
    ])


class MultiTransform:
    def __init__(self, num_trans, output_size):
        """Construct multi transfrom to generate multi data augmentaion version
        Args:
            num_trans: number of transform
            output_size: the size of transfromed image
        """
        self.transforms = [simclr_data_aug(output_size) for i in range(num_trans)]
        self.num_trans = num_trans

    def __call__(self, x):
        return [self.transforms[i](x) for i in range(self.num_trans)]
