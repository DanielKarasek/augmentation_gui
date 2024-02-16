from typing import Tuple, Union

from PySide6.QtCore import QObject, Property

from typedefs import Number
from parameter_models.number_parameter import NumberParameter
from parameter_models.parameter_interface import Parameter


class StringDescription(QObject):
    def __init__(self, description: str):
        super().__init__()
        self._description = description

    @Property(str, constant=True)
    def description(self) -> str:
        return self._description

    @Property(str, constant=True)
    def type(self) -> str:
        return "description"

    def __repr__(self):
        return f"StringDescriptionDescription({self._description})"

    def __str__(self):
        return self.__repr__()

    def to_dict(self) -> dict:
        return {"type": self.type,
                "state": {"description": self._description}}

    @staticmethod
    def from_dict(d: dict) -> 'StringDescription':
        description = d["description"]
        me = StringDescription(description)
        return me


class TupleParameter(Parameter):
    def __init__(self, name: str, parameter_name: str, fields_tuple: Tuple[Union[NumberParameter, StringDescription], ...], **kwargs):
        super().__init__(name, parameter_name, **kwargs)
        self._fields_tuple = fields_tuple

    def __repr__(self):
        return f"TupleParameter({self._name}, {self.value})"

    def __str__(self):
        return self.__repr__()

    def state2dict(self) -> dict:
        return {"fields": [field.to_dict() for field in self._fields_tuple]}

    @staticmethod
    def from_dict(d: dict) -> 'TupleParameter':
        fields = d["fields"]
        fields_tuple = []
        for field in fields:
            if field["type"] == "description":
                fields_tuple.append(StringDescription.from_dict(field["state"]))
            else:
                fields_tuple.append(Parameter.from_dict(field))

        name = d["name"]
        parameter_name = d["parameter_name"]
        me = TupleParameter(name, parameter_name, tuple(fields_tuple))
        return me

    @property
    def value(self) -> Tuple[Union[Number, str], ...]:
        return tuple(field.value for field in self._fields_tuple if isinstance(field, NumberParameter))

    @Property('QVariantList', constant=True)
    def items(self):
        return list(self._fields_tuple)
