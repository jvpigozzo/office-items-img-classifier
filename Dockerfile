# syntax=docker/dockerfile:1

# Python version
ARG PYTHON_VERSION=3.10.12
FROM python:${PYTHON_VERSION} as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Create directories
RUN mkdir -p /vol/media /vol/static

# Create user that the app will run under and change ownership of the directory
RUN adduser --disabled-password --gecos '' user && \
    chown -R user:user /vol/ && \
    chmod -R 755 /vol/

WORKDIR /app

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install --no-cache-dir -r requirements.txt

# Switch to the non-privileged user to run the application.
USER user

# Copy the source code into the container.
COPY ./app /app

# Expose the port that the application listens on.
EXPOSE 80

# Run the application.
CMD ["uvicorn", "main:app", "--reload", "--port", "80", "--host", "0.0.0.0"]
