FROM python:3.6.7-alpine3.7

LABEL maintainer="Lionel Mena <lionel@audiadis.com>"

WORKDIR /code

COPY requirements.txt .coveragerc ./

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

COPY ./myapi ./myapi

CMD [ "python", "myapi/app.py" ]