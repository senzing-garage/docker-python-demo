ARG BASE_IMAGE=senzing/senzing-base
FROM ${BASE_IMAGE}

ENV REFRESHED_AT=2019-05-01

LABEL Name="senzing/python-demo" \
      Maintainer="support@senzing.com" \
      Version="1.0.1"

HEALTHCHECK CMD ["/app/healthcheck.sh"]

# Install packages via PIP.

RUN pip install \
    Flask==1.0.2

# The port for the Flask is 5000.

EXPOSE 5000

# Copy files from repository.

COPY ./rootfs /

# Environment variables for app.

ENV FLASK_APP=/app/app.py

# Runtime execution.

WORKDIR /app
CMD ["flask", "run", "--host=0.0.0.0"]
