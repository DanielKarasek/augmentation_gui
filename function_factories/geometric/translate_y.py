from typing import List

from imgaug import augmenters as iaa

from projects_src.augmentation_gui.function_model import IFunctionFactory
from projects_src.augmentation_gui.parameter_models.constraints import Constraints
from projects_src.augmentation_gui.parameter_models.number_parameter import NumberParameter
from projects_src.augmentation_gui.parameter_models.parameter_interface import Parameter
from projects_src.augmentation_gui.parameter_models.tuple_parameter import StringDescription, TupleParameter


class TranslateY(IFunctionFactory):

    def __init__(self, parent=None):
        super().__init__(parent)

    def _init_name(self) -> str:
        return "Translate Y"

    def _init_parameters(self) -> List[Parameter]:
        percent = TupleParameter('percent', 'percent', (StringDescription('from'), NumberParameter('percent', 'percent', -0.1, Constraints(-1, 1, 0.01, float)), StringDescription('to'), NumberParameter('percent', 'percent', 0.1, Constraints(-1, 1, 0.01, float))))
        return [percent]

    def _init_function(self) -> callable:
        return iaa.TranslateY

    def _init_sub_functions_param(self) -> str:
        return ""
