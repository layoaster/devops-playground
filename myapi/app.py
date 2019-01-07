"""
Sample API implementation.
"""
import os
import time

import flask
import redis
from flask import Flask, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

# Redis DB
cache = redis.Redis(host=os.getenv('REDIS_HOSTNAME'), port=6379)


def get_hit_count() -> int:
    """
    Fetches the number of times the main page has been hit.

    :raises redis.exceptions.ConnectionError: Can't stablish a connection to
        redis after retrying for 2.5 seconds.
    :return: Number of web page hits.
    """
    retries = 5

    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


class HelloWorld(Resource):
    """
    The helloworld resource.
    """

    def get(self) -> flask.Response:
        """
        And it's GET handler.

        :return: Main page data.
        """
        response = jsonify({'Hello-World! hits': get_hit_count()})
        response.status_code = 202

        return response


class HealthCheck(Resource):
    """
    Implements application health checks.
    """

    def get(self) -> flask.Response:
        """
        Checks application's health.

        :return: `200` if everything is ok. `503` otherwise.
        """
        check = {'status': 'pass'}

        # Checking Redis
        try:
            cache.info(section='server')
        except redis.exceptions.RedisError:
            check['status'] = 'fail'

        response = jsonify(check)
        response.status_code = 200 if check['status'] == 'pass' else 503

        return response


# Adding resources
api.add_resource(HelloWorld, '/')
api.add_resource(HealthCheck, '/healthz')


if __name__ == '__main__':  # pragma: no cover
    app.run(host="0.0.0.0", debug=True)
