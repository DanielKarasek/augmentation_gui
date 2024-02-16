# This Python file uses the following encoding: utf-8
import json
import os
import random
import sys
from copy import deepcopy
from pathlib import Path
from typing import List, Tuple

import cv2
import numpy as np
from PySide6.QtCore import QCoreApplication, QObject, Signal, Property, Slot
from PySide6.QtGui import QGuiApplication, QFontDatabase
from PySide6.QtQml import QQmlApplicationEngine
from imgaug import Keypoint, KeypointsOnImage
from imgaug.augmenters import Augmenter

from ImageTableModel import ImageTableModel
from ai_core.data_flow.pipeline_elements.annotation_parsers.ap_factory import AnnotationParserFactory
from ai_core.data_flow.pipeline_elements.dataset_loaders.dl_factory import DatasetLoaderFactory
from ai_core.data_structure.colours.colour import Colour
from ai_core.data_structure.coordinates.keypoint_general import KeypointGeneral
from ai_core.data_structure.coordinates.point import Point
from ai_core.data_structure.data_collections.base_collection import BaseCollection
from function_database import FunctionDatabase
from function_model_tree import TreeModel
from projects_src.augmentation_gui.image_utils import letterbox
from projects_src.bioster.src.experimental.letterbox2_0 import letterbox2_0


