from typing import List

from imgaug import augmenters as iaa

from projects_src.augmentation_gui.function_model import IFunctionFactory
from projects_src.augmentation_gui.parameter_models.constraints import Constraints
from projects_src.augmentation_gui.parameter_models.number_parameter import NumberParameter
from projects_src.augmentation_gui.parameter_models.parameter_interface import Parameter
from projects_src.augmentation_gui.parameter_models.tuple_parameter import StringDescription, TupleParameter


class Rotate(IFunctionFactory):

    def __init__(self, parent=None):
        super().__init__(parent)

    def _init_name(self) -> str:
        return "Rotate"

    def _init_parameters(self) -> List[Parameter]:
        rotate = TupleParameter('rotate', 'rotate', (StringDescription('from'), NumberParameter('rotate', 'rotate', -90, Constraints(-360, 360, 0.01, float)), StringDescription('to'), NumberParameter('rotate', 'rotate', 90, Constraints(-360, 360, 0.01, float))))
        return [rotate]

    def _init_function(self) -> callable:
        return iaa.Rotate

    def _init_sub_functions_param(self) -> str:
        return ""
