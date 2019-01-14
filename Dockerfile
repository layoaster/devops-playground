FROM python:3.6.7-alpine3.7

LABEL maintainer="Lionel Mena <lionel@audiadis.io>"

WORKDIR /code

COPY requirements.txt .coveragerc pytest.ini ./

RUN set -x \
    && apk add --update --no-cache \
        g++ \
        make \
        libffi-dev \
        openssl-dev \
        # Adds timezones support to alpine-based images
        tzdata \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

COPY ./etc/gunicorn_conf.py /code/etc/
COPY ./myapi ./myapi

CMD [ "gunicorn", "-c", "./etc/gunicorn_conf.py", "myapi.app:app" ]
