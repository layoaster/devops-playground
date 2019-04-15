ARG PYTHON_VERSION=3.6.7-alpine3.8

# Python Base build
FROM python:${PYTHON_VERSION} AS python-base

LABEL maintainer="Lionel Mena <lionel@audiadis.io>"

RUN set -x \
    && apk add --update --no-cache \
        g++ \
        make \
        libffi-dev \
        openssl-dev \
        # Adds timezones support to alpine-based images
        tzdata

WORKDIR /wheels

COPY requirements.txt ./

RUN pip install --upgrade pip \
    && pip wheel -r /wheels/requirements.txt


# Production Image build
FROM python:${PYTHON_VERSION} AS release

LABEL maintainer="Lionel Mena <lionel@audiadis.io>"

COPY --from=python-base /wheels /wheels

RUN set -x \
    && pip install --upgrade pip \
    && pip install -r /wheels/requirements.txt -f /wheels \
    && rm -rf /wheels \
    && rm -rf /root/.cache/pip/*

WORKDIR /code

COPY .coveragerc pytest.ini ./
COPY ./etc/gunicorn_conf.py /code/etc/
COPY ./myapi ./myapi

CMD [ "gunicorn", "-c", "./etc/gunicorn_conf.py", "myapi.app:app" ]
