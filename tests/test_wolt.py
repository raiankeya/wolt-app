import os
import json

import pytest


json_file = os.path.join(os.path.dirname(__file__), "data.json")


@pytest.fixture
def close_day_data():
    data = {
        "monday": [],
        "friday": [{"type": "open", "value": 64800}, {"type": "close", "value": 64820}],
    }
    return data


@pytest.fixture
def two_consecutive_open_type():
    data = {
        "monday": [{"type": "open", "value": 36000}],
        "friday": [{"type": "open", "value": 64800}, {"type": "close", "value": 64820}],
    }
    return data


def test_request_with_sample_data(client):
    with open(json_file) as fp:
        response = client.post("/api", json=json.load(fp))
        assert b"Friday: 18:00 PM - 01:00 AM" in response.data
        assert b"Saturday: 09:00 AM - 11:00 AM, 16:00 PM - 23:00 PM" in response.data


def test_close_day(client, close_day_data):
    response = client.post("/api", json=close_day_data)
    assert b"Monday: Closed" in response.data


def test_two_consecutive_open_type(client, two_consecutive_open_type):
    expected_response = {
        "_schema": [
            "Cannot have two consecutive \"close\" times."
        ]
    }
    response = client.post("/api", json=two_consecutive_open_type)
    assert response == expected_response
