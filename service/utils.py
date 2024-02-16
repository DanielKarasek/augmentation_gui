from __future__ import annotations

import json
import os

import imgaug
import numpy as np

from ai_core.data_structure.coordinates.keypoint_general import KeypointGeneral
from projects_src.augmentation_gui.function_model_tree import TreeModel
from projects_src.augmentation_gui.service.exceptions import PipelineFileError


def load_pipeline(path: str):
    # TODO: Find out valid exceptions during my pipeline loading
    if not os.path.exists(path):
        raise PipelineFileError(f"File {path} doesn't exist")
    try:
        with open(path, "r") as f:
            model_dict = json.load(f)
            tree_model = TreeModel()
            tree_model.from_dict(model_dict["data"])
            pipeline = tree_model.build_callable_pipeline()
    except Exception as e:
        raise PipelineFileError(f"Error while loading pipeline: {e}")
    return pipeline


def keypoints2imgaug(kps: list[KeypointGeneral], shape: tuple[int, ...]) -> imgaug.KeypointsOnImage:
    return imgaug.KeypointsOnImage([imgaug.Keypoint(x=kp.center_point.x, y=kp.center_point.y) for kp in kps],
                                   shape=shape)


def dtype2int(dtype: np.dtype) -> int:
    dtype_dict = {
        np.uint8: 0,
        np.uint16: 1,
        np.float16: 2,
        np.float32: 3,
        np.float64: 4,
    }
    return dtype_dict[dtype.type]


def int2dtype_and_type_size(dtype: int) -> tuple[np.dtype, int]:
    dtype_dict = {
        0: (np.uint8, 1),
        1: (np.uint16, 2),
        2: (np.float16, 2),
        3: (np.float32, 4),
        4: (np.float64, 8),
    }
    return dtype_dict[dtype]
