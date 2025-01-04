from flask import Flask
from flask_restful import Api

from .AppCore import *

app = Flask(__name__)
api = Api(app)

def add_resource(c):
    # /AppCore/ClassName/<string:name>
    api.add_resource(c, f'/AppCore/{c.__name__}/<{c.type}:{c.arg}>')


add_resource(SayHello)