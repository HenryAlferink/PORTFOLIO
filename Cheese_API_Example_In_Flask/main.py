from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import json

app = Flask(__name__)
api = Api(app)

# import json data into Python dictionary
with open("cheeses.json", "r") as file:
    cheeses = json.load(file)


class Cheese(Resource):
    def get(self, cheese):
        return {"data": {cheese: cheeses[cheese]}}

    def post(self):
        data = request.json
        cheese = data["cheese"]
        cheeses[cheese] = {
            "age_years": data["age_years"],
            "country": data["country"],
            "hardness": data["hardness"],
        }
        with open("cheeses.json", "w") as file:
            file.write(json.dumps(cheeses, indent=4))
        return {"message": f"Cheese {cheese} added successfully"}

    def delete(self):
        cheese = request.json["cheese"]
        del cheeses[cheese]
        with open("cheeses.json", "w") as file:
            file.write(json.dumps(cheeses, indent=4))
        return {"message": f"Cheese {cheese} deleted successfully"}


# define which endpoints can use the given methods
api.add_resource(Cheese, "/cheese/<string:cheese>", "/cheese")

file.close()

if __name__ == "__main__":
    app.run(debug=True)
