# docker-python-demo

## Synopsis

This [senzing/python-demo](https://hub.docker.com/r/senzing/python-demo)
docker image demonstrates how to write a Flask app based on the
[senzing/senzingapi-runtime](https://hub.docker.com/r/senzing/senzingapi-runtime) docker image.

## Overview

### Related artifacts

1. [DockerHub](https://hub.docker.com/r/senzing/python-demo)

### Contents

1. [Demonstrate using Docker](#demonstrate-using-docker)
    1. [Set environment variables](#set-environment-variables)
    1. [Run docker container](#run-docker-container)
1. [Demonstrate using docker-compose](#demonstrate-using-docker-compose)
    1. [Create directories for artifacts](#create-directories-for-artifacts)
    1. [Prerequisite docker-compose stack](#prerequisite-docker-compose-stack)
    1. [Bring up docker-compose stack](#bring-up-docker-compose-stack)
1. [Develop](#develop)
    1. [Prerequisite software](#prerequisite-software)
    1. [Clone repository](#clone-repository)
    1. [Build docker image for development](#build-docker-image-for-development)
1. [Advanced](#advanced)
    1. [Configuration](#configuration)
1. [Examples](#examples)
1. [Errors](#errors)
1. [References](#references)

### Legend

1. :thinking: - A "thinker" icon means that a little extra thinking may be required.
   Perhaps you'll need to make some choices.
   Perhaps it's an optional step.
1. :pencil2: - A "pencil" icon means that the instructions may need modification before performing.
1. :warning: - A "warning" icon means that something tricky is happening, so pay attention.

### Expectations

- **Space:** This repository and demonstration require 6 GB free disk space.
- **Time:** Budget 40 minutes to get the demonstration up-and-running, depending on CPU and network speeds.
- **Background knowledge:** This repository assumes a working knowledge of:
  - [Docker](https://github.com/Senzing/knowledge-base/blob/main/WHATIS/docker.md)

## Demonstrate using Docker

### Set environment variables

1. Construct Senzing SQL Connection.
   Example:

    ```console
    export SENZING_SQL_CONNECTION="postgresql://username:password@hostname:5432:G2/"
    ```

### Run docker container

1. Run docker container.
   Example:

    ```console
    sudo docker run \
      --env SENZING_SQL_CONNECTION \
      --interactive \
      --publish 8356:5000 \
      --rm \
      --tty \
      senzing/python-demo
    ```

1. The running app is viewable at [localhost:8356](http://localhost:8256).

## Demonstrate using docker-compose

### Create directories for artifacts

1. Specify a new directory to place artifacts in.
   Example:

    ```console
    export SENZING_VOLUME=~/my-senzing
    ```

1. Create directories.
   Example:

    ```console
    export PGADMIN_DIR=${SENZING_VOLUME}/pgadmin
    export POSTGRES_DIR=${SENZING_VOLUME}/postgres
    export RABBITMQ_DIR=${SENZING_VOLUME}/rabbitmq
    export SENZING_UID=$(id -u)
    export SENZING_GID=$(id -g)
    mkdir -p ${PGADMIN_DIR} ${POSTGRES_DIR} ${RABBITMQ_DIR}
    chmod -R 777 ${SENZING_VOLUME}
    ```

### Prerequisite docker-compose stack

1. Bring up a Docker Compose stack with backing services.
   Example:

    ```console
    wget \
      -O ${SENZING_VOLUME}/docker-compose-backing-services-only.yaml \
      "https://raw.githubusercontent.com/Senzing/docker-compose-demo/main/resources/postgresql/docker-compose-rabbitmq-postgresql-backing-services-only.yaml"

    docker-compose -f ${SENZING_VOLUME}/docker-compose-backing-services-only.yaml pull
    docker-compose -f ${SENZING_VOLUME}/docker-compose-backing-services-only.yaml up
    ```

### Bring up docker-compose stack

1. Download `docker-compose.yaml` file and deploy stack.
   Example:

    ```console
    wget \
      -O ${SENZING_VOLUME}/docker-compose.yaml \
      "https://raw.githubusercontent.com/Senzing/docker-python-demo/main/docker-compose.yaml"

    docker-compose -f ${SENZING_VOLUME}/docker-compose.yaml pull
    docker-compose -f ${SENZING_VOLUME}/docker-compose.yaml up
    ```

## Develop

### Prerequisite software

The following software programs need to be installed:

1. [git](https://github.com/Senzing/knowledge-base/blob/main/HOWTO/install-git.md)
1. [make](https://github.com/Senzing/knowledge-base/blob/main/HOWTO/install-make.md)
1. [docker](https://github.com/Senzing/knowledge-base/blob/main/HOWTO/install-docker.md)

### Clone repository

For more information on environment variables,
see [Environment Variables](https://github.com/Senzing/knowledge-base/blob/main/lists/environment-variables.md).

1. Set these environment variable values:

    ```console
    export GIT_ACCOUNT=senzing
    export GIT_REPOSITORY=docker-python-demo
    export GIT_ACCOUNT_DIR=~/${GIT_ACCOUNT}.git
    export GIT_REPOSITORY_DIR="${GIT_ACCOUNT_DIR}/${GIT_REPOSITORY}"
    ```

1. Follow steps in [clone-repository](https://github.com/Senzing/knowledge-base/blob/main/HOWTO/clone-repository.md) to install the Git repository.

### Build docker image for development

1. **Option #1:** Using `docker` command and GitHub.

    ```console
    sudo docker build --tag senzing/python-demo https://github.com/senzing/docker-python-demo.git#main
    ```

1. **Option #2:** Using `docker` command and local repository.

    ```console
    cd ${GIT_REPOSITORY_DIR}
    sudo docker build --tag senzing/python-demo .
    ```

1. **Option #3:** Using `make` command.

    ```console
    cd ${GIT_REPOSITORY_DIR}
    sudo make docker-build
    ```

    Note: `sudo make docker-build-development-cache` can be used to create cached docker layers.

## Examples

## Advanced

### Configuration

Configuration values specified by environment variable or command line parameter.

- **[SENZING_DEBUG](https://github.com/Senzing/knowledge-base/blob/main/lists/environment-variables.md#senzing_debug)**
- **[SENZING_NETWORK](https://github.com/Senzing/knowledge-base/blob/main/lists/environment-variables.md#senzing_network)**
- **[SENZING_RUNAS_USER](https://github.com/Senzing/knowledge-base/blob/main/lists/environment-variables.md#senzing_runas_user)**

## Errors

1. See [docs/errors.md](docs/errors.md).

## References
