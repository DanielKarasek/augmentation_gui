from PySide6.QtCore import Signal, Property

from typedefs import Number
from parameter_models.constraints import Constraints
from parameter_models.parameter_interface import Parameter


class NumberParameter(Parameter):
    valueChanged = Signal()

    def __init__(self,
                 name: str,
                 parameter_name: str,
                 default_value: Number,
                 constraints: Constraints,
                 **kwargs):
        super().__init__(name, parameter_name, **kwargs)
        self._value = default_value
        self._constraints = constraints

    def state2dict(self) -> dict:
        return {"value": self._value,
                "constraints": self._constraints.to_dict()}

    @staticmethod
    def from_dict(d: dict) -> 'NumberParameter':
        value = d["value"]
        constraints = Constraints.from_dict(d["constraints"])
        name = d["name"]
        parameter_name = d["parameter_name"]
        me = NumberParameter(name, parameter_name, value, constraints)
        return me

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
            # TODO move this to constraints? e.g. fit to constraints method
            if self._constraints.data_type == 'int':
                new_value = int(new_value)
            self._value = new_value
            self.valueChanged.emit()

    @Property(Constraints, constant=True)
    def constraints(self) -> Constraints:
        return self._constraints
