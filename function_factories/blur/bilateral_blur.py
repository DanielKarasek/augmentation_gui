from typing import List

from imgaug import augmenters as iaa

from projects_src.augmentation_gui.function_model import IFunctionFactory
from projects_src.augmentation_gui.parameter_models.constraints import Constraints
from projects_src.augmentation_gui.parameter_models.number_parameter import NumberParameter
from projects_src.augmentation_gui.parameter_models.parameter_interface import Parameter
from projects_src.augmentation_gui.parameter_models.tuple_parameter import StringDescription, TupleParameter


class BilateralBlur(IFunctionFactory):

    def __init__(self, parent=None):
        super().__init__(parent)

    def _init_name(self) -> str:
        return "Bilateral Blur"

    def _init_parameters(self) -> List[Parameter]:
        d = NumberParameter('d', 'd', 1, Constraints(1, 50, 1, int))
        sigma_color = TupleParameter('Sigma Color', 'sigma_color', (StringDescription('from'), NumberParameter('sigma_color', 'sigma_color', 10, Constraints(0, 999, 0.01, float)), StringDescription('to'), NumberParameter('sigma_color', 'sigma_color', 250, Constraints(0, 999, 0.01, float))))
        sigma_space = TupleParameter('Sigma Space', 'sigma_space', (StringDescription('from'), NumberParameter('sigma_space', 'sigma_space', 10, Constraints(0, 999, 0.01, float)), StringDescription('to'), NumberParameter('sigma_space', 'sigma_space', 250, Constraints(0, 999, 0.01, float))))
        return [d, sigma_color, sigma_space]

    def _init_function(self) -> callable:
        return iaa.BilateralBlur

    def _init_sub_functions_param(self) -> str:
        return ""
