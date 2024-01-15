import abc

from PySide6.QtCore import QObject, Property


class ABCQObjectMeta(abc.ABCMeta, type(QObject)):
    pass


class Parameter(QObject, metaclass=ABCQObjectMeta):

    def __init__(self, name: str, **kwargs):
        super().__init__()
        self._name = name

    @Property(str, constant=True)
    def name(self):
        return self._name

    @abc.abstractmethod
    def value(self):
        pass

    @Property(str, constant=True)
    def type(self):
        return self.__class__.__name__.lower()
