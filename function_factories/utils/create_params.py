from typing import List, Union
from parameter_models.boolean_parameter import BooleanParameter
from parameter_models.constraints import Constraints
from parameter_models.number_parameter import NumberParameter
from parameter_models.parameter_interface import Parameter
from parameter_models.tuple_parameter import StringDescription, TupleParameter


def create_parameters_method(param_specs: List[Union[str, List]]) -> str:
    method_lines = ["def _init_parameters(self) -> List[Parameter]:"]
    for spec in param_specs:
        name, param_type, further_specs = spec
        if param_type == 'BooleanParameter':
            method_lines.append(f"        {name} = BooleanParameter('{name}', '{name}', False)")
        elif param_type == 'NumberParameter':
            min_val, max_val, data_type = further_specs
            preceding_parameter = 0.01 if data_type == 'float' else 1
            method_lines.append(
                f"        constraint_{name} = Constraints({min_val}, {max_val}, {preceding_parameter}, {data_type})")
            method_lines.append(f"        {name} = NumberParameter('{name}', '{name}', {min_val}, constraint_{name})")
        elif param_type == 'TupleParameter':
            tuple_params = []
            for item in further_specs:
                if isinstance(item, str):
                    tuple_params.append(f"StringDescription('{item}')")
                else:
                    min_val, max_val, data_type = item
                    preceding_parameter = 0.01 if data_type == 'float' else 1
                    tuple_params.append(
                        f"NumberParameter('{name}', '{name}', {min_val}, Constraints({min_val}, {max_val}, {preceding_parameter}, {data_type}))")
            method_lines.append(f"        {name} = TupleParameter('{name}', '{name}', ({', '.join(tuple_params)}))")
    method_lines.append("        return [" + ", ".join([spec[0] for spec in param_specs]) + "]")
    return "\n".join(method_lines)


param_specs = [

    ('loc', 'NumberParameter', (0, 255, 'float')),
    ('scale', 'TupleParameter', ('from', (0, 255, 'float'), 'to', (0, 255, 'float'))),
    ('per_channel', 'NumberParameter', (0, 1, 'float'))
]
print(create_parameters_method(param_specs))
# param_specs ARITHMETHIC
# param_specs = {"multiply": (("mul", "TupleParameter", ["from", (0, 8, "float"), "to", (0, 8, "float")]),
#                             ("per_channel", "NumberParameter", (0, 1, "float"))),
#                "salt_and_pepper": (("p", "NumberParameter", (0, 1, "float")),
#                                    ("per_channel", "NumberParameter", (0, 1, "float")),),
#                "coarse_pepper": (("p", "NumberParameter", (0, 1, "float")),
#                                  ("size_percent", "NumberParameter", (0, 1, "float")),
#                                  ("per_channel", "NumberParameter", (0, 1, "float"))),
#                "coarse_salt_and_pepper": (("p", "NumberParameter", (0, 1, "float")),
#                                           ("size_percent", "NumberParameter", (0, 1, "float"))
#                                           , ("per_channel", "NumberParameter", (0, 1, "float"))),
#                "dropout2d": (("p", "NumberParameter", (0, 1, "float")),
#                              ("nb_keep_channels", "NumberParameter", (1, 3, "int"))),
#                "additive_poisson_noise": (("loc", "NumberParameter", (0, 255, "float")),
#                                           ("scale", "TupleParameter", ["from", (0, 255, "float"),
#                                            "to", (0, 255, "float")]),
#                                           ("per_channel", "NumberParameter", (0, 1, "float"))),
#                "pepper": (("p", "NumberParameter", (0, 1, "float")),
#                           ("per_channel", "NumberParameter", (0, 1, "float"))),
#                "coarse_dropout": (("p", "NumberParameter", (0, 1, "float")),
#                                   ("size_percent", "NumberParameter", (0, 1, "float")),
#                                   ("per_channel", "NumberParameter", (0, 1, "float"))),
#                "multiply_elementwise": (("mul", "TupleParameter", ["from", (0, 8, "float"), "to", (0, 8, "float")]),
#                                         ("per_channel", "NumberParameter", (0, 1, "float"))),
#                "salt": (("p", "NumberParameter", (0, 1, "float")),
#                         ("per_channel", "NumberParameter", (0, 1, "float"))),
#                "solarize": (("p", "NumberParameter", (0, 1, "float")),
#                             ("per_channel", "NumberParameter", (0, 1, "float"))),
#                "invert": (("p", "NumberParameter", (0, 1, "float")),
#                           ("per_channel", "NumberParameter", (0, 1, "float"))),
#                "dropout": (("p", "NumberParameter", (0, 1, "float")),
#                            ("per_channel", "NumberParameter", (0, 1, "float"))),
#                "jpeg_compression": (("compression", "TupleParameter",
#                                      ["from", (0, 100, "float"), "to", (0, 100, "float")]),),
#
#                "coarse_salt": (("p", "NumberParameter", (0, 1, "float")),
#                                ("size_percent", "NumberParameter", (0, 1, "float")),
#                                ("per_channel", "NumberParameter", (0, 1, "float"))),
#                "contrast_normalization": (("alpha", "NumberParameter", (0, 20, "float")),
#                                           ("per_channel", "NumberParameter", (0, 1, "float"))),
#                }
# PARAM SPECS GEOMETRIC
# param_specs = {"affine": (("scale", "TupleParameter", ["from", (0, 5, "float"), "to", (0, 5, "float")]),
#                           ("translate_percent", "TupleParameter", ["from", (0, 1, "float"), "to", (0, 1, "float")]),
#                           ("rotate", "TupleParameter", ["from", (-360, 360, "float"), "to", (-360, 360, "float")]),
#                           ("shear", "TupleParameter", ["from", (-360, 360, "float"), "to", (-360, 360, "float")])),
#                "elastic_transformation": (("alpha", "NumberParameter", (0, 100, "float")),
#                                             ("sigma", "NumberParameter", (0, 100, "float"))),
#                "jigsaw": (("nb_rows", "NumberParameter", (1, 10, "int")),
#                             ("nb_cols", "NumberParameter", (1, 10, "int")),
#                           ("max_steps", "NumberParameter", (1, 10, "int"))),
#                "perspective_transform": (("scale", "TupleParameter",
#                                           ["from", (0, 1, "float"), "to", (0, 1, "float")]),),
#                "piecewise_affine": (("scale", "TupleParameter", ["from", (0, 1, "float"), "to", (0, 1, "float")]),
#                                      ("nb_rows", "NumberParameter", (1, 10, "int")),
#                                      ("nb_cols", "NumberParameter", (1, 10, "int"))),
#                "rot90": (("k", "TupleParameter", ["from", (0, 3, "int"), "to", (0, 3, "int")]),),
#                "rotate": (("rotate", "TupleParameter", ["from", (-360, 360, "float"), "to", (-360, 360, "float")]),),
#                "scale_x": (("scale", "TupleParameter", ["from", (0, 5, "float"), "to", (0, 5, "float")]),),
#                "scale_y": (("scale", "TupleParameter", ["from", (0, 5, "float"), "to", (0, 5, "float")]),),
#                "shear_x": (("shear", "TupleParameter", ["from", (-360, 360, "float"), "to", (-360, 360, "float")]),),
#                "shear_y": (("shear", "TupleParameter", ["from", (-360, 360, "float"), "to", (-360, 360, "float")]),),
#                "translate_x": (("percent", "TupleParameter", ["from", (0, 1, "float"), "to", (0, 1, "float")]),),
#                "translate_y": (("percent", "TupleParameter", ["from", (0, 1, "float"), "to", (0, 1, "float")]),),
#                }

