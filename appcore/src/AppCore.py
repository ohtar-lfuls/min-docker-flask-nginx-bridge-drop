from flask_restful import Resource

from abc import ABC, abstractmethod

from .util.ResponseType import ResponseType

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


class SayHello(Resource, AppCoreProtocol):
    type = "string"
    arg = "name"
    def get(self, name:str):
        return ResponseType.text(f'Hello! {name}')
