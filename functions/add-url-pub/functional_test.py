import utils
import constants
import requests


test_url = "https://test.com/123"

test_request_json = {
    "queryResult": {
        "parameters": {
            "url": test_url
        }
    }
}

resp_raw = requests.post(url=constants.ADD_NEW_URL_URL, json=test_request_json)
resp = resp_raw.json()
print(resp)
if not "fulfillmentMessages" in resp:
    raise ValueError("incorrect answer from the function")
