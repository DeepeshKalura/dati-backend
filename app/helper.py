import json

def standardize_json(input_data):
    if "```json" in input_data:
        start_index = input_data.find("```json") + len("```json")
        end_index = input_data.find("```", start_index)
        json_data = input_data[start_index:end_index].strip()
        data = json.loads(json_data)
        return data
    else:
        return json.load(input_data)