import pytest
import csv
from utils.api_client import WeatherApiClient
from utils.schema_validator import validate_json_schema

API_KEY = "39d797f396b049ad900173658241405"

# Define JSON schema for validation
current_weather_schema = {
    "type": "object",
    "properties": {
        "location": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "region": {"type": "string"},
                "country": {"type": "string"},
            },
            "required": ["name", "region", "country"]
        },
        "current": {
            "type": "object",
            "properties": {
                "temp_c": {"type": "number"},
                "condition": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string"},
                    },
                    "required": ["text"]
                }
            },
            "required": ["temp_c", "condition"]
        }
    },
    "required": ["location", "current"]
}

simplified_forecast_schema = {
    "type": "object",
    "properties": {
        "location": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "region": {"type": "string"},
                "country": {"type": "string"},
            },
            "required": ["name", "region", "country"]
        },
        "forecast": {
            "type": "object",
            "properties": {
                "forecastday": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "date": {"type": "string"},
                            "day": {
                                "type": "object",
                                "properties": {
                                    "maxtemp_c": {"type": "number"},
                                    "mintemp_c": {"type": "number"},
                                    "condition": {
                                        "type": "object",
                                        "properties": {
                                            "text": {"type": "string"}
                                        },
                                        "required": ["text"]
                                    }
                                },
                                "required": ["maxtemp_c", "mintemp_c", "condition"]
                            }
                        },
                        "required": ["date", "day"]
                    }
                }
            },
            "required": ["forecastday"]
        }
    },
    "required": ["location", "forecast"]
}

@pytest.fixture(scope="module")
def api_client():
    return WeatherApiClient(API_KEY)

def read_test_data(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

@pytest.mark.parametrize("data", read_test_data("tests/test_data.csv"))
def test_get_current_weather(api_client, data):
    response = api_client.get_current_weather(data['location'])
    assert response.status_code == 200

    response_json = response.json()
    is_valid, error_message = validate_json_schema(response_json, current_weather_schema)
    assert is_valid, f"Schema validation failed for location {data['location']}: {error_message}"

@pytest.mark.parametrize("data", read_test_data("tests/test_data.csv"))
def test_get_forecast(api_client, data):
    response = api_client.get_forecast(data['location'], 3)
    assert response.status_code == 200

    response_json = response.json()
    is_valid, error_message = validate_json_schema(response_json, simplified_forecast_schema)
    assert is_valid, f"Schema validation failed for forecast of location {data['location']}: {error_message}"

def test_post_example(api_client):
    payload = {
        "example_key": "example_value"
    }
    response = api_client.post_example("example_endpoint", payload)
    assert response.status_code == 404  # Change according to your actual endpoint and expected response
