# Linux
docker run -it --name myapp --rm --volume $(pwd):/usr/src/app --net=host mypython-dev:latest sh

# Powershell
docker run -it --name myapp --rm --volume ${pwd}:/usr/src/app --net=host mypython-dev:latest sh