from typing import List

from imgaug import augmenters as iaa

from projects_src.augmentation_gui.function_model import IFunctionFactory
from projects_src.augmentation_gui.parameter_models.parameter_interface import Parameter


class Sequential(IFunctionFactory):

    def __init__(self, parent=None):
        super().__init__(parent)

    def _init_name(self) -> str:
        return "Sequential"

    def _init_parameters(self) -> List[Parameter]:
        return []

    def _init_function(self) -> callable:
        return iaa.Sequential

    def _init_sub_functions_param(self) -> str:
        return "children"
