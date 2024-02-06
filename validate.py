import json
import metro2


# Load the JSON data
with open('data.json', 'r') as f:
    data = json.load(f)

# Instantiate the validator
v = metro2.Metro2Validator(metro2.schema)

if not isinstance(data, list):
    data = [data]

for item in data:
    # Validate the item
    if v.validate(item):
        print("The JSON data is valid.")
    else:
        print("The JSON data is invalid.")
        print("Errors:", v.errors)
