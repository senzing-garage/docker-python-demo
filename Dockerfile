FROM senzing/python-base

# Build-time variables

ARG REFRESHED_AT=2018-10-15

# Perform PIP installs

RUN pip install \
    Flask==1.0.2

# The port for the Flask is 5000.

EXPOSE 5000

# Copy the repository's app directory.

COPY ./app /app

# Environment variables for app.

ENV FLASK_APP=/app/app.py

# Run-time command

WORKDIR /app
CMD ["flask", "run", "--host=0.0.0.0"]
