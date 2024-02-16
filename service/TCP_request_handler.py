from __future__ import annotations

import logging
import socket
import socketserver
import time
from select import select
from typing import TYPE_CHECKING

from ai_core.data_structure.annotation_general import AnnotationGeneral
from ai_core.data_structure.colours.colours_palette import ColoursPalette
from ai_core.data_structure.coordinates.detection_general import DetectionGeneral
from ai_core.data_structure.coordinates.keypoint_general import KeypointGeneral
from ai_core.data_structure.coordinates.point import Point
from ai_core.data_structure.data_collections.base_collection import BaseCollection
from ai_core.data_structure.data_collections.base_prop import UnknownProp
from ai_core.data_structure.image_data import ImageData
from projects_src.augmentation_gui.service.exceptions import SocketClosedError
from projects_src.augmentation_gui.service.socket_utils import recv_annotation_with_data, \
    send_annotation_with_data
from projects_src.augmentation_gui.service.utils import keypoints2imgaug

if TYPE_CHECKING:
    from projects_src.augmentation_gui.service.TCP_server import TCPServer


class TCPRequestHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def __init__(self,
                 request: socket.socket,
                 client_address: tuple[str, int],
                 server: TCPServer):
        self._pipeline = server.pipeline
        self._logger = logging.getLogger('TCPRequestHandler')
        self._logger.debug('TCPRequestHandler object created')
        super().__init__(request, client_address, server)

    def setup(self):
        self._logger.info('{}:{} connected'.format(*self.client_address))

    def handle(self):
        # SPEED testing 1920x1080x3 uint8 = 0.004 seconds = 250 fps
        # SPEED testing 4000x2000x3 uint8 = 0.03 seconds = 33 fps
        while True:
            time_start = time.time()
            data = self.request.recv(1, socket.MSG_PEEK)
            if not data:
                break

            annotation = recv_annotation_with_data(self.request)
            image = annotation.img_data.data
            dets = annotation.dets
            # TODO: fix so it works for any type of detection
            # TODO: factor out all annotation stuff -> imgaug -> annotation stuff
            kps: list[KeypointGeneral] = [det.shape for det in dets]
            imgaug_kps = keypoints2imgaug(kps, image.shape)
            image, kps_aug = self._pipeline.augment(image=image, keypoints=imgaug_kps)
            prop = UnknownProp(-1, 0.0, ColoursPalette.black_colour())
            kps_aug = [kp for kp in kps_aug if 0 <= kp.x <= image.shape[1] and 0 <= kp.y <= image.shape[0]]
            kps = [KeypointGeneral(Point(kp_aug.x, kp_aug.y), prop) for kp_aug in kps_aug]
            dets = [DetectionGeneral(kp, prop) for kp in kps]
            annotation = AnnotationGeneral(ImageData.from_numpy(image), BaseCollection(), dets)

            if self.is_connection_closed():
                raise SocketClosedError('Socket closed while sending data')
            send_annotation_with_data(self.request, annotation)
            time_end = time.time()
            self._logger.debug(f'Image processed in {time_end - time_start:.6f} seconds')

    def is_connection_closed(self) -> bool:
        r, _, _ = select([self.request], [], [], 0)
        if r:
            data = self.request.recv(1, socket.MSG_PEEK)
            return not data

    def finish(self):
        self._logger.info('{}:{} disconnected'.format(*self.client_address))
