from abc import ABC, abstractmethod

class AppCoreProtocol(ABC):
    @property
    @classmethod
    @abstractmethod
    def type(cls):
        pass

    @property
    @classmethod
    @abstractmethod
    def arg(cls):
        pass