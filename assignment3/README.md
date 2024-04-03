# Assignment 3 - Docker Containers

This directory contains Dockerized implementations of three spaCy-based NER/dependency parsing applications

1. A RESTful API
2. A streamlit server
3. A Flask server/frontend connected to a(n) SQLAlchemy database

## Requirements
- Docker >= 24.0.2
- Python >= 3.10.12

## Quick Start

To spin up all containers at once for immediate access, run the following command from the root (/assignment3) directory:

```
docker compose up
```

This will launch all containers: they will be accessible at the following routes/URLs:

1. FastAPI:     [localhost:8000](localhost:8000)
2. Streamlit:   [localhost:8501](localhost:8501)
3. Flask:       [localhost:5555](localhost:5555)

For information on starting up individual containers or further information on the containerized services, continue reading.

## Building an individual container

Each application also has a Containerfile for individual access. To build a specific container, **make sure you are in the root directory (/assignment3)** [^1]. Then, run the one of the following commands to build the corresponding app:

**FastAPI**
```
docker build . -f fastapi/Containerfile -t app-fastapi
```

**Streamlit**
```
docker build . -f streamlit/Containerfile -t app-streamlit
```

**Flask**
```
docker build . -f flask/Containerfile -t app-flask
```

For more information about the functionality of each app, see `/assignment1/README.md` for FastAPI and Streamlit, and `/assignment2/README.md` for Flask.

[^1]: This is necessary to avoid redundancy, since all three files reference functions defined in `ner.py`. Rather than copy this file to each directory, the containers can all access the same file by using the parent context. 

## Running an individual container

Then, to run an individual container, from any directory:

**FastAPI**: `docker run -p 8000:8000 app-fastapi`


**Streamlit**: `docker run -p 8501:8501 app-streamlit`

**Flask**: `docker run -p 5555:5555 app-flask`


## A note on hard drive usage

Because each container may be run separately, each one must be able to install dependencies individually from their respective requirements. Because all the containers perform similar tasks and share mostly identical dependencies, this will produce larger than necessary Docker images if all three containers are built individually.

The `docker-compose.yml` addresses this limitation by building a fourth, base container in the /base directory. This installs the dependencies needed for all applications in a single base image, which is then built from for all subsequent containers. This approach ensures that the shared dependencies will only be installed once across all applications.

If you would like to save storage space when building containers individually, this can be achieved using the same technique (from the root /assignment3):

1. Build the base image: `docker build . -f base/Containerfile -t base-image`
2. When building an application that you would like to use this shared pip-install image, pass in the image name as a build-arg: 
    ```
    docker build . --build-arg BASE_IMAGE=base-image -f <containerfile route> -t <app name>
    ```
3. Run the container as usual.