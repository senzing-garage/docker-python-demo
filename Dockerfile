ARG BASE_IMAGE=debian:11.3-slim@sha256:78fd65998de7a59a001d792fe2d3a6d2ea25b6f3f068e5c84881250373577414

# -----------------------------------------------------------------------------
# Stage: Final
# -----------------------------------------------------------------------------

# Create the runtime image.

FROM ${BASE_IMAGE} AS runner

ENV REFRESHED_AT=2022-04-01

LABEL Name="senzing/python-demo" \
      Maintainer="support@senzing.com" \
      Version="1.4.4"

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
 && apt-get clean \
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
ENV PYTHONPATH=/opt/senzing/g2/python
ENV SENZING_ETC_PATH=/etc/opt/senzing

WORKDIR /app
CMD ["flask", "run", "--host=0.0.0.0"]
