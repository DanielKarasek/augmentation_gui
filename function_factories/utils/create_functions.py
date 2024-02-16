import os
# BLUR methods
methods = [
           "GaussianBlur",
           "AverageBlur",
           "MedianBlur",
           "BilateralBlur",
           "MotionBlur",
           "MeanShiftBlur",
           ]
# FLIP
# methods = [
#            "Fliplr",
#            "Flipud",
#            ]

# GEOMETRIC methods
# methods = [
#         "Affine",
#         "ScaleX",
#         "ScaleY",
#         "TranslateX",
#         "TranslateY",
#         "Rotate",
#         "ShearX",
#         "ShearY",
#         "PiecewiseAffine",
#         "PerspectiveTransform",
#         "ElasticTransformation",
#         "Rot90",
#         "WithPolarWarping",
#         "Jigsaw",
# ]
# META
# methods = [
#             "SomeOf",
#             "OneOf",
#             "Sometimes",
#     ]

template = '''from typing import List

from imgaug import augmenters as iaa

from function_model import IFunctionFactory
from parameter_models.boolean_parameter import BooleanParameter
from parameter_models.constraints import Constraints
from parameter_models.number_parameter import NumberParameter
from parameter_models.parameter_interface import Parameter
from parameter_models.tuple_parameter import StringDescription, TupleParameter


class {class_name}(IFunctionFactory):

    def __init__(self, parent=None):
        super().__init__(parent)

    def _init_name(self) -> str:
        return "{method_name_with_spaces}"

    def _init_parameters(self) -> List[Parameter]:
        # TODO: Define the parameters for the method
        return []

    def _init_function(self) -> callable:
        return iaa.{method_name}

    def _init_sub_functions_param(self) -> str:
        return ""
'''

for method in methods:
    # lower method name but add _ between words
    method_lower = ''.join(['_' + i.lower() if i.isupper() else i for i in method]).lstrip('_')
    # camel case but with spaces between words
    method_name_with_spaces = ''.join([' ' + i if i.isupper() else i for i in method]).lstrip(' ')
    with open(f'{method_lower}.py', 'w') as f:
        f.write(template.format(class_name=method,
                                method_name=method,
                                method_name_with_spaces=method_name_with_spaces))
