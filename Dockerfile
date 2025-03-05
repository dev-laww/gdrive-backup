FROM python:3.11-buster AS builder

RUN pip install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --no-root

FROM python:3.11-slim-buster AS runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

ARG SERVICE_ACCOUNT
COPY ${SERVICE_ACCOUNT:-credentials.json} ./credentials.json

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY main.py .

ENTRYPOINT ["python", "-u", "/app/main.py"]