from typing import List

from imgaug import augmenters as iaa

from projects_src.augmentation_gui.function_model import IFunctionFactory
from projects_src.augmentation_gui.parameter_models.constraints import Constraints
from projects_src.augmentation_gui.parameter_models.number_parameter import NumberParameter
from projects_src.augmentation_gui.parameter_models.parameter_interface import Parameter


class ContrastNormalization(IFunctionFactory):

    def __init__(self, parent=None):
        super().__init__(parent)

    def _init_name(self) -> str:
        return "Contrast Normalization"

    def _init_parameters(self) -> List[Parameter]:
        constraint_alpha = Constraints(0, 20, 0.01, float)
        alpha = NumberParameter('alpha', 'alpha', 0, constraint_alpha)
        constraint_per_channel = Constraints(0, 1, 0.01, float)
        per_channel = NumberParameter('Per channel', 'per_channel', 0, constraint_per_channel)
        return [alpha, per_channel]

    def _init_function(self) -> callable:
        return iaa.ContrastNormalization

    def _init_sub_functions_param(self) -> str:
        return ""
