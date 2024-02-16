from typing import List

from imgaug import augmenters as iaa

from projects_src.augmentation_gui.function_model import IFunctionFactory
from projects_src.augmentation_gui.parameter_models.constraints import Constraints
from projects_src.augmentation_gui.parameter_models.number_parameter import NumberParameter
from projects_src.augmentation_gui.parameter_models.parameter_interface import Parameter
from projects_src.augmentation_gui.parameter_models.tuple_parameter import StringDescription, TupleParameter


class PerspectiveTransform(IFunctionFactory):

    def __init__(self, parent=None):
        super().__init__(parent)

    def _init_name(self) -> str:
        return "Perspective Transform"

    def _init_parameters(self) -> List[Parameter]:
        scale = TupleParameter('scale',
                               'scale',
                               (StringDescription('from'),
                                NumberParameter('scale', 'scale', 0, Constraints(0, 1, 0.01, float)), StringDescription('to'), NumberParameter('scale', 'scale', 0.06, Constraints(0, 1, 0.01, float))))
        return [scale]

    def _init_function(self) -> callable:
        return iaa.PerspectiveTransform

    def _init_sub_functions_param(self) -> str:
        return ""
