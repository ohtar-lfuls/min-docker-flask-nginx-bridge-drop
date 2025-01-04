from flask import Flask
from flask_restful import Api

import inspect

from .AppCore import AppCore

app = Flask(__name__)
api = Api(app)

def add_resource(c):
    # /AppCore/ClassName/<string:name>
    api.add_resource(c, f'/AppCore/{c.__name__}/<{c.type}:{c.arg}>')


# AppCoreモジュール内のすべてのクラスをリスト化
classes = [cls for name, cls in inspect.getmembers(AppCore, inspect.isclass) if name != "__class__"]

for cls in classes:
    # print(cls.__name__)
    add_resource(cls)



