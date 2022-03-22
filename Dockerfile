ARG BASE_IMAGE=senzing/senzing-base:1.6.5

# -----------------------------------------------------------------------------
# Stage: Final
# -----------------------------------------------------------------------------

# Create the runtime image.

FROM ${BASE_IMAGE} AS runner

ENV REFRESHED_AT=2022-03-22

LABEL Name="senzing/python-demo" \
      Maintainer="support@senzing.com" \
      Version="1.4.4"

# Define health check.

HEALTHCHECK CMD ["/app/healthcheck.sh"]

# Run as "root" for system installation.

USER root

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

WORKDIR /app
CMD ["flask", "run", "--host=0.0.0.0"]
