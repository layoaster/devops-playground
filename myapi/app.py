"""
Sample API implementation.
"""


from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    """
    The helloworld resource.
    """

    def get(self):
        """
        And it's GET handler.
        """
        return 'hello world!'


# Adding resources
api.add_resource(HelloWorld, '/')


if __name__ == '__main__':  # pragma: no cover
    app.run(debug=True)
