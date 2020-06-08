import requests
import json

from google.cloud import secretmanager

project_id = "tldr-278619"
secret_id = "bearer"

client = secretmanager.SecretManagerServiceClient()
secret_name = client.secret_version_path(project_id, secret_id, "1")
secret_response = client.access_secret_version(secret_name)
bearer = secret_response.payload.data.decode('UTF-8')

summary_extractor_url = "https://us-central1-tldr-278619.cloudfunctions.net/extract-summary"


def process_call(request):
    # Yes the following three lines are horrible, there is a reason for this, and it will be fixed ASAP.
    bearer_from_request = request.headers["bearer"]
    if bearer_from_request != bearer:
        return "error"
    print(request)
    request_json = request.get_json()
    url = request_json["queryResult"]["parameters"]["url"]
    print("processing url: {}".format(url))
    return extract_summary(url)


def extract_summary(url):
    resp = requests.post(url=summary_extractor_url, json={"url": url, "bearer": bearer})
    summary_sentances = resp.json()["summary"].split("\n")
    fulfillment_messages = [{"text": {"text": [msg]}} for msg in summary_sentances]
    bot_resp = {
            "fulfillmentMessages": fulfillment_messages
    }
    return json.dumps(bot_resp)
