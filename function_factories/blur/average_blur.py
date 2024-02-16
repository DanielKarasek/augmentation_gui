from typing import List

from imgaug import augmenters as iaa

from projects_src.augmentation_gui.function_model import IFunctionFactory
from projects_src.augmentation_gui.parameter_models.constraints import Constraints
from projects_src.augmentation_gui.parameter_models.number_parameter import NumberParameter
from projects_src.augmentation_gui.parameter_models.parameter_interface import Parameter
from projects_src.augmentation_gui.parameter_models.tuple_parameter import StringDescription, TupleParameter


class AverageBlur(IFunctionFactory):

    def __init__(self, parent=None):
        super().__init__(parent)

    def _init_name(self) -> str:
        return "Average Blur"

    def _init_parameters(self) -> List[Parameter]:
        k = TupleParameter('Square kernel size sampled per image',
                           'k',
                           (StringDescription('from'), NumberParameter('k', 'k', 3, Constraints(1, 10000, 1, int)), StringDescription('to'), NumberParameter('k', 'k', 3, Constraints(1, 10000, 1, int))))
        return [k]

    def _init_function(self) -> callable:
        return iaa.AverageBlur

    def _init_sub_functions_param(self) -> str:
        return ""
