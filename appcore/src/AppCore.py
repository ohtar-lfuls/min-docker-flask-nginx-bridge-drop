from flask_restful import Resource

from .util.ResponseType import ResponseType
from .util.AppCoreProtocol import AppCoreProtocol

class AppCore:
    class SayHello(Resource, AppCoreProtocol):
        type = "string"
        arg = "name"
        def get(self, name:str):
            return ResponseType.text(f'Hello! {name}')
    