from typing import List

from imgaug import augmenters as iaa

from projects_src.augmentation_gui.function_model import IFunctionFactory
from projects_src.augmentation_gui.parameter_models.constraints import Constraints
from projects_src.augmentation_gui.parameter_models.number_parameter import NumberParameter
from projects_src.augmentation_gui.parameter_models.parameter_interface import Parameter
from projects_src.augmentation_gui.parameter_models.tuple_parameter import StringDescription, TupleParameter


class MeanShiftBlur(IFunctionFactory):

    def __init__(self, parent=None):
        super().__init__(parent)

    def _init_name(self) -> str:
        return "Mean Shift Blur"

    def _init_parameters(self) -> List[Parameter]:
        spatial_radius = TupleParameter('spatial_radius', 'spatial_radius', (StringDescription('from'), NumberParameter('spatial_radius', 'spatial_radius', 5, Constraints(1, 1000, 1, int)), StringDescription('to'), NumberParameter('spatial_radius', 'spatial_radius', 40, Constraints(1, 10000, 1, int))))
        color_radius = TupleParameter('color_radius', 'color_radius', (StringDescription('from'), NumberParameter('color_radius', 'color_radius', 5, Constraints(1, 1000, 1, int)), StringDescription('to'), NumberParameter('color_radius', 'color_radius', 40, Constraints(1, 10000, 1, int))))
        return [spatial_radius, color_radius]

    def _init_function(self) -> callable:
        return iaa.MeanShiftBlur

    def _init_sub_functions_param(self) -> str:
        return ""
