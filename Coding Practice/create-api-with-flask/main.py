from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


class Cheese(Resource):
    def get(self, name):
        return {}


api.add_resource(Cheese, "/cheese")

if __name__ == "__main__":
    app.run(debug=True)
