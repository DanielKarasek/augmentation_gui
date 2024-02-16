from typing import List

from imgaug import augmenters as iaa

from projects_src.augmentation_gui.function_model import IFunctionFactory
from projects_src.augmentation_gui.parameter_models.constraints import Constraints
from projects_src.augmentation_gui.parameter_models.number_parameter import NumberParameter
from projects_src.augmentation_gui.parameter_models.parameter_interface import Parameter
from projects_src.augmentation_gui.parameter_models.tuple_parameter import StringDescription, TupleParameter


class Multiply(IFunctionFactory):

    def __init__(self, parent=None):
        super().__init__(parent)

    def _init_name(self) -> str:
        return "Multiply"

    def _init_parameters(self) -> List[Parameter]:
        mul = TupleParameter('Multiply factor sampled per image', 'mul', (StringDescription('from'), NumberParameter('mul', 'mul', 0, Constraints(0, 8, 0.01, float)), StringDescription('to'), NumberParameter('mul', 'mul', 0, Constraints(0, 8, 0.01, float))))
        constraint_per_channel = Constraints(0, 1, 0.01, float)
        per_channel = NumberParameter('Per channel', 'per_channel', 0, constraint_per_channel)
        return [mul, per_channel]

    def _init_function(self) -> callable:
        return iaa.Multiply

    def _init_sub_functions_param(self) -> str:
        return ""
