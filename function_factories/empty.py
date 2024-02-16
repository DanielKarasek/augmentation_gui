from typing import List

from imgaug import augmenters as iaa

from function_model import IFunctionFactory
from parameter_models.parameter_interface import Parameter


class Empty(IFunctionFactory):

    def __init__(self, parent=None):
        super().__init__(parent)

    def _init_name(self) -> str:
        return "Empty"

    def _init_parameters(self) -> List[Parameter]:
        return []

    def _init_function(self) -> callable:
        return iaa.Noop

    def _init_sub_functions_param(self) -> str:
        return ""
