# syntax=docker/dockerfile:1

FROM docker.io/python:3.11-slim-bookworm AS python

# === Python Build Stage ===
FROM python AS python-build-stage

ARG BUILD_ENVIRONMENT=local

RUN apt-get update && apt-get install --no-install-recommends -y \
  build-essential \
  libpq-dev \
  && rm -rf /var/lib/apt/lists/*

COPY ./requirements /requirements
RUN pip wheel --wheel-dir /usr/src/app/wheels -r /requirements/local.txt

# === Python Run Stage ===
FROM python AS python-run-stage

ARG BUILD_ENVIRONMENT=local
ARG APP_HOME=/app
ARG USERID=1000
ARG GROUPID=1000

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    BUILD_ENV=${BUILD_ENVIRONMENT} \
    PYTHONPATH=/app:/app/jpf_stretch_hub:$PYTHONPATH \
    NODE_VERSION=20 \
    NODE_PATH=/home/devuser/.npm-global/lib/node_modules \
    NPM_CONFIG_PREFIX=/home/devuser/.npm-global \
    PATH=/home/devuser/.npm-global/bin:$PATH

# Install Node.js using the official Node.js installation method
RUN apt-get update && apt-get install --no-install-recommends -y \
    sudo git bash-completion nano ssh curl ca-certificates \
    libpq-dev wait-for-it gettext gnupg \
    && mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_${NODE_VERSION}.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list \
    && apt-get update && apt-get install --no-install-recommends -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user and set up directory structure
RUN groupadd --gid ${GROUPID} devuser \
    && useradd --uid ${USERID} --gid devuser --shell /bin/bash --create-home devuser \
    && echo devuser ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/devuser \
    && chmod 0440 /etc/sudoers.d/devuser

# Create all required directories at once
RUN mkdir -p ${APP_HOME} \
    ${APP_HOME}/theme/static \
    ${APP_HOME}/theme/static_src/src/styles \
    ${APP_HOME}/staticfiles \
    ${APP_HOME}/mediafiles \
    ${APP_HOME}/node_modules \
    /home/devuser/.npm-global \
    && chown -R devuser:devuser ${APP_HOME} /home/devuser/.npm-global

# Copy and set up scripts as root
COPY ./compose/production/django/entrypoint /entrypoint
COPY ./compose/local/django/start /start
COPY ./compose/local/django/celery/worker/start /start-celeryworker
COPY ./compose/local/django/celery/beat/start /start-celerybeat
COPY ./compose/local/django/celery/flower/start /start-flower

RUN sed -i 's/\r$//g' /entrypoint /start /start-celeryworker /start-celerybeat /start-flower \
    && chmod +x /entrypoint /start /start-celeryworker /start-celerybeat /start-flower

# Switch to non-root user
USER devuser
WORKDIR ${APP_HOME}

# Add user paths
ENV PATH="/home/devuser/.local/bin:/home/devuser/.npm-global/bin:$PATH"

# Install global npm packages
RUN npm config set prefix '/home/devuser/.npm-global' \
    && npm install -g tailwindcss@latest postcss@latest autoprefixer@latest postcss-cli@latest cssnano@latest

# Copy application code
COPY --chown=devuser:devuser . ${APP_HOME}

# Copy and install Python dependencies
COPY --from=python-build-stage /usr/src/app/wheels /wheels/
RUN pip install --user --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    && sudo rm -rf /wheels/

ENTRYPOINT ["/entrypoint"]
