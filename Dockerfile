# Reference : https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0
# Build it by "docker build -t tinymurky/cs50_financial ."
# Push it by "docker push tinymurky/cs50_financial"
# run it by

# docker run -d -p 3000:80 \
#   -v $(pwd)/flask_session:/app/data/flask_session \
#   -v $(pwd)/database:/app/data/database \
#   -e PORT=3000 \
#   -e FLASK_SESSION_PATH=/app/data/flask_session \
#   -e DATABASE_PATH=/app/data/database \
#   tinymurky/cs50_financial

# builder is for install poetry
FROM python:3.11-buster as builder

RUN pip install poetry==1.8.3

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

# Copy poetry.lock* and toml first, then downoload and install dependencies

copy pyproject.toml poetry.lock* ./

#  install poetry then delete poetry cache(which store the downloaded packages) for minimizing the image size
RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

# The run time image, this won't have poetry
FROM python:3.11-slim-buster as runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"\
    PYTHONPATH=/app/src \
    PORT=3000\
    FLASK_SESSION_PATH=/app/data/flask_session\
    DATABASE_PATH=/app/data/database

# builder /app/.venv is python virtual environment, we copy to run time /app/.venv
copy --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

copy src ./src

EXPOSE $PORT

ENTRYPOINT ["python", "-m", "src.app.main"]