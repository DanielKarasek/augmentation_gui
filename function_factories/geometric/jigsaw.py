from typing import List

from imgaug import augmenters as iaa

from projects_src.augmentation_gui.function_model import IFunctionFactory
from projects_src.augmentation_gui.parameter_models.constraints import Constraints
from projects_src.augmentation_gui.parameter_models.number_parameter import NumberParameter
from projects_src.augmentation_gui.parameter_models.parameter_interface import Parameter


class Jigsaw(IFunctionFactory):

    def __init__(self, parent=None):
        super().__init__(parent)

    def _init_name(self) -> str:
        return "Jigsaw"

    def _init_parameters(self) -> List[Parameter]:
        constraint_nb_rows = Constraints(1, 10, 1, int)
        nb_rows = NumberParameter('nb_rows', 'nb_rows', 1, constraint_nb_rows)
        constraint_nb_cols = Constraints(1, 10, 1, int)
        nb_cols = NumberParameter('nb_cols', 'nb_cols', 1, constraint_nb_cols)
        constraint_max_steps = Constraints(1, 10, 1, int)
        max_steps = NumberParameter('max_steps', 'max_steps', 1, constraint_max_steps)
        return [nb_rows, nb_cols, max_steps]

    def _init_function(self) -> callable:
        return iaa.Jigsaw

    def _init_sub_functions_param(self) -> str:
        return ""
