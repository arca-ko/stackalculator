To run the application, it is recommended to use a Linux-based distribution either in a virtual machine (VM) or on bare-metal. If you are using a Windows machine, you have two options:

1. Follow the instructions under the **For Windows users (no WSL)** section.
2. Install the WSL (Windows Subsystem for Linux) to run the application.


***How to run the application***
`docker compose up -d`

*Note: If you are using Linux or macOS, you might need to use `sudo` before the command.*


***Image Options***
- The recommended image is:
`docker pull arcak0/restapi_mysql:1.0-alpine`

- An alternative is the *ubuntu:mantic* based image:
`docker pull arcak0/restapi_mysql:1.0`


***For Windows users (no WSL)***
In case you are on Windows and don't have the WSL installed you can do the following:
1. Edit the provided Dockerfile: replace `python:alpine` with `python:3` for the image.
2. Uncomment the `build` line under the *app service* in the docker-compose file.
3. Comment out the `image` line ...
