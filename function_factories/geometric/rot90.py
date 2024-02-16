from typing import List

from imgaug import augmenters as iaa

from projects_src.augmentation_gui.function_model import IFunctionFactory
from projects_src.augmentation_gui.parameter_models.constraints import Constraints
from projects_src.augmentation_gui.parameter_models.number_parameter import NumberParameter
from projects_src.augmentation_gui.parameter_models.parameter_interface import Parameter
from projects_src.augmentation_gui.parameter_models.tuple_parameter import StringDescription, TupleParameter


class Rot90(IFunctionFactory):

    def __init__(self, parent=None):
        super().__init__(parent)

    def _init_name(self) -> str:
        return "Rot90"

    def _init_parameters(self) -> List[Parameter]:
        k = TupleParameter('k', 'k', (StringDescription('from'), NumberParameter('k', 'k', 0, Constraints(0, 3, 1, int)), StringDescription('to'), NumberParameter('k', 'k', 3, Constraints(0, 3, 1, int))))
        return [k]

    def _init_function(self) -> callable:
        return iaa.Rot90

    def _init_sub_functions_param(self) -> str:
        return ""
