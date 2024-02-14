import json
import os
from metro2 import Metro2Validator, schema
import pprint

def validate_json_objects_in_files(folder_path):
    for dirname, _, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.endswith('.json'):
                f_path = os.path.join(dirname, filename)
                with open(f_path, 'r') as f:
                    data = json.load(f)

                validator = Metro2Validator(schema)

                if not isinstance(data, list):
                    data = [data]

                valid_objs = 0
                invalid_objs = 0
                errors = {}

                for item in data:
                    if validator.validate(item):
                        valid_objs += 1
                    else:
                        invalid_objs += 1
                        errors[valid_objs + invalid_objs] = validator.errors

                print(f'File: {f_path}')
                print(f'  Valid objects: {valid_objs}')
                print(f'  Invalid objects: {invalid_objs}')
                print(f'  Errors:')
                pprint.pprint(errors)

# Run the function with the folder path
validate_json_objects_in_files('.')
