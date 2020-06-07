import requests
import json

summary_extractor_url = "https://us-central1-tldr-278619.cloudfunctions.net/extract-summary"


def process_call(request):
    print(request)
    request_json = request.get_json()
    url = request_json["queryResult"]["parameters"]["url"]
    print("processing url: {}".format(url))
    return extract_summary(url)


def extract_summary(url):
    resp = requests.post(url=summary_extractor_url, json={"url": url})
    summary_sentances = resp.json()["summary"].split("\n")
    fulfillment_messages = [{"text": {"text": [msg]}} for msg in summary_sentances]
    bot_resp = {
            "fulfillmentMessages": fulfillment_messages
    }
    return json.dumps(bot_resp)
