ARG BASE_IMAGE=senzing/senzing-base
FROM ${BASE_IMAGE}

# Build-time variables.

ENV REFRESHED_AT=2019-03-22

LABEL Name="senzing/python-demo" \
      Version="1.0.0"

# Perform PIP installs.

RUN pip install \
    Flask==1.0.2

# The port for the Flask is 5000.

EXPOSE 5000

# Copy the repository's app directory.

COPY ./rootfs /

# Environment variables for app.

ENV FLASK_APP=/app/app.py

# Run-time command.

WORKDIR /app
CMD ["flask", "run", "--host=0.0.0.0"]
