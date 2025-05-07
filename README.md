# docker-python-demo

If you are beginning your journey with [Senzing],
please start with [Senzing Quick Start guides].

You are in the [Senzing Garage] where projects are "tinkered" on.
Although this GitHub repository may help you understand an approach to using Senzing,
it's not considered to be "production ready" and is not considered to be part of the Senzing product.
Heck, it may not even be appropriate for your application of Senzing!

## Synopsis

This [senzing/python-demo] docker image demonstrates how to write
a Flask app based on the [senzing/senzingapi-runtime] docker image.

## Overview

### Related artifacts

1. [senzing/python-demo]

### Contents

1. [Demonstrate using Docker]
   1. [Set environment variables]
   1. [Run docker container]
1. [Demonstrate using docker-compose]
   1. [Download artifacts]
   1. [Prerequisite docker-compose stack]
   1. [Bring up docker-compose stack]
1. [Configuration]
1. [References]

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
  - [Docker]

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
     --publish 8356:5000 \
     --rm \
     senzing/python-demo
   ```

1. The running app is viewable at [localhost:8356].

## Demonstrate using docker-compose

### Download artifacts

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

1. Download artifacts.
   Example:

   ```console
   wget \
     -O ${SENZING_VOLUME}/docker-compose-backing-services-only.yaml \
     "https://raw.githubusercontent.com/Senzing/docker-compose-demo/main/resources/postgresql/docker-compose-rabbitmq-postgresql-backing-services-only.yaml"

   wget \
     -O ${SENZING_VOLUME}/docker-compose.yaml \
     "https://raw.githubusercontent.com/Senzing/docker-python-demo/main/docker-compose.yaml"
   ```

### Prerequisite docker-compose stack

1. Bring up a Docker Compose stack with backing services.
   Example:

   ```console
   docker-compose -f ${SENZING_VOLUME}/docker-compose-backing-services-only.yaml pull
   docker-compose -f ${SENZING_VOLUME}/docker-compose-backing-services-only.yaml up
   ```

### Bring up docker-compose stack

1. Download `docker-compose.yaml` file and deploy stack.
   _Note:_ `SENZING_VOLUME` needs to be set.
   Example:

   ```console
   docker-compose -f ${SENZING_VOLUME}/docker-compose.yaml pull
   docker-compose -f ${SENZING_VOLUME}/docker-compose.yaml up
   ```

1. The running app is viewable at [localhost:8356].

### Configuration

Configuration values specified by environment variable or command line parameter.

- **[SENZING_DEBUG]**

## References

- [Development]
- [Errors]
- [Examples]

[Bring up docker-compose stack]: #bring-up-docker-compose-stack
[Configuration]: #configuration
[Demonstrate using docker-compose]: #demonstrate-using-docker-compose
[Demonstrate using Docker]: #demonstrate-using-docker
[Development]: docs/development.md
[Docker]: https://github.com/senzing-garage/knowledge-base/blob/main/WHATIS/docker.md
[Download artifacts]: #download-artifacts
[Errors]: docs/errors.md
[Examples]: docs/examples.md
[localhost:8356]: http://localhost:8356
[Prerequisite docker-compose stack]: #prerequisite-docker-compose-stack
[References]: #references
[Run docker container]: #run-docker-container
[Senzing Garage]: https://github.com/senzing-garage
[Senzing Quick Start guides]: https://docs.senzing.com/quickstart/
[SENZING_DEBUG]: https://github.com/senzing-garage/knowledge-base/blob/main/lists/environment-variables.md#senzing_debug
[Senzing]: https://senzing.com/
[senzing/python-demo]: https://hub.docker.com/r/senzing/python-demo
[senzing/senzingapi-runtime]: https://hub.docker.com/r/senzing/senzingapi-runtime
[Set environment variables]: #set-environment-variables
