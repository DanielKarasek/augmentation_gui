from __future__ import annotations

import logging
import socketserver
from typing import Union, Type

from imgaug.augmenters import Augmenter

from projects_src.augmentation_gui.service.TCP_request_handler import TCPRequestHandler


class TCPServer(socketserver.TCPServer):

    def __init__(self,
                 server_address: tuple[Union[int, str], int],
                 pipeline: Augmenter,
                 handler_class: Type[TCPRequestHandler] = TCPRequestHandler):
        self._logger = logging.getLogger('TCPServer')
        self._logger.debug('TCPServer object created')
        self._logger.info(f"Server started on {server_address[0]}:{server_address[1]}")

        self._pipeline = pipeline

        socketserver.TCPServer.__init__(self, server_address, handler_class)

    def serve_forever(self):
        self._logger.debug('waiting for request')
        self._logger.info('Handling requests, press <Ctrl-C> to quit')
        while True:
            try:
                self.handle_request()
            except Exception as e:
                self._logger.error(f'Error while handling request: {e}')

    @property
    def pipeline(self):
        return self._pipeline
