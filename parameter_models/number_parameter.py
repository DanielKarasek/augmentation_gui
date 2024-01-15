from PySide6.QtCore import Signal, Property

from typedefs import Number
from parameter_models.constraints import Constraints
from parameter_models.parameter_interface import Parameter


class NumberParameter(Parameter):

    def __init__(self,
                 name: str,
                 default_value: Number,
                 constraints: Constraints,
                 **kwargs):
        super().__init__(name, **kwargs)
        self._value = default_value
        self._constraints = constraints

    valueChanged = Signal()

    def __repr__(self):
        return (f"NumberParameter({self._name}, {self._value}, "
                f"{self._constraints})")

    def __str__(self):
        return self.__repr__()

    @Property(float, notify=valueChanged)
    def value(self) -> Number:
        return self._value

    @value.setter
    def value(self, new_value: Number):
        if self._constraints.check(new_value):
            print("Value changed")
            self._value = new_value
            self.valueChanged.emit()

    @Property(Constraints, constant=True)
    def constraints(self) -> Constraints:
        return self._constraints
