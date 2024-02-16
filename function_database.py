from function_factories.arithmetic.add import Add
from function_factories.arithmetic.add_elementwise import AddElementwise
from function_factories.arithmetic.add_gaussian_noise import AddGaussianNoise
from function_factories.arithmetic.additive_laplace_noise import AdditiveLaplaceNoise
from function_factories.arithmetic.additive_poisson_noise import AdditivePoissonNoise
from function_factories.arithmetic.coarse_dropout import CoarseDropout
from function_factories.arithmetic.coarse_pepper import CoarsePepper
from function_factories.arithmetic.coarse_salt import CoarseSalt
from function_factories.arithmetic.coarse_salt_and_pepper import CoarseSaltAndPepper
from function_factories.arithmetic.contrast_normalization import ContrastNormalization
from function_factories.arithmetic.dropout import Dropout
from function_factories.arithmetic.dropout2d import Dropout2d
from function_factories.arithmetic.invert import Invert
from function_factories.arithmetic.jpeg_compression import JpegCompression
from function_factories.arithmetic.multiply import Multiply
from function_factories.arithmetic.multiply_elementwise import MultiplyElementwise
from function_factories.arithmetic.pepper import Pepper
from function_factories.arithmetic.salt import Salt
from function_factories.arithmetic.salt_and_pepper import SaltAndPepper
from function_factories.arithmetic.solarize import Solarize
from function_factories.blur.average_blur import AverageBlur
from function_factories.blur.bilateral_blur import BilateralBlur
from function_factories.blur.gaussian_blur import GaussianBlur
from function_factories.blur.mean_shift_blur import MeanShiftBlur
from function_factories.blur.median_blur import MedianBlur
from function_factories.blur.motion_blur import MotionBlur
from function_factories.empty import Empty
from function_factories.flip.fliplr import Fliplr
from function_factories.flip.flipud import Flipud
from function_factories.geometric.affine import Affine
from function_factories.geometric.elastic_transformation import ElasticTransformation
from function_factories.geometric.jigsaw import Jigsaw
from function_factories.geometric.perspective_transform import PerspectiveTransform
from function_factories.geometric.piecewise_affine import PiecewiseAffine
from function_factories.geometric.roll import Roll
from function_factories.geometric.rot90 import Rot90
from function_factories.geometric.rotate import Rotate
from function_factories.geometric.scale_x import ScaleX
from function_factories.geometric.scale_y import ScaleY
from function_factories.geometric.shear_x import ShearX
from function_factories.geometric.shear_y import ShearY
from function_factories.geometric.translate_x import TranslateX
from function_factories.geometric.translate_y import TranslateY
from function_factories.geometric.with_polar_warping import WithPolarWarping
from function_factories.meta.one_of import OneOf
from function_factories.meta.sequential import Sequential
from function_factories.meta.some_of import SomeOf
from function_factories.meta.sometimes import Sometimes
from function_model import FunctionModel


class FunctionDatabase:
    function_database = [Add(),
                         AddElementwise(),
                         AddGaussianNoise(),
                         AdditiveLaplaceNoise(),
                         AdditivePoissonNoise(),
                         CoarseDropout(),
                         CoarsePepper(),
                         CoarseSalt(),
                         CoarseSaltAndPepper(),
                         ContrastNormalization(),
                         Dropout(),
                         Dropout2d(),
                         Empty(),
                         Invert(),
                         JpegCompression(),
                         Multiply(),
                         MultiplyElementwise(),
                         Pepper(),
                         Salt(),
                         SaltAndPepper(),
                         Solarize(),

                         Affine(),
                         ScaleX(),
                         ScaleY(),
                         TranslateX(),
                         TranslateY(),
                         Rotate(),
                         ShearX(),
                         ShearY(),
                         PiecewiseAffine(),
                         PerspectiveTransform(),
                         ElasticTransformation(),
                         Rot90(),
                         WithPolarWarping(),
                         Jigsaw(),

                         Sequential(),
                         SomeOf(),
                         OneOf(),
                         Sometimes(),

                         Fliplr(),
                         Flipud(),

                         GaussianBlur(),
                         AverageBlur(),
                         MedianBlur(),
                         BilateralBlur(),
                         MotionBlur(),
                         MeanShiftBlur(),
                         Roll(),
                         ]

    @staticmethod
    def get_function_by_name(name: str) -> FunctionModel:
        for fnc in FunctionDatabase.function_database:
            if fnc.name == name:
                return fnc.function
        raise ValueError(f"Function with name {name} not found")

    @staticmethod
    def __iter__():
        return iter(FunctionDatabase.function_database)

