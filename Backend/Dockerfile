FROM python:3.12-slim AS python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    POETRY_VERSION=2.0.0 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"


ENV PATH="$VENV_PATH/bin:$PATH"


FROM python-base AS builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential

#only for CV
#RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

#RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

RUN python -m venv $VENV_PATH && \
    . $VENV_PATH/bin/activate && \
    poetry install --only main



FROM python-base AS production

ENV FASTAPI_ENV=production

WORKDIR /app

COPY --from=builder-base $VENV_PATH $VENV_PATH
COPY . .

#CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
