FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Maintainer of the Dockerfile
LABEL maintainer="Mairror Team"

# Input data
ARG NON_ROOT_USER=nroot
ARG ID=1000

# Configure environment
ENV APP_MODULE=main:app \
    WORKERS_PER_CORE=4 \
    MAX_WORKERS=4 \
    WEB_CONCURRENCY=4 \
    HOST=0.0.0.0 \
    PORT=8000 \
    BIND=0.0.0.0:8000 \
    LOG_LEVEL=info \
    WORKER_CLASS=uvicorn.workers.UvicornWorker \
    TIMEOUT=120 \
    KEEP_ALIVE=20 \
    GRACEFUL_TIMEOUT=120

# Hadolint DL4006
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Switch to root user to make administrative tasks
# hadolint ignore=DL3002
USER root

# Change directory to /tmp to do administrative tasks
WORKDIR /tmp

# Create a non-root user group
RUN addgroup ${NON_ROOT_USER} --gid ${ID} && \
    adduser \
      --disabled-password \
      --uid ${ID} --gid ${ID} \
      --shell /bin/bash \
      --gecos "" \
      ${NON_ROOT_USER}

# Upgrade OS && install all OS dependencies
RUN apt-get update && \
      # DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends
    # APT and /tmp cleanup
    apt-get clean && apt-get autoremove -y && \
        rm -rf /var/lib/{apt,dpkg,cache,log}/ && \
        rm -rf -- *

# Change the ownership of /app to the non-root user
RUN chown -R ${NON_ROOT_USER}:${NON_ROOT_USER} /app

# Use non-root user
USER ${NON_ROOT_USER}

# Install python libraries
COPY requirements.txt /app

RUN pip install --upgrade pip==21.3.1 --no-cache-dir && \
    pip install -r /app/requirements.txt --no-cache-dir

# Change directory to /app to execute the app
WORKDIR /app

# Add local files as late as possible to avoid cache busting
COPY --chown=${NON_ROOT_USER}:${ID} src/ /app

CMD ["python", "main.py"]
