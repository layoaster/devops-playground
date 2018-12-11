"""
Sample API implementation.
"""
import os
import time

import redis
from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

# Redis DB
cache = redis.Redis(host=os.getenv('REDIS_HOSTNAME'), port=6379)


def get_hit_count():
    """
    Fetches the number of times the main page has been hit.

    :raises redis.exceptions.ConnectionError: Can't stablish a connection to
        redis after retrying for 2.5 seconds.
    :return: Number of web page hits.
    :rtype: int
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

    def get(self):
        """
        And it's GET handler.
        """
        return {'Hello World!': get_hit_count()}


# Adding resources
api.add_resource(HelloWorld, '/')


if __name__ == '__main__':  # pragma: no cover
    app.run(host="0.0.0.0", debug=True)
