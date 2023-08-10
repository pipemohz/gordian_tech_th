"""
Task 1
"""
import requests
from requests import Response
from requests import HTTPError
import json
import os
from os import listdir
from os.path import dirname, join
from dotenv import load_dotenv

load_dotenv()

URL = os.environ["GORDIAN_API_URL"]
API_KEY = os.environ["GORDIAN_API_KEY"]

headers = {
    "accept": "application/json",
    "authorization": f"Basic {API_KEY}",
    "content-type": "application/json"
}


def load_json(path: str) -> dict:
    with open(path, mode="r", encoding="utf8") as f:
        return json.load(f)


def save_output(filename: str, data: dict):
    path = join(dirname(__file__), "output", filename)
    with open(path, mode="w", encoding="utf8") as f:
        f.write(json.dumps(data, indent=4))


def create_trip(data: dict) -> Response:
    response = requests.post(
        URL,
        headers=headers,
        json=data
    )

    response.raise_for_status()

    return response


def get_search_results(trip_id: str, search_id: str) -> Response:
    response = requests.get(
        f"{URL}/{trip_id}/search/{search_id}",
        headers=headers
    )

    response.raise_for_status()

    if response.json()["status"] == "in_progress":
        print(f"Retrying search results for search_id {search_id}...")
        response = get_search_results(trip_id, search_id)

    return response


def process():
    path = join(dirname(__file__), "input")
    for file in listdir(path):
        try:
            data = load_json(join(path, file))
            response = create_trip(data)
            response = get_search_results(
                trip_id=response.json()["trip_id"],
                search_id=response.json()["search_id"]
            )
            save_output(file, response.json())
        except HTTPError as exception:
            print(f"An error has ocurred during request stage: {exception}")
        else:
            print(f"Data from {file} has been processed.")


if __name__ == "__main__":
    process()
