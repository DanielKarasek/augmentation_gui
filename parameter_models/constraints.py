from typing import Union, Type

from PySide6.QtCore import QObject, Property

from typedefs import Number


class Constraints(QObject):
    def __init__(self,
                 min_value: Number,
                 max_value: Number,
                 step: Number,
                 data_type: Union[Type[int], Type[float]]):
        super().__init__()
        self._min_value = min_value
        self._max_value = max_value
        self._step_size = step
        self._data_type = data_type

    @Property(float, constant=True)
    def min_value(self):
        return self._min_value

    @Property(float, constant=True)
    def max_value(self):
        return self._max_value

    @Property(float, constant=True)
    def step_size(self):
        return self._step_size

    @Property(str, constant=True)
    def data_type(self):
        return self._data_type.__name__

    def check(self, new_value: Number):
        if new_value < self._min_value or new_value > self._max_value:
            return False
        return True

    def __repr__(self):
        return (f"Constraints({self._min_value}, "
                f"{self._max_value}, {self._step_size}, {self._data_type})")

    def __str__(self):
        return self.__repr__()
