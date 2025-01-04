import requests

url = 'http://localhost:8080/AppCore'

def sayHello(name:str) -> str:
    response = requests.get(f"{url}/sayhello/{name}")
    return response.text

if __name__ == "__main__":
    name = "MyName"
    print(sayHello(name))