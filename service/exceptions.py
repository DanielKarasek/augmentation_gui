from __future__ import annotations


class SocketClosedError(Exception):
    pass


class PipelineFileError(Exception):
    pass


class PortInUseError(Exception):
    pass
