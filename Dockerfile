FROM python:3.14-alpine
ENV PYTHONPATH "${PYTHONPATH}:/bot"
ENV PATH "/bot/scripts:${PATH}"
WORKDIR /bot

# Install poetry
RUN set +x \
 && apk update \
 && apk upgrade \
 && apk add --no-cache curl bash gcc \
 && curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python -\
 && ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry \
 && apk del curl \
 && rm -rf /var/lib/apt/lists/* \
 && poetry config virtualenvs.create false

# Install dependencies
COPY pyproject.toml /bot/
RUN poetry install --no-interaction --no-ansi --only main --no-root

# Prepare entrypoint
ADD . /bot/
RUN chmod +x scripts/*
ENTRYPOINT ["docker-entrypoint.sh"]
