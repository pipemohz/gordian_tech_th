"""
Task 2
"""
from os.path import dirname, join
from pathlib import Path
import yaml
import json
import xmltodict
import jsonschema
import re


def set_schema() -> dict:
    path = Path(dirname(__file__)).parent
    with open(join(path, "seats.yaml")) as f:
        return yaml.safe_load(f)


def apply_schema(json_data: dict, schema: dict):
    json_parsed = {}
    keys = list(map(lambda x: x.lower(), schema.keys()))
    for prop, prop_schema in json_data.items():
        tag = re.sub(r"ns:|@|#", "", prop).lower()
        if not prop in keys and type(prop_schema) is dict:
            json_parsed[tag] = apply_schema(prop_schema, schema)
        elif type(prop_schema) is list:
            json_parsed[tag] = [
                apply_schema(item, schema)
                if type(item) is dict
                else
                item
                for item in prop_schema]
        else:
            json_parsed[tag] = prop_schema

    return json_parsed


def parse_xml_to_json(xml_string):
    return xmltodict.parse(xml_string)


def write_json_file(data: dict):
    path = dirname(__file__)
    with open(join(path, "seatmap.json"), mode="w") as f:
        f.write(json.dumps(data, indent=4))


def process():
    path = dirname(__file__)

    with open(join(path, "seatmap.xml")) as f:
        json_data = parse_xml_to_json(f.read())

    schema = set_schema()

    parsed = apply_schema(
        json_data["soapenv:Envelope"]["soapenv:Body"]["ns:OTA_AirSeatMapRS"]["ns:SeatMapResponses"],
        schema
    )

    jsonschema.validate(parsed, schema)

    write_json_file(parsed)


if __name__ == "__main__":
    process()
