import requests

# add a new cheese to the data file
response = requests.post(
    "http://127.0.0.1:5000/cheese",
    json={"cheese": "Gouda", "age_years": 0.5, "country": "Netherlands", "hardness": 5},
    headers={"Content-Type": "application/json"},
)
print(response.json(), sep="\n")

# return data for the "Cheddar" cheese
response = requests.get("http://127.0.0.1:5000/cheese/Cheddar")
print(response.json(), sep="\n")

# delete the "Gouda" cheese from the data file
response = requests.delete("http://127.0.0.1:5000/cheese", json={"cheese": "Gouda"})
print(response.json(), sep="\n")
