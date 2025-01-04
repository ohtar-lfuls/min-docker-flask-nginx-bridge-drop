from flask import Flask, make_response
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class SayHello(Resource):
    def get(self, name:str):
        response = make_response(f'Hello! {name}')
        response.headers["Content-Type"] = "text/plain; charset=utf-8"
        return response

api.add_resource(SayHello, '/AppCore/sayhello/<string:name>')





