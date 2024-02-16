from typing import Literal

import numpy as np
import skimage.transform as tf
from imgaug.augmenters import meta
import imgaug.parameters as iap
import imgaug as ia
from imgaug.augmenters.geometric import _warp_affine_arr
import six.moves as sm
from nptyping import NDArray, Shape, Int


def _is_identity_matrix(matrix):
    return np.allclose(matrix, np.eye(matrix.shape[0], dtype=matrix.dtype))


def _wrap_coordinate_circularly(xy_coords: NDArray[Shape["M, 2"], Int],
                                boundaries: tuple[int, int]):
    xy_coords %= np.array(boundaries).reshape((-1, 2))
    return xy_coords


class _RollSampleResult(object):
    def __init__(self, roll_x_ratio: list[float], roll_y_ratio: list[float]):
        self._roll_x_ratio = roll_x_ratio
        self._roll_y_ratio = roll_y_ratio

    # Added in 0.4.0.
    def get_affine_parameters(self, idx: int, arr_shape: tuple[int]):
        roll_x_ratio = self._roll_x_ratio[idx]
        roll_y_ratio = self._roll_y_ratio[idx]

        roll_x_px = roll_x_ratio * arr_shape[1]
        roll_y_px = roll_y_ratio * arr_shape[0]

        return {
            "roll_y_px": roll_y_px,
            "roll_x_px": roll_x_px,
        }

    def to_matrix(self,
                  idx: int,
                  arr_shape: tuple[int],
                  image_shape: tuple[int],
                  is_image: bool = False):
        if 0 in image_shape:
            return tf.AffineTransform(), arr_shape

        height, width = arr_shape[0:2]

        params = self.get_affine_parameters(idx,
                                            arr_shape=arr_shape)

        # for images we use additional shifts of (0.5, 0.5) as otherwise
        # we get an ugly black border for 90deg rotations
        add_factor = 0.5 if is_image else 0.0
        shift_y = height / 2.0 - add_factor
        shift_x = width / 2.0 - add_factor

        matrix_to_topleft = tf.SimilarityTransform(
            translation=[-shift_x, -shift_y])
        matrix_transforms = tf.AffineTransform(
            translation=(params["roll_x_px"], params["roll_y_px"]),
        )
        matrix_to_center = tf.SimilarityTransform(
            translation=[shift_x, shift_y])
        matrix = (matrix_to_topleft
                  + matrix_transforms
                  + matrix_to_center)
        return matrix, arr_shape

    def to_matrix_cba(self, idx, arr_shape):
        return self.to_matrix(idx, arr_shape, arr_shape)

    def copy(self):
        # TODO: this only copies references, not the actual data
        return _RollSampleResult(
            roll_x_ratio=self._roll_x_ratio,
            roll_y_ratio=self._roll_y_ratio
        )


class RollAugment(meta.Augmenter):

    def __init__(self,
                 roll_x_ratio: tuple[float, float] = (0.0, 0.0),
                 roll_y_ratio: tuple[float, float] = (0.0, 0.0),
                 backend: Literal['auto', 'cv2', 'skimage'] = "auto",
                 seed=None,
                 name=None):
        super(RollAugment, self).__init__(seed=seed, name=name)
        self._roll_x_ratio = self._handle_roll_param(roll_x_ratio)
        self._roll_y_ratio = self._handle_roll_param(roll_y_ratio)
        self._backend = backend

    @classmethod
    def _handle_roll_param(cls,
                           roll_ratio: tuple[float, float] = (0.0, 0.0)) -> iap.Uniform:
        return (
            iap.handle_continuous_param(
                roll_ratio, "roll_ratio", value_range=None,
                tuple_to_uniform=True, list_to_choice=True)
        )

    def _augment_batch_(self, batch, random_state, parents, hooks):
        samples = self._draw_samples(batch.nb_rows, random_state)

        if batch.images is not None:
            batch.images = self._augment_images_by_samples(batch.images,
                                                           samples)

        for augm_name in ["keypoints", "bounding_boxes", "polygons",
                          "line_strings"]:
            augm_value = getattr(batch, augm_name)
            if augm_value is not None:
                for i, cbaoi in enumerate(augm_value):
                    matrix, output_shape = samples.to_matrix_cba(
                        i, cbaoi.shape)

                    if (not cbaoi.empty
                            and 0 not in cbaoi.shape[0:2]):
                        # TODO this is hacky
                        if augm_name == "bounding_boxes":

                            raise Exception("NOT SUPPORTED YET!")
                            # Ensure that 4 points are used for bbs.
                            # to_keypoints_on_images() does return 4 points,
                            # to_xy_array() does not.
                            # kpsoi = cbaoi.to_keypoints_on_image()
                            # coords = kpsoi.to_xy_array()
                            # coords_aug = tf.matrix_transform(coords,
                            #                                  matrix.params)
                            # kpsoi = kpsoi.fill_from_xy_array_(coords_aug)
                            # cbaoi = cbaoi.invert_to_keypoints_on_image_(
                            #     kpsoi)
                        elif augm_name == "keypoints":
                            coords = cbaoi.to_xy_array()
                            coords_aug = tf.matrix_transform(coords,
                                                             matrix.params)
                            coords_aug = _wrap_coordinate_circularly(xy_coords=coords_aug,
                                                                     boundaries=cbaoi.shape[0:2])
                            cbaoi = cbaoi.fill_from_xy_array_(coords_aug)
                        else:
                            raise Exception("NOT SUPPORTED YET!")
                            # coords = cbaoi.to_xy_array()
                            # coords_aug = tf.matrix_transform(coords,
                            #                                  matrix.params)
                            # cbaoi = cbaoi.fill_from_xy_array_(coords_aug)

                    cbaoi.shape = output_shape
                    augm_value[i] = cbaoi

        return batch

    def _augment_images_by_samples(self, images, samples,
                                   image_shapes=None):
        nb_images = len(images)
        result = []
        for i in sm.xrange(nb_images):
            image = images[i]

            image_shape = (image.shape if image_shapes is None
                           else image_shapes[i])
            matrix, output_shape = samples.to_matrix(i, image.shape,
                                                     image_shape)

            image_warped = _warp_affine_arr(
                image, matrix,
                order=1, mode="wrap", cval=[0, 0, 0],
                output_shape=output_shape, backend=self._backend)

            result.append(image_warped)

        return result

    def _draw_samples(self, nb_samples, random_state):
        rngs = random_state.duplicate(2)

        roll_x_sample = self._roll_x_ratio.draw_samples((nb_samples,),
                                                        random_state=rngs[0])
        roll_y_sample = self._roll_y_ratio.draw_samples((nb_samples,),
                                                        random_state=rngs[1])

        return _RollSampleResult(
            roll_x_ratio=roll_x_sample,
            roll_y_ratio=roll_y_sample
        )

    def get_parameters(self):
        """See :func:`~imgaug.augmenters.meta.Augmenter.get_parameters`."""
        return [
            self._roll_y_ratio, self._roll_y_ratio, self._backend]