# PARAM SPECS FLIP
# param_specs = {"fliplr": (("p", "NumberParameter", (0, 1, "float")),),
#                "flipud": (("p", "NumberParameter", (0, 1, "float")),),
#                }

# param specs BLUR
param_specs = {"average_blur": (("k", "TupleParameter", ["from", (1, 10000, "int"), "to", (1, 10000, "int")]),),
                "gaussian_blur": (("sigma", "TupleParameter", ["from", (0, 100, "float"), "to", (0, 100, "float")]),),
                "median_blur": (("k", "TupleParameter", ["from", (1, 10000, "int"), "to", (1, 10000, "int")]),),
                "motion_blur": (("k", "TupleParameter", ["from", (1, 10000, "int"), "to", (1, 10000, "int")]),
                                ("angle", "TupleParameter", ["from", (0, 360, "float"), "to", (0, 360, "float")]),
                                ("direction", "NumberParameter", (-1.0, 1.0, "float"))),
                "bilateral_blur": (("d", "TupleParameter", ["from", (1, 10000, "int"), "to", (1, 10000, "int")]),
                              ("sigma_color", "TupleParameter", ["from", (0, 999, "float"), "to", (0, 999, "float")]),
                              ("sigma_space", "TupleParameter", ["from", (0, 999, "float"), "to", (0, 999, "float")]),),
                "mean_shift_blur": (("spatial_radius", "TupleParameter", ["from", (1, 1000, "int"), "to", (1, 10000, "int")]),
                                  ("color_radius", "TupleParameter", ["from", (1, 1000, "int"), "to", (1, 10000, "int")]),),

                 }





import re

for key, value in param_specs.items():
    # Generate the new _init_parameters method string
    new_method_string = create_parameters_method(value)+"\n\n    "

    # Open the corresponding Python file
    file_path = f'./{key}.py'
    with open(file_path, 'r') as f:
        file_content = f.read()

    # Replace the _init_parameters method with the new method string
    file_content = re.sub(r'def _init_parameters\(self\) -> List\[Parameter\]:.*?(?=def _init_|$)',
                          new_method_string, file_content, flags=re.DOTALL)

    # Write the updated content back to the file
    with open(file_path, 'w') as f:
        f.write(file_content)
    # print(file_content)