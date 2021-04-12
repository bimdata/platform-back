FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION="1.1.3"

RUN wget -O get-poetry.py https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py && \
    python get-poetry.py --version ${POETRY_VERSION} -y && \
    rm get-poetry.py
ENV PATH="/root/.poetry/bin:${PATH}"
WORKDIR /opt

RUN poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml /opt/
RUN poetry install --no-dev --no-root
COPY ./ /opt