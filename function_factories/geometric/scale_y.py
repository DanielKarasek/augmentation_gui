from typing import List

from imgaug import augmenters as iaa

from projects_src.augmentation_gui.function_model import IFunctionFactory
from projects_src.augmentation_gui.parameter_models.constraints import Constraints
from projects_src.augmentation_gui.parameter_models.number_parameter import NumberParameter
from projects_src.augmentation_gui.parameter_models.parameter_interface import Parameter
from projects_src.augmentation_gui.parameter_models.tuple_parameter import StringDescription, TupleParameter


class ScaleY(IFunctionFactory):

    def __init__(self, parent=None):
        super().__init__(parent)

    def _init_name(self) -> str:
        return "Scale Y"

    def _init_parameters(self) -> List[Parameter]:
        scale = TupleParameter('scale', 'scale', (StringDescription('from'), NumberParameter('scale', 'scale', 0.5, Constraints(0, 5, 0.01, float)), StringDescription('to'), NumberParameter('scale', 'scale', 1.5, Constraints(0, 5, 0.01, float))))
        return [scale]

    def _init_function(self) -> callable:
        return iaa.ScaleY

    def _init_sub_functions_param(self) -> str:
        return ""
