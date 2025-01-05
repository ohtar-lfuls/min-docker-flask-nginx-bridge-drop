# System Configuration Diagram

<span style="display:block;text-align:center">![System Configuration Diagram](doc/System_configuration_diagram.png)

# Environmental setup

## Install Docker
See: [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)



## Add User to docker group
```bash
cat /etc/group | grep docker
# docker:x:***:

sudo usermod -aG docker $USER

cat /etc/group | grep docker
# docker:x:***:<username>
```

## Run docker without root permission
```bash
docker run hello-world
# Hello from Docker!
```

# Run App
```bash
docker compose up --build
```

## Check flask api return
Open [http://localhost:8080/AppCore/SayHello/\<string\>](http://localhost:8080/AppCore/SayHello/<string>) in your browser to execute sayhello


## Access from external device on your network
* [Windows](Scripts/win/README.md)
