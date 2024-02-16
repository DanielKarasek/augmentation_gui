import cv2
import numpy as np

from typing import List, Union, Tuple


def letterbox(im: np.ndarray,
              new_shape: Union[List[int], int] = [640, 640],
              colour: Tuple[int, int, int] = [0, 0, 0],
              minimal_padding_flag=False,
              scale_up_flag=False,
              stride=32):
    """
    Resizes image while keeping the aspect ratio and adds padding (letterbox) if necessary.

    :param minimal_padding_flag: Instead of padding to full new_shape size, we pad as little as possible so the
                                 smaller dimension is divisible by stride.
    :param stride: if minimal padding, smaller side of image will be padded to be divisible by this stride
    """
    shape = im.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = [new_shape, new_shape]

    # matching cv2 coordinates
    new_shape = new_shape[::-1]

    # Scale ratio (new / old)
    scale_ratio = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scale_up_flag:  # only scale down, do not scale up (for better val mAP)
        scale_ratio = min(scale_ratio, 1.0)

    # Compute padding
    ratio = scale_ratio, scale_ratio  # width, height ratios
    unpad_shape = int(round(shape[1] * scale_ratio)), int(round(shape[0] * scale_ratio))

    dw, dh = new_shape[1] - unpad_shape[0], new_shape[0] - unpad_shape[1]  # wh padding

    if minimal_padding_flag:  # minimum rectangle
        dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding

    dw /= 2
    dh /= 2

    if shape != unpad_shape[::-1]:  # resize
        im = cv2.resize(im, unpad_shape, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    im = cv2.copyMakeBorder(im,
                            top, bottom,
                            left, right,
                            cv2.BORDER_CONSTANT, value=colour)
    return im
