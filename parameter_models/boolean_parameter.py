from PySide6.QtCore import Signal, Property

from parameter_models.parameter_interface import Parameter


class BooleanParameter(Parameter):
    valueChanged = Signal()

    def __init__(self, name: str, default_value: bool, **kwargs):
        super().__init__(name, **kwargs)
        self._value = default_value

    def __repr__(self) -> str:
        return f"BooleanParameter({self._name}, {self._value})"

    def __str__(self) -> str:
        return self.__repr__()

    @Property(bool, notify=valueChanged)
    def value(self) -> bool:
        return self._value

    @value.setter
    def value(self, new_value: bool):
        self._value = new_value
        self.valueChanged.emit()
