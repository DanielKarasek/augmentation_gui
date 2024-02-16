from typing import List

from imgaug import augmenters as iaa

from projects_src.augmentation_gui.function_model import IFunctionFactory
from projects_src.augmentation_gui.parameter_models.boolean_parameter import BooleanParameter
from projects_src.augmentation_gui.parameter_models.constraints import Constraints
from projects_src.augmentation_gui.parameter_models.number_parameter import NumberParameter
from projects_src.augmentation_gui.parameter_models.parameter_interface import Parameter
from projects_src.augmentation_gui.parameter_models.tuple_parameter import StringDescription, TupleParameter


class AddGaussianNoise(IFunctionFactory):

    def __init__(self, parent=None):
        super().__init__(parent)

    def _init_name(self) -> str:
        return "Add gaussian noise"

    def _init_parameters(self) -> List[Parameter]:
        constraint = Constraints(0., 255., 1., float)
        loc = NumberParameter("Loc (μ):",
                                "loc",
                                0,
                                constraint)
        scale_from = NumberParameter("σ from",
                                    "scale",
                                    0,
                                    constraint)
        scale_to = NumberParameter("σ to",
                                    "scale",
                                    10,
                                    constraint)
        string_lower = StringDescription("from: ")
        string_upper = StringDescription("to: ")

        scale = TupleParameter("Scale sampled per image",
                                    "scale",
                                    (string_lower,
                                     scale_from,
                                     string_upper,
                                     scale_to))

        per_channel = BooleanParameter("Per channel",
                                       "per_channel",
                                       False,
                                       )
        return [loc, scale, per_channel]

    def _init_function(self) -> callable:
        return iaa.AdditiveGaussianNoise

    def _init_sub_functions_param(self) -> str:
        return ""
