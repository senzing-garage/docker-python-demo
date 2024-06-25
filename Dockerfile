ARG BASE_IMAGE=senzing/senzingapi-runtime:3.10.3

# -----------------------------------------------------------------------------
# Stage: Final
# -----------------------------------------------------------------------------

# Create the runtime image.

FROM ${BASE_IMAGE}

ENV REFRESHED_AT=2024-06-24

LABEL Name="senzing/python-demo" \
  Maintainer="support@senzing.com" \
  Version="1.5.6"

# Define health check.

HEALTHCHECK CMD ["/app/healthcheck.sh"]

# Run as "root" for system installation.

USER root

# Install packages via apt.

RUN apt-get update \
  && apt-get -y install \
  libssl1.1 \
  odbc-postgresql \
  odbcinst \
  python3-dev \
  python3-pip \
  sqlite3 \
  unixodbc \
  && rm -rf /var/lib/apt/lists/*

# Install packages via PIP.

COPY requirements.txt .
RUN pip3 install --upgrade pip \
  && pip3 install -r requirements.txt \
  && rm /requirements.txt

# Copy files from repository.

COPY ./rootfs /

# The port for the Flask is 5000.

EXPOSE 5000

# Make non-root container.

USER 1001

# Runtime execution.

ENV FLASK_APP=/app/app.py
ENV LD_LIBRARY_PATH=/opt/senzing/g2/lib:/opt/senzing/g2/lib/debian:/opt/IBM/db2/clidriver/lib
ENV ODBCSYSINI=/etc/opt/senzing
ENV PATH=${PATH}:/opt/senzing/g2/python:/opt/IBM/db2/clidriver/adm:/opt/IBM/db2/clidriver/bin
ENV PYTHONPATH=/opt/senzing/g2/sdk/python
ENV SENZING_ETC_PATH=/etc/opt/senzing

WORKDIR /app
CMD ["flask", "run", "--host=0.0.0.0"]
