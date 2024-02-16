from typing import List

from imgaug import augmenters as iaa

from projects_src.augmentation_gui.function_model import IFunctionFactory
from projects_src.augmentation_gui.parameter_models.constraints import Constraints
from projects_src.augmentation_gui.parameter_models.number_parameter import NumberParameter
from projects_src.augmentation_gui.parameter_models.parameter_interface import Parameter
from projects_src.augmentation_gui.parameter_models.tuple_parameter import StringDescription, TupleParameter


class PiecewiseAffine(IFunctionFactory):

    def __init__(self, parent=None):
        super().__init__(parent)

    def _init_name(self) -> str:
        return "Piecewise Affine"

    def _init_parameters(self) -> List[Parameter]:
        scale = TupleParameter('scale', 'scale', (StringDescription('from'), NumberParameter('scale', 'scale', 0, Constraints(0, 1, 0.01, float)), StringDescription('to'), NumberParameter('scale', 'scale', 0.06, Constraints(0, 1, 0.01, float))))
        constraint_nb_rows = Constraints(1, 10, 1, int)
        nb_rows = NumberParameter('nb_rows', 'nb_rows', 1, constraint_nb_rows)
        constraint_nb_cols = Constraints(1, 10, 1, int)
        nb_cols = NumberParameter('nb_cols', 'nb_cols', 1, constraint_nb_cols)
        return [scale, nb_rows, nb_cols]

    def _init_function(self) -> callable:
        return iaa.PiecewiseAffine

    def _init_sub_functions_param(self) -> str:
        return ""
