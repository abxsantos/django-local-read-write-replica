FROM python:3.9-slim-buster

WORKDIR /app

# Copies necessary stuff to install dependencies
COPY pyproject.toml /app/

# Installs Poetry
RUN pip install --upgrade pip && \
    pip install poetry  && poetry config virtualenvs.create false --local

# Creates requirements.txt, removes poetry and installs projects dependencies as a separate layer
RUN poetry export -f requirements.txt -o requirements.txt && \
    pip uninstall --yes poetry && \
    pip install --require-hashes -r requirements.txt

# Copies other files
COPY . /app