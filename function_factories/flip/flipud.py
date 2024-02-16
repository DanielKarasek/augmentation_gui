from typing import List

from imgaug import augmenters as iaa

from projects_src.augmentation_gui.function_model import IFunctionFactory
from projects_src.augmentation_gui.parameter_models.constraints import Constraints
from projects_src.augmentation_gui.parameter_models.number_parameter import NumberParameter
from projects_src.augmentation_gui.parameter_models.parameter_interface import Parameter


class Flipud(IFunctionFactory):

    def __init__(self, parent=None):
        super().__init__(parent)

    def _init_name(self) -> str:
        return "Flipud"

    def _init_parameters(self) -> List[Parameter]:
        constraint_p = Constraints(0, 1, 0.01, float)
        p = NumberParameter('Probability', 'p', 0.5, constraint_p)
        return [p]

    def _init_function(self) -> callable:
        return iaa.Flipud

    def _init_sub_functions_param(self) -> str:
        return ""
