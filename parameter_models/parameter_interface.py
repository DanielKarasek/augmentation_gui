import abc

from PySide6.QtCore import QObject, Property


class ABCQObjectMeta(abc.ABCMeta, type(QObject)):
    pass


class Parameter(QObject, metaclass=ABCQObjectMeta):

    def __init__(self, name: str, parameter_name: str, **kwargs):
        super().__init__()
        self._name = name
        self._parameter_name = parameter_name

    def to_dict(self) -> dict:
        return {"type": self.type,
                "state": {"name": self._name,
                          "parameter_name": self._parameter_name,
                          **self.state2dict()
                          }
                }

    @abc.abstractmethod
    def state2dict(self) -> dict:
        return {}

    @staticmethod
    def from_dict(d: dict) -> 'Parameter':
        parameter_type = d["type"]
        if parameter_type == "numberparameter":
            from parameter_models.number_parameter import NumberParameter
            return NumberParameter.from_dict(d["state"])
        elif parameter_type == "booleanparameter":
            from parameter_models.boolean_parameter import BooleanParameter
            return BooleanParameter.from_dict(d["state"])
        elif parameter_type == "tupleparameter":
            from parameter_models.tuple_parameter import TupleParameter
            return TupleParameter.from_dict(d["state"])
        else:
            raise ValueError(f"Unknown parameter type: {parameter_type}")

    @Property(str, constant=True)
    def name(self):
        return self._name

    @Property(str, constant=True)
    def parameter_name(self):
        return self._parameter_name

    @abc.abstractmethod
    def value(self):
        pass

    @Property(str, constant=True)
    def type(self):
        return self.__class__.__name__.lower()

    def deepcopy(self) -> 'Parameter':
        return Parameter.from_dict(self.to_dict())
