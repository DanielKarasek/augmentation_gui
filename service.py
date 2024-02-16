from __future__ import annotations

import argparse
import logging
import sys

from service.TCP_request_handler import TCPRequestHandler
from service.TCP_server import TCPServer
from service.exceptions import PortInUseError
from service.socket_utils import is_port_in_use
from service.utils import load_pipeline

# TODO: possibly add workers, but beware of having workers both on client and server side as it could
#  lead to a lot of overhead
parser = argparse.ArgumentParser(
    prog='Augmentation Service',
    description='This is a service using imgaug to augment images. '
                'It listens for images and sends back augmented images according to provided pipeline. ',
    epilog='Thx for using our service <3')
parser.add_argument('--port', type=int, default=10014, help='Port to bind the service to')
parser.add_argument('--pipeline', type=str, default='test.json', help='Path to the pipeline file')


def setup_loggers():
    server_logger = logging.getLogger('TCPServer')
    server_logger.setLevel(logging.DEBUG)
    handler_logger = logging.getLogger('TCPRequestHandler')
    handler_logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    server_logger.addHandler(console_handler)
    handler_logger.addHandler(console_handler)


def main():
    args = parser.parse_args()

    HOST, PORT = "localhost", args.port
    pipeline = load_pipeline(args.pipeline)

    setup_loggers()

    if is_port_in_use(args.port):
        raise PortInUseError("Port is already in use, please choose another one."
                             " You can choose 0 for automatic port selection and the choice will be printed to console.")

    with TCPServer((HOST, PORT), pipeline, TCPRequestHandler) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()
