from typing import List

from imgaug import augmenters as iaa

from projects_src.augmentation_gui.function_model import IFunctionFactory
from projects_src.augmentation_gui.parameter_models.constraints import Constraints
from projects_src.augmentation_gui.parameter_models.number_parameter import NumberParameter
from projects_src.augmentation_gui.parameter_models.parameter_interface import Parameter
from projects_src.augmentation_gui.parameter_models.tuple_parameter import StringDescription, TupleParameter


class AdditiveLaplaceNoise(IFunctionFactory):

    def __init__(self, parent=None):
        super().__init__(parent)

    def _init_name(self) -> str:
        return "Additive Laplace Noise"

    def _init_parameters(self) -> List[Parameter]:
        constraint_loc = Constraints(0, 255, 0.01, float)
        loc = NumberParameter('Loc', 'loc', 0, constraint_loc)
        scale = TupleParameter('Scale sampled per image', 'scale', (
        StringDescription('from:'), NumberParameter('scale', 'scale', 0, Constraints(0, 255, 0.01, float)),
        StringDescription('to:'), NumberParameter('scale', 'scale', 0, Constraints(0, 255, 0.01, float))))
        constraint_per_channel = Constraints(0, 1, 0.01, float)
        per_channel = NumberParameter('per_channel', 'per_channel', 0, constraint_per_channel)
        return [loc, scale, per_channel]

    def _init_function(self) -> callable:
        return iaa.AdditiveLaplaceNoise

    def _init_sub_functions_param(self) -> str:
        return ""
