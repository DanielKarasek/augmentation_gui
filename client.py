import logging
import socket
import time

import cv2
import numpy as np

from ai_core.data_structure.annotation_general import AnnotationGeneral
from ai_core.data_structure.colours.colours_palette import ColoursPalette
from ai_core.data_structure.coordinates.detection_general import DetectionGeneral
from ai_core.data_structure.coordinates.keypoint_general import KeypointGeneral
from ai_core.data_structure.coordinates.point import Point
from ai_core.data_structure.data_collections.base_collection import BaseCollection
from ai_core.data_structure.data_collections.base_prop import UnknownProp
from ai_core.data_structure.image_data import ImageData
from projects_src.augmentation_gui.service.socket_utils import send_annotation_with_data, recv_annotation_with_data


class SocketClosedError(Exception):
    pass


def recv_n_bytes(sock: socket.socket, n: int) -> bytes:
    buffer = b''
    while len(buffer) < n:
        data = sock.recv(n - len(buffer))
        if not data:
            raise SocketClosedError('Socket closed while reading data')
        buffer += data
    return buffer


def recv_image(sock: socket.socket) -> np.ndarray:
    # TODO: add support for error handling
    # TODO: add different image dtypes
    im_size_bytes = recv_n_bytes(sock, n=5)
    im_size = int.from_bytes(im_size_bytes[0:2]), int.from_bytes(im_size_bytes[2:4]), im_size_bytes[4]

    image_buffer = recv_n_bytes(sock, n=im_size[0] * im_size[1] * im_size[2])
    image = np.frombuffer(image_buffer, dtype=np.uint8).reshape(im_size[0], im_size[1], im_size[2])
    return image


def send_image(sock: socket.socket, image: np.ndarray):
    shape_encoded = image.shape[0].to_bytes(2) + image.shape[1].to_bytes(2) + image.shape[2].to_bytes(1)
    sock.sendall(shape_encoded)
    sock.sendall(image)


def is_socket_closed(sock: socket.socket) -> bool:
    try:
        # this will try to read bytes without blocking and also without removing them from buffer (peek only)
        data = sock.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
        if len(data) == 0:
            return True
    except BlockingIOError:
        return False  # socket is open and reading from it would block
    except ConnectionResetError:
        return True  # socket was closed for some other reason
    except Exception as e:
        return False


class ImageAugmentServiceAdapter:
    def __init__(self, port: int = 10014):
        self._logger = logging.getLogger('ImageAugmentServiceAdapter')
        self._port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.try_connect()

    def try_connect(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            self._logger.info(f"Trying to connect to port {self._port}")
            try:
                self._sock.connect(('localhost', self._port))
                return
            except ConnectionRefusedError:
                self._logger.info(f"Connection refused on port {self._port} waiting for server to start")
                time.sleep(0.5)

    def augment_image(self, annot: AnnotationGeneral) -> AnnotationGeneral:
        while True:
            if is_socket_closed(self._sock):
                self.try_connect()
            send_annotation_with_data(self._sock, annot)
            try:
                new_annot = recv_annotation_with_data(self._sock)
                new_dets = [new_det.change_cls(old_det.cls_obj) for new_det, old_det in zip(new_annot.dets, annot.dets)]
                new_annot.set_dets(new_dets)
                new_annot._collection = annot.collection
                return new_annot
            except SocketClosedError:
                self._logger.info("Socket closed while reading data")


if __name__ == "__main__":
    augmenter = ImageAugmentServiceAdapter()
    image = np.zeros((500, 500, 3), np.uint8) + 255
    kp = KeypointGeneral(Point(100, 100), UnknownProp(-1, 0.0, ColoursPalette.black_colour()))
    det = DetectionGeneral(kp, UnknownProp(-1, 0.0, ColoursPalette.black_colour()))
    annot = AnnotationGeneral(ImageData.from_numpy(image), BaseCollection(), [det])
    annot = augmenter.augment_image(annot)
    cv2.imshow("image", annot.img_data.data)
    print(annot.dets)
    cv2.waitKey(0)
