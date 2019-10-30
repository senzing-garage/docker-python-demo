# docker-python-demo

## Overview

This [senzing/python-demo](https://cloud.docker.com/u/senzing/repository/docker/senzing/python-demo)
docker image demonstrates how to write an app based on the
[senzing/senzing-base](https://github.com/Senzing/docker-senzing-base) docker image.

To see a demonstration of this python demo in action, see
[github.com/senzing/docker-compose-mysql-demo](https://github.com/senzing/docker-compose-mysql-demo).

### Related artifacts

1. [DockerHub](https://hub.docker.com/r/senzing/python-demo)

### Contents

1. [Expectations](#expectations)
    1. [Space](#space)
    1. [Time](#time)
    1. [Background knowledge](#background-knowledge)
1. [Demonstrate using Docker](#demonstrate-using-docker)
    1. [Initialize Senzing](#initialize-senzing)
    1. [Configuration](#configuration)
    1. [Volumes](#volumes)
    1. [Docker network](#docker-network)
    1. [External database](#external-database)
    1. [Docker user](#docker-user)
    1. [Run docker container](#run-docker-container)
1. [Demonstrate using Command Line](#demonstrate-using-command-line)
    1. [Prerequisite software for command line demonstration](#prerequisite-software-for-command-line-demonstration)
    1. [Clone repository for command line demonstration](#clone-repository-for-command-line-demonstration)
    1. [Install](#install)
    1. [Run commands](#run-commands)
1. [Develop](#develop)
    1. [Prerequisite software](#prerequisite-software)
    1. [Clone repository](#clone-repository)
    1. [Build docker image for development](#build-docker-image-for-development)
1. [Examples](#examples)
1. [Errors](#errors)
1. [References](#references)

## Expectations

### Space

This repository and demonstration require 6 GB free disk space.

### Time

Budget 40 minutes to get the demonstration up-and-running, depending on CPU and network speeds.

### Background knowledge

This repository assumes a working knowledge of:

1. [Docker](https://github.com/Senzing/knowledge-base/blob/master/WHATIS/docker.md)

## Reconfigure directories

1. Move existing directories.
   Example:

    ```console
    sudo mv /opt/senzing/data/1.0.0 /opt/senzing/data-1.0
    sudo rmdir /opt/senzing/data/

    sudo mv /opt/senzing/g2         /opt/senzing/g2-1.12
    ```

1. Make SymLinks.
   Example:

    ```console
    cd /opt/senzing

    sudo ln -s data-1.0 data
    sudo ln -s g2-1.12  g2
    ```

## Demonstrate using Docker

### Initialize Senzing

1. If Senzing has not been initialized, visit
   "[How to initialize Senzing with Docker](https://github.com/Senzing/knowledge-base/blob/master/HOWTO/initialize-senzing-with-docker.md)".

### Configuration

Configuration values specified by environment variable or command line parameter.

- **[SENZING_DATA_VERSION_DIR](https://github.com/Senzing/knowledge-base/blob/master/lists/environment-variables.md#senzing_data_version_dir)**
- **[SENZING_DATABASE_URL](https://github.com/Senzing/knowledge-base/blob/master/lists/environment-variables.md#senzing_database_url)**
- **[SENZING_DEBUG](https://github.com/Senzing/knowledge-base/blob/master/lists/environment-variables.md#senzing_debug)**
- **[SENZING_ETC_DIR](https://github.com/Senzing/knowledge-base/blob/master/lists/environment-variables.md#senzing_etc_dir)**
- **[SENZING_G2_DIR](https://github.com/Senzing/knowledge-base/blob/master/lists/environment-variables.md#senzing_g2_dir)**
- **[SENZING_NETWORK](https://github.com/Senzing/knowledge-base/blob/master/lists/environment-variables.md#senzing_network)**
- **[SENZING_RUNAS_USER](https://github.com/Senzing/knowledge-base/blob/master/lists/environment-variables.md#senzing_runas_user)**
- **[SENZING_VAR_DIR](https://github.com/Senzing/knowledge-base/blob/master/lists/environment-variables.md#senzing_var_dir)**

### Volumes

The output of `yum install senzingapi` placed files in different directories.
Create a folder for each output directory.

1. :pencil2: Option #1.
   To mimic an actual RPM installation,
   identify directories for RPM output in this manner:

    ```console
    export SENZING_DATA_VERSION_DIR=/opt/senzing/data/1.0.0
    export SENZING_ETC_DIR=/etc/opt/senzing
    export SENZING_G2_DIR=/opt/senzing/g2
    export SENZING_VAR_DIR=/var/opt/senzing
    ```

1. :pencil2: Option #2.
   If Senzing directories were put in alternative directories,
   set environment variables to reflect where the directories were placed.
   Example:

    ```console
    export SENZING_VOLUME=/opt/my-senzing

    export SENZING_DATA_VERSION_DIR=${SENZING_VOLUME}/data/1.0.0
    export SENZING_ETC_DIR=${SENZING_VOLUME}/etc
    export SENZING_G2_DIR=${SENZING_VOLUME}/g2
    export SENZING_VAR_DIR=${SENZING_VOLUME}/var
    ```

1. :thinking: If internal database is used, permissions may need to be changed in `/var/opt/senzing`.
   Example:

    ```console
    sudo chown $(id -u):$(id -g) -R ${SENZING_VAR_DIR}
    ```

### Docker network

:thinking: **Optional:**  Use if docker container is part of a docker network.

1. List docker networks.
   Example:

    ```console
    sudo docker network ls
    ```

1. :pencil2: Specify docker network.
   Choose value from NAME column of `docker network ls`.
   Example:

    ```console
    export SENZING_NETWORK=*nameofthe_network*
    ```

1. Construct parameter for `docker run`.
   Example:

    ```console
    export SENZING_NETWORK_PARAMETER="--net ${SENZING_NETWORK}"
    ```

### External database

:thinking: **Optional:**  Use if storing data in an external database.

1. :pencil2: Specify database.
   Example:

    ```console
    export DATABASE_PROTOCOL=postgresql
    export DATABASE_USERNAME=postgres
    export DATABASE_PASSWORD=postgres
    export DATABASE_HOST=senzing-postgresql
    export DATABASE_PORT=5432
    export DATABASE_DATABASE=G2
    ```

1. Construct Database URL.
   Example:

    ```console
    export SENZING_DATABASE_URL="${DATABASE_PROTOCOL}://${DATABASE_USERNAME}:${DATABASE_PASSWORD}@${DATABASE_HOST}:${DATABASE_PORT}/${DATABASE_DATABASE}"
    ```

1. Construct parameter for `docker run`.
   Example:

    ```console
    export SENZING_DATABASE_URL_PARAMETER="--env SENZING_DATABASE_URL=${SENZING_DATABASE_URL}
    ```

### Docker user

:thinking: **Optional:**  The docker container runs as "USER 1001".
Use if a different userid is required.

1. :pencil2: Manually identify user.
   User "0" is root.
   Example:

    ```console
    export SENZING_RUNAS_USER="0"
    ```

   Another option, use current user.
   Example:

    ```console
    export SENZING_RUNAS_USER=$(id -u)
    ```

1. Construct parameter for `docker run`.
   Example:

    ```console
    export SENZING_RUNAS_USER_PARAMETER="--user ${SENZING_RUNAS_USER}"
    ```

### Run docker container

1. Run docker container.
   Example:

    ```console
    sudo docker run \
      ${SENZING_RUNAS_USER_PARAMETER} \
      ${SENZING_DATABASE_URL_PARAMETER} \
      ${SENZING_NETWORK_PARAMETER} \
      --interactive \
      --publish 5001:5000 \
      --rm \
      --tty \
      --volume ${SENZING_DATA_VERSION_DIR}:/opt/senzing/data \
      --volume ${SENZING_ETC_DIR}:/etc/opt/senzing \
      --volume ${SENZING_G2_DIR}:/opt/senzing/g2 \
      --volume ${SENZING_VAR_DIR}:/var/opt/senzing \
      senzing/python-demo
    ```

1. The running app is viewable at [localhost:5001](http://localhost:5001).

## Demonstrate using Command Line

### Prerequisite software for command line demonstration

The following software programs need to be installed:

1. [git](https://github.com/Senzing/knowledge-base/blob/master/HOWTO/install-git.md)
1. [senzingdata](https://github.com/Senzing/knowledge-base/blob/master/HOWTO/install-senzing-data.md)
1. [senzingapi](https://github.com/Senzing/knowledge-base/blob/master/HOWTO/install-senzing-api.md)

### Clone repository for command line demonstration

1. Set these environment variable values:

    ```console
    export GIT_ACCOUNT=docktermj
    export GIT_REPOSITORY=docker-python-demo
    export GIT_ACCOUNT_DIR=~/${GIT_ACCOUNT}.git
    export GIT_REPOSITORY_DIR="${GIT_ACCOUNT_DIR}/${GIT_REPOSITORY}"
    ```

1. Follow steps in [clone-repository](https://github.com/Senzing/knowledge-base/blob/master/HOWTO/clone-repository.md) to install the Git repository.

### Install

1. Install prerequisites:
    1. [Debian-based installation](https://github.com/Senzing/knowledge-base/blob/master/HOWTO/install-and-configure-senzing-using-apt.md) - For Ubuntu and [others](https://en.wikipedia.org/wiki/List_of_Linux_distributions#Debian-based)
    1. [RPM-based installation](https://github.com/Senzing/knowledge-base/blob/master/HOWTO/install-and-configure-senzing-using-yum.md) - For Red Hat, CentOS, openSuse and [others](https://en.wikipedia.org/wiki/List_of_Linux_distributions#RPM-based).

### Run commands

1. :pencil2: Run command for file input/output.
   Note: **GIT_REPOSITORY_DIR** needs to be set.
   Example:

    ```console
    export FLASK_APP=${GIT_REPOSITORY_DIR}/rootfs/app/app.py
    flask run --host=0.0.0.0
    ```

1. The web page can be seen at
   [localhost:5000](http://localhost:5000).

## Demonstrate as a project

### Create project

1. Define project location.
   Example:

    ```console
    export SENZING_PROJECT_DIR=${GIT_REPOSITORY_DIR}
    ```

1. Create  directories.
   Example:

    ```console
    mkdir --parents ${SENZING_PROJECT_DIR}/.senzing
    mkdir --parents ${SENZING_PROJECT_DIR}/var/sqlite
    mkdir --parents ${SENZING_PROJECT_DIR}/etc
    ```

1. Make SymLinks.
   Example:

    ```console
    cd ${SENZING_PROJECT_DIR}

    ln -s /opt/senzing/data-1.0 data
    ln -s /opt/senzing/g2-1.12 g2
    ```

1. Copy template files.
   Example:

    ```console
    cp ${SENZING_PROJECT_DIR}/g2/resources/templates/cfgVariant.json.template     ${SENZING_PROJECT_DIR}/etc/cfgVariant.json
    cp ${SENZING_PROJECT_DIR}/g2/resources/templates/customGn.txt.template        ${SENZING_PROJECT_DIR}/etc/customGn.txt
    cp ${SENZING_PROJECT_DIR}/g2/resources/templates/customOn.txt.template        ${SENZING_PROJECT_DIR}/etc/customOn.txt
    cp ${SENZING_PROJECT_DIR}/g2/resources/templates/customSn.txt.template        ${SENZING_PROJECT_DIR}/etc/customSn.txt
    cp ${SENZING_PROJECT_DIR}/g2/resources/templates/defaultGNRCP.config.template ${SENZING_PROJECT_DIR}/etc/defaultGNRCP.config
    cp ${SENZING_PROJECT_DIR}/g2/resources/templates/g2config.json.template       ${SENZING_PROJECT_DIR}/etc/g2config.json
    cp ${SENZING_PROJECT_DIR}/g2/resources/templates/G2Module.ini.template        ${SENZING_PROJECT_DIR}/etc/G2Module.ini
    cp ${SENZING_PROJECT_DIR}/g2/resources/templates/G2Project.ini.template       ${SENZING_PROJECT_DIR}/etc/G2Project.ini
    cp ${SENZING_PROJECT_DIR}/g2/resources/templates/stb.config.template          ${SENZING_PROJECT_DIR}/etc/stb.config

    cp ${SENZING_PROJECT_DIR}/g2/resources/templates/G2C.db.template              ${SENZING_PROJECT_DIR}/var/sqlite/G2C.db
    ```

1. Make files.
   Example:

    ```console
    touch  ${SENZING_PROJECT_DIR}/.senzing/project-history.json
    ```

1. Make `setupEnv`.
   Example:

    ```console
    cat <<EOT > ${SENZING_PROJECT_DIR}/setupEnv
    #!/bin/bash

    # Check if we are on a Debian based system, use additional libs
    if [ -f "/etc/debian_version" ]; then
      export LD_LIBRARY_PATH=${SENZING_PROJECT_DIR}/g2/lib:${SENZING_PROJECT_DIR}/g2/lib/debian:$LD_LIBRARY_PATH
    elif [[ "$OSTYPE" == "darwin"* ]]; then
      export LD_LIBRARY_PATH=${SENZING_PROJECT_DIR}/g2/lib:${SENZING_PROJECT_DIR}/g2/lib/macos:$LD_LIBRARY_PATH
      export DYLD_LIBRARY_PATH=${SENZING_PROJECT_DIR}/g2/lib:${SENZING_PROJECT_DIR}/g2/lib/macos:$DYLD_LIBRARY_PATH
    else
      export LD_LIBRARY_PATH=${SENZING_PROJECT_DIR}/g2/lib:$LD_LIBRARY_PATH
    fi
    EOT

    chmod +x ${SENZING_PROJECT_DIR}/setupEnv
    source ${SENZING_PROJECT_DIR}/setupEnv
    ```

1. Modify files.
   Example:

    ```console
    export MODIFY_FILES=( \
      "etc/G2Module.ini" \
      "etc/G2Project.ini" \
    )

    cd ${SENZING_PROJECT_DIR}

    for MODIFY_FILE in ${MODIFY_FILES[@]}; \
    do \
      sed -i.$(date +%s) \
        -e "s:/opt/senzing/data:${SENZING_PROJECT_DIR}/data:" \
        -e "s:/opt/senzing/g2/:${SENZING_PROJECT_DIR}/g2/:" \
        -e "s:/etc/opt/senzing:${SENZING_PROJECT_DIR}/etc:" \
        -e "s:/var/opt/senzing/:${SENZING_PROJECT_DIR}/var/:" \
        ${MODIFY_FILE}; \
    done
    ```

1. Initialize database.
   Example:

    ```console
    ${SENZING_PROJECT_DIR}/g2/python/G2SetupConfig.py --iniFile ${SENZING_PROJECT_DIR}/etc/G2Module.ini
    ```

### Project using docker

1. Build docker image.
   Example:

    ```console
    cd ${SENZING_PROJECT_DIR}
    sudo make docker-build
    ```

#### Project using docker using system mounts

1. Identify directories used by docker.
   Example:

    ```console
    export SENZING_DATA_VERSION_DIR=${SENZING_PROJECT_DIR}/data
    export SENZING_ETC_DIR=${SENZING_PROJECT_DIR}/etc
    export SENZING_G2_DIR=${SENZING_PROJECT_DIR}/g2
    export SENZING_VAR_DIR=${SENZING_PROJECT_DIR}/var
    ```

1. Use "Demonstrate using Docker" starting at [Docker network](#docker-network).

#### Project using docker using project mount

1. Run docker container.
   Example:

    ```console
    sudo docker run \
      ${SENZING_RUNAS_USER_PARAMETER} \
      ${SENZING_DATABASE_URL_PARAMETER} \
      ${SENZING_NETWORK_PARAMETER} \
      --env SENZING_PROJECT_DIR=/my-project \
      --env LD_LIBRARY_PATH=/my-project/g2/lib:/my-project/g2/lib/debian \
      --interactive \
      --publish 5001:5000 \
      --rm \
      --tty \
      --volume ${SENZING_PROJECT_DIR}:/my-project \
      --volume ${SENZING_DATA_VERSION_DIR}:/opt/senzing/data-1.0 \
      --volume ${SENZING_G2_DIR}:/opt/senzing/g2-1.12 \
      senzing/python-demo
    ```

### Project using command line

1. Run Flask.
   Example:

    ```console
    export FLASK_APP=${SENZING_PROJECT_DIR}/rootfs/app/app.py
    flask run --host=0.0.0.0
    ```

## Develop

### Prerequisite software

The following software programs need to be installed:

1. [git](https://github.com/Senzing/knowledge-base/blob/master/HOWTO/install-git.md)
1. [make](https://github.com/Senzing/knowledge-base/blob/master/HOWTO/install-make.md)
1. [docker](https://github.com/Senzing/knowledge-base/blob/master/HOWTO/install-docker.md)

### Clone repository

For more information on environment variables,
see [Environment Variables](https://github.com/Senzing/knowledge-base/blob/master/lists/environment-variables.md).

1. Set these environment variable values:

    ```console
    export GIT_ACCOUNT=docktermj
    export GIT_REPOSITORY=docker-python-demo
    export GIT_ACCOUNT_DIR=~/${GIT_ACCOUNT}.git
    export GIT_REPOSITORY_DIR="${GIT_ACCOUNT_DIR}/${GIT_REPOSITORY}"
    ```

1. Follow steps in [clone-repository](https://github.com/Senzing/knowledge-base/blob/master/HOWTO/clone-repository.md) to install the Git repository.

### Build docker image for development

1. Option #1 - Using `docker` command and GitHub.

    ```console
    sudo docker build --tag senzing/python-demo https://github.com/senzing/docker-python-demo.git
    ```

1. Option #2 - Using `docker` command and local repository.

    ```console
    cd ${GIT_REPOSITORY_DIR}
    sudo docker build --tag senzing/python-demo .
    ```

1. Option #3 - Using `make` command.

    ```console
    cd ${GIT_REPOSITORY_DIR}
    sudo make docker-build
    ```

    Note: `sudo make docker-build-development-cache` can be used to create cached docker layers.

## Examples

## Errors

1. See [docs/errors.md](docs/errors.md).

## References
