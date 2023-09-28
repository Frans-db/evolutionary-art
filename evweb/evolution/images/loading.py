from PIL import Image
from torch import Tensor
from torchvision.transforms import ToTensor


def load_image(path: str) -> Tensor:
    image = Image.open(path)
    image = ToTensor()(image)

    return image
