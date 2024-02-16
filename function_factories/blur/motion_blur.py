from typing import List

from imgaug import augmenters as iaa

from projects_src.augmentation_gui.function_model import IFunctionFactory
from projects_src.augmentation_gui.parameter_models.constraints import Constraints
from projects_src.augmentation_gui.parameter_models.number_parameter import NumberParameter
from projects_src.augmentation_gui.parameter_models.parameter_interface import Parameter
from projects_src.augmentation_gui.parameter_models.tuple_parameter import StringDescription, TupleParameter


class MotionBlur(IFunctionFactory):

    def __init__(self, parent=None):
        super().__init__(parent)

    def _init_name(self) -> str:
        return "Motion Blur"

    def _init_parameters(self) -> List[Parameter]:
        k = TupleParameter('Kernel size', 'k', (StringDescription('from'), NumberParameter('k', 'k', 1, Constraints(1, 10000, 1, int)), StringDescription('to'), NumberParameter('k', 'k', 7, Constraints(1, 10000, 1, int))))
        angle = TupleParameter('angle', 'angle', (StringDescription('from'), NumberParameter('angle', 'angle', 0, Constraints(0, 360, 0.01, float)), StringDescription('to'), NumberParameter('angle', 'angle', 90, Constraints(0, 360, 0.01, float))))
        constraint_direction = Constraints(-1.0, 1.0, 0.01, float)
        direction = NumberParameter('direction', 'direction', -0.0, constraint_direction)
        return [k, angle, direction]

    def _init_function(self) -> callable:
        return iaa.MotionBlur

    def _init_sub_functions_param(self) -> str:
        return ""
