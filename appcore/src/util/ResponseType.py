from flask import make_response

class ResponseType:
    def __new__(cls, *args, **kwargs):
        # Do not allow generating class instance.
        raise TypeError(f"Cannot instantiate class {cls.__name__}")
    
    @staticmethod
    def text(text:str):
        res = make_response(text)
        res.headers["Content-Type"] = "text/plain; charset=utf-8"
        return res