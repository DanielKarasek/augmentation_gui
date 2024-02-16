from PySide6.QtCore import Signal, Property

from parameter_models.parameter_interface import Parameter


class BooleanParameter(Parameter):
    valueChanged = Signal()

    def __init__(self, name: str, parameter_name: str, default_value: bool, **kwargs):
        super().__init__(name, parameter_name, **kwargs)
        self._value = default_value

    @Property(bool, notify=valueChanged)
    def value(self) -> bool:
        return self._value

    @value.setter
    def value(self, new_value: bool):
        self._value = new_value
        self.valueChanged.emit()

    def __repr__(self) -> str:
        return f"BooleanParameter({self._name}, {self._value})"

    def __str__(self) -> str:
        return self.__repr__()


    def state2dict(self) -> dict:
        return {"value": self._value}

    @staticmethod
    def from_dict(d: dict) -> 'BooleanParameter':
        value = d["value"]
        name = d["name"]
        parameter_name = d["parameter_name"]
        me = BooleanParameter(name, parameter_name, value)
        return me


