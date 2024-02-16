from typing import List

from imgaug import augmenters as iaa

from projects_src.augmentation_gui.function_model import IFunctionFactory
from projects_src.augmentation_gui.parameter_models.constraints import Constraints
from projects_src.augmentation_gui.parameter_models.number_parameter import NumberParameter
from projects_src.augmentation_gui.parameter_models.parameter_interface import Parameter


class CoarseDropout(IFunctionFactory):

    def __init__(self, parent=None):
        super().__init__(parent)

    def _init_name(self) -> str:
        return "Coarse Dropout"

    def _init_parameters(self) -> List[Parameter]:
        constraint_p = Constraints(0, 1, 0.01, float)
        p = NumberParameter('probability', 'p', 0, constraint_p)
        constraint_size_percent = Constraints(0, 1, 0.01, float)
        size_percent = NumberParameter('Dropout size as ratio of image', 'size_percent', 0, constraint_size_percent)
        constraint_per_channel = Constraints(0, 1, 0.01, float)
        per_channel = NumberParameter('Per channel', 'per_channel', 0, constraint_per_channel)
        return [p, size_percent, per_channel]

    def _init_function(self) -> callable:
        return iaa.CoarseDropout

    def _init_sub_functions_param(self) -> str:
        return ""
