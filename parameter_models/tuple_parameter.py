from typing import Tuple, Union

from PySide6.QtCore import QObject, Property

from typedefs import Number
from parameter_models.number_parameter import NumberParameter
from parameter_models.parameter_interface import Parameter


class StringDescription(QObject):
    def __init__(self, description: str):
        super().__init__()
        self._description = description

    def __repr__(self):
        return f"StringDescriptionDescription({self._description})"

    def __str__(self):
        return self.__repr__()

    @Property(str, constant=True)
    def description(self) -> str:
        return self._description

    @Property(str, constant=True)
    def type(self) -> str:
        return "description"


class TupleParameter(Parameter):
    def __init__(self, name: str, fields_tuple: Tuple[Union[NumberParameter, StringDescription], ...], **kwargs):
        super().__init__(name, **kwargs)
        self._fields_tuple = fields_tuple

    def __repr__(self):
        return f"TupleParameter({self._name}, {self.value})"

    def __str__(self):
        return self.__repr__()

    @property
    def value(self) -> Tuple[Union[Number, str], ...]:
        return tuple(field.value for field in self._fields_tuple if isinstance(field, NumberParameter))

    @Property('QVariantList', constant=True)
    def items(self):
        return list(self._fields_tuple)
