from typing import List

from imgaug import augmenters as iaa

from projects_src.augmentation_gui.function_model import IFunctionFactory
from projects_src.augmentation_gui.parameter_models.constraints import Constraints
from projects_src.augmentation_gui.parameter_models.number_parameter import NumberParameter
from projects_src.augmentation_gui.parameter_models.parameter_interface import Parameter
from projects_src.augmentation_gui.parameter_models.tuple_parameter import StringDescription, TupleParameter


class ElasticTransformation(IFunctionFactory):

    def __init__(self, parent=None):
        super().__init__(parent)

    def _init_name(self) -> str:
        return "Elastic Transformation"

    def _init_parameters(self) -> List[Parameter]:
        constraint_alpha = Constraints(0., 150., 0.01, float)
        alpha_lower = NumberParameter('alpha', 'alpha', 0., constraint_alpha)
        alpha_upper = NumberParameter('alpha', 'alpha', 40., constraint_alpha)
        alpha = TupleParameter('alpha', 'alpha', (StringDescription('from'), alpha_lower, StringDescription('to'), alpha_upper))
        constraint_sigma = Constraints(0., 50., 0.01, float)
        sigma_lower = NumberParameter('sigma', 'sigma', 4., constraint_sigma)
        sigma_upper = NumberParameter('sigma', 'sigma', 8., constraint_sigma)
        sigma = TupleParameter('sigma', 'sigma', (StringDescription('from'), sigma_lower, StringDescription('to'), sigma_upper))
        return [alpha, sigma]

    def _init_function(self) -> callable:
        return iaa.ElasticTransformation

    def _init_sub_functions_param(self) -> str:
        return ""
