import requests

class ApiWrapper:
    def __init__(self, url, name):
        self.module_name = name
        self.url = url
    
    def get(self, func_name:str, arg:str):
        return requests.get(f"{self.url}/{self.module_name}/{func_name}/{arg}").text
        


if __name__ == "__main__":
    app_core = ApiWrapper("http://localhost:8080", "AppCore")
    
    print(app_core.get("Test", "MyName"))


