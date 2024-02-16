from typing import List

from imgaug import augmenters as iaa

from projects_src.augmentation_gui.function_model import IFunctionFactory
from projects_src.augmentation_gui.parameter_models.constraints import Constraints
from projects_src.augmentation_gui.parameter_models.number_parameter import NumberParameter
from projects_src.augmentation_gui.parameter_models.parameter_interface import Parameter


class SomeOf(IFunctionFactory):

    def __init__(self, parent=None):
        super().__init__(parent)

    def _init_name(self) -> str:
        return "Some Of"

    def _init_parameters(self) -> List[Parameter]:
        number_of_children = NumberParameter("Number of children", "number_of_children", 1, Constraints(1, 50, 1, int))
        return [number_of_children]

    def _init_function(self) -> callable:
        return iaa.SomeOf

    def _init_sub_functions_param(self) -> str:
        return "children"
