from flask import Flask
from flask_restful import Api

import inspect

from .AppCore import AppCore

app = Flask(__name__)
api = Api(app)

def add_resource(module_name:str, c):
    # /AppCore/ClassName/<string:name>
    api.add_resource(c, f'/{module_name}/{c.__name__}/<{c.type}:{c.arg}>')

def add_resources(module):
    classes = [cls for name, cls in inspect.getmembers(AppCore, inspect.isclass) if name != "__class__"]

    for cls in classes:
        add_resource(module.__name__, cls)

add_resources(AppCore)