def load_images_from_folder(folder: str, N: int) -> list:
    images = []
    for filename in os.listdir(folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            images.append(filename)

    if len(images) > N:
        images = random.sample(images, N)

    loaded_images = []
    # Load the images
    for img in images:
        img_path = os.path.join(folder, img)
        img_bgr = cv2.imread(img_path, cv2.IMREAD_COLOR)
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        img_rgb = img_rgb[:, :img_rgb.shape[1] - img_rgb.shape[1] % 4, :]
        img_rgb = letterbox(img_rgb)
        loaded_images.append(img_rgb)

    return loaded_images


def peak_keypoint_aug(seq: Augmenter, image: np.ndarray, keypoints: List[KeypointGeneral]) -> Tuple[
    np.ndarray, List[KeypointGeneral]]:
    keypoints = [keypoint.shape for keypoint in keypoints]
    h, w, _ = image.shape
    kps = KeypointsOnImage([Keypoint(x=kp.center_point.x, y=kp.center_point.y) for kp in keypoints], shape=image.shape)

    image_aug, kps_aug = seq(image=image, keypoints=kps)
    aug_points = [KeypointGeneral(Point(kp_aug.x % w, kp_aug.y % h), orig_kp.name) for kp_aug, orig_kp in
                  zip(kps_aug, keypoints)]

    return image_aug, aug_points


class BackendModel(QObject):
    # TODO: Move into IAA model
    augmentationStringChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._augmentationString = "Unnamed pipeline"
        self._tree_model = self._init_tree_model()
        self._image_grid_model = self._init_image_grid_model()
        self._example_images_cnt = 8
        self._augment_cnt = 3
        self._example_images = []
        self._annotations = []
        # self.load_dataset("/home/danielkarasek/PycharmProjects/AI_data/peak_keypoint_dataset/val")
        self.create_augmented_examples()

    @Slot(str)
    def create_new_pipeline(self, name: str):
        self._tree_model.reset_model()
        self.augmentationString = name

    @Slot(str)
    def change_pipeline_name(self, name: str):
        self.augmentationString = name

    @Slot()
    def create_augmented_examples(self):
        augmentor = self._tree_model.build_callable_pipeline()
        augmented_images = []

        for i in range(len(self._example_images)):
            orig_image, tr = letterbox2_0(self._example_images[i], scale_up_flag=True)
            for kp in deepcopy(self._annotations[i].dets):
                kp = kp.shape
                kp: KeypointGeneral
                kp = kp.apply_transformation(tr)
                kp.draw(orig_image, radius=10, thickness=5, colour=Colour(1, 0, 0))
            augmented_images.append([orig_image])

            for aug_num in range(self._augment_cnt):
                aug_im, aug_annot = peak_keypoint_aug(seq=augmentor, image=self._example_images[i],
                                                      keypoints=self._annotations[i].dets)
                aug_im, tr = letterbox2_0(aug_im, scale_up_flag=True)
                for kp in aug_annot:
                    kp: KeypointGeneral
                    kp = kp.apply_transformation(tr)
                    kp.draw(aug_im, radius=10, thickness=5, colour=Colour(1, 0, 0))
                augmented_images[-1].append(aug_im)

        # for row in range(len(augmented_images)):
        #     augmented_images[row] = [self._example_images[row], *augmented_images[row]]
        self._image_grid_model.setImageData(augmented_images)

    @Slot(str)
    def save_model_to_file(self, path: str):
        if path[-5:] != ".json":
            path += ".json"
        path = path[7:]
        tree_model_dict = self._tree_model.to_dict()
        save_dict = {"pipeline name": self.augmentationString, "data": tree_model_dict}
        with open(path, "w") as f:
            json.dump(save_dict, f, indent=2)

    @Slot(str)
    def load_model(self, path: str):
        path = path[7:]
        with open(path, "r") as f:
            model_dict = json.load(f)
            self._tree_model.from_dict(model_dict["data"])
            self.augmentationString = model_dict["pipeline name"]

    @Slot(str)
    def load_dataset(self, path: str):
        path = path[7:]
        dl_cvat = DatasetLoaderFactory.DatasetLoaderCVAT(path)
        anns = AnnotationParserFactory.AnnotationParserCVAT(dl_cvat, BaseCollection()).parse_dataset()
        if len(anns) > self._example_images_cnt:
            anns = random.sample(anns, self._example_images_cnt)
        image_files_list = [ann.img_data for ann in anns]
        self._example_images = []
        for ann in anns:
            dets = list(filter(lambda det: isinstance(det.shape, KeypointGeneral), ann.dets))
            ann.set_dets(dets)
        self._annotations = anns
        for image_data in image_files_list:
            new_image = image_data.data
            new_image = cv2.cvtColor(new_image, cv2.COLOR_GRAY2RGB)
            self._example_images.append(new_image)
        self.create_augmented_examples()

    @Property(QObject, constant=True)
    def treeModel(self) -> TreeModel:
        return self._tree_model

    @Property(list, constant=True)
    def functionDatabase(self) -> list:
        return FunctionDatabase.function_database

    @Property(QObject, constant=True)
    def imageGridModel(self) -> ImageTableModel:
        return self._image_grid_model

    @Property(str, notify=augmentationStringChanged)
    def augmentationString(self) -> str:
        return self._augmentationString

    @augmentationString.setter
    def augmentationString(self, value):
        if self._augmentationString != value:
            self._augmentationString = value
            self.augmentationStringChanged.emit()

    def _init_image_grid_model(self) -> ImageTableModel:
        return ImageTableModel([[np.zeros((500, 500), np.uint8) + 255 for _ in range(5)] for _ in range(5)])

    def _init_tree_model(self) -> TreeModel:
        tree_model = TreeModel()
        return tree_model


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    engine.addImportPath(str(Path(__file__).resolve().parent))
    engine.addImportPath(QCoreApplication.applicationDirPath() + "/qml")
    engine.addImportPath(QCoreApplication.applicationDirPath() + ":/content")
    engine.addImportPath(":/")

    content_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'content')
    imports_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'imports')

    engine.addImportPath(content_dir)
    engine.addImportPath(imports_dir)

    font_database = QFontDatabase()
    font_database.addApplicationFont(":/content/fonts/fonts.txt")

    backend_model = BackendModel()

    instantiated_function = backend_model.functionDatabase[0].get_function_model()

    engine.rootContext().setContextProperty("backendModel", backend_model)
    engine.rootContext().setContextProperty("functionModel", instantiated_function)
    engine.rootContext().setContextProperty("imageTableModel", backend_model.imageGridModel)

    engine.addImageProvider("image_provider", backend_model.imageGridModel._image_provider)

    qml_file = Path(__file__).resolve().parent / "main.qml"
    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
