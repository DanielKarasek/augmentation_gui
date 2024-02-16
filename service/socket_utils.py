from __future__ import annotations

import socket

import numpy as np

from ai_core.data_structure.annotation_general import AnnotationGeneral
from ai_core.data_structure.colours.colours_palette import ColoursPalette
from ai_core.data_structure.coordinates.detection_general import DetectionGeneral
from ai_core.data_structure.coordinates.keypoint_general import KeypointGeneral
from ai_core.data_structure.coordinates.point import Point
from ai_core.data_structure.data_collections.base_collection import BaseCollection
from ai_core.data_structure.data_collections.base_prop import UnknownProp
from ai_core.data_structure.image_data import ImageData
from projects_src.augmentation_gui.service.exceptions import SocketClosedError
from projects_src.augmentation_gui.service.utils import dtype2int, int2dtype_and_type_size


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
    im_type = int.from_bytes(recv_n_bytes(sock, 1), 'big')
    im_type, type_size = int2dtype_and_type_size(im_type)

    image_buffer = recv_n_bytes(sock, n=im_size[0] * im_size[1] * im_size[2] * type_size)
    image = np.frombuffer(image_buffer, dtype=im_type).reshape(im_size[0], im_size[1], im_size[2])
    return image


def send_image(sock: socket.socket, image: np.ndarray):
    shape_encoded = image.shape[0].to_bytes(2) + image.shape[1].to_bytes(2) + image.shape[2].to_bytes(1)
    type_encoded = dtype2int(image.dtype).to_bytes(1, 'big')
    sock.sendall(shape_encoded)
    sock.sendall(type_encoded)
    sock.sendall(image)


def send_detections(sock: socket.socket, dets: list[DetectionGeneral]):
    # TODO: support more than one detection dtype (keypoint)
    dets = list(filter(lambda det: isinstance(det.shape, KeypointGeneral), dets))
    kps = [det.shape for det in dets]
    kps_len = len(kps).to_bytes(2, 'big')
    sock.sendall(kps_len)
    for kp in kps:
        kp: KeypointGeneral
        x_bytes, y_bytes = (int(kp.center_point.x).to_bytes(2, 'big'),
                            int(kp.center_point.y).to_bytes(2, 'big'))
        sock.sendall(x_bytes)
        sock.sendall(y_bytes)


def recv_detections(sock: socket.socket) -> list[DetectionGeneral]:
    # TODO: add support for more than one detection dtype (keypoint)
    kps_len_bytes = recv_n_bytes(sock, 2)
    kps_len = int.from_bytes(kps_len_bytes, 'big')
    dets = []
    bytes_coords = recv_n_bytes(sock, 4 * kps_len)
    for i in range(0, len(bytes_coords), 4):
        x = int.from_bytes(bytes_coords[i:i + 2], 'big')
        y = int.from_bytes(bytes_coords[i + 2:i + 4], 'big')
        prop = UnknownProp(-1, 0.0, ColoursPalette.black_colour())
        kp = KeypointGeneral(Point(x, y), prop)
        dets.append(DetectionGeneral(kp, prop))
    return dets


def send_annotation_with_data(sock: socket.socket, annot: AnnotationGeneral):
    send_image(sock, annot.img_data.data)
    send_detections(sock, annot.dets)


def recv_annotation_with_data(sock: socket.socket) -> AnnotationGeneral:
    image = recv_image(sock)
    dets = recv_detections(sock)
    image_data = ImageData.from_numpy(image)
    annot = AnnotationGeneral(image_data, BaseCollection(), dets)
    return annot


def is_port_in_use(port: int) -> bool:
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0
