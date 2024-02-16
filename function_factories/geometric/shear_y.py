from typing import List

from imgaug import augmenters as iaa

from projects_src.augmentation_gui.function_model import IFunctionFactory
from projects_src.augmentation_gui.parameter_models.constraints import Constraints
from projects_src.augmentation_gui.parameter_models.number_parameter import NumberParameter
from projects_src.augmentation_gui.parameter_models.parameter_interface import Parameter
from projects_src.augmentation_gui.parameter_models.tuple_parameter import StringDescription, TupleParameter


class ShearY(IFunctionFactory):

    def __init__(self, parent=None):
        super().__init__(parent)

    def _init_name(self) -> str:
        return "Shear Y"

    def _init_parameters(self) -> List[Parameter]:
        shear = TupleParameter('shear', 'shear', (StringDescription('from'), NumberParameter('shear', 'shear', -90, Constraints(-360, 360, 0.01, float)), StringDescription('to'), NumberParameter('shear', 'shear', 90, Constraints(-360, 360, 0.01, float))))
        return [shear]

    def _init_function(self) -> callable:
        return iaa.ShearY

    def _init_sub_functions_param(self) -> str:
        return ""
