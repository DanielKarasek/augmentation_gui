from typing import List

from imgaug import augmenters as iaa

from projects_src.augmentation_gui.function_model import IFunctionFactory
from projects_src.augmentation_gui.parameter_models.constraints import Constraints
from projects_src.augmentation_gui.parameter_models.number_parameter import NumberParameter
from projects_src.augmentation_gui.parameter_models.parameter_interface import Parameter
from projects_src.augmentation_gui.parameter_models.tuple_parameter import StringDescription, TupleParameter


class Affine(IFunctionFactory):

    def __init__(self, parent=None):
        super().__init__(parent)

    def _init_name(self) -> str:
        return "Affine"

    def _init_parameters(self) -> List[Parameter]:
        scale = TupleParameter('scale', 'scale', (StringDescription('from'),
                                                  NumberParameter('scale', 'scale', 0.5, Constraints(0, 5, 0.01, float)), StringDescription('to'), NumberParameter('scale', 'scale', 1.5, Constraints(0, 5, 0.01, float))))
        translate_percent = TupleParameter('translate_percent', 'translate_percent', (StringDescription('from'), NumberParameter('translate_percent', 'translate_percent', -0.1, Constraints(-1, 1, 0.01, float)), StringDescription('to'), NumberParameter('translate_percent', 'translate_percent', 0.1, Constraints(-1, 1, 0.01, float))))
        rotate = TupleParameter('rotate', 'rotate', (StringDescription('from'), NumberParameter('rotate', 'rotate', -360, Constraints(-360, 360, 0.01, float)), StringDescription('to'), NumberParameter('rotate', 'rotate', -360, Constraints(-360, 360, 0.01, float))))
        shear = TupleParameter('shear', 'shear', (StringDescription('from'), NumberParameter('shear', 'shear', -360, Constraints(-360, 360, 0.01, float)), StringDescription('to'), NumberParameter('shear', 'shear', -360, Constraints(-360, 360, 0.01, float))))
        return [scale, translate_percent, rotate, shear]

    def _init_function(self) -> callable:
        return iaa.Affine

    def _init_sub_functions_param(self) -> str:
        return ""
