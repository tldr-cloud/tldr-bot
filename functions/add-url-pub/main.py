import json

from google.cloud import secretmanager
from flask import jsonify

publisher = None
topic = "new-urls"
topic_path = None

summary_extractor_url = "https://us-central1-tldr-278619.cloudfunctions.net/extract-summary"

status_publish = "publish"
status_preview = "preview"
status_test = "test"

project_id = "tldr-278619"
secret_id = "bearer"

client = secretmanager.SecretManagerServiceClient()
secret_name = client.secret_version_path(project_id, secret_id, "1")
secret_response = client.access_secret_version(secret_name)
bearer = secret_response.payload.data.decode('UTF-8')


def preview_url(url, session, retry_count):
    import requests
    try:
        resp_raw = requests.post(url=summary_extractor_url, json={"url": url, "bearer": bearer}, timeout=2)
        print(resp_raw.content)
        resp = resp_raw.json()
    except requests.exceptions.Timeout:
        if retry_count < 5:
            retry_response = {
                "fulfillmentMessages": [
                    {
                        "text": {
                            "text": ["failed to get summary, retrying, # {}".format(str(retry_count))]
                        }
                    }
                ],
                "followupEventInput": {
                    "name": "retry",
                    "languageCode": "en-US",
                    "parameters": {
                        "count": retry_count + 1
                    }
                }
            }
        else:
            retry_response = {
                "fulfillmentMessages": [
                    {
                        "text": {
                            "text": ["retry error"]
                        }
                    }
                ]
            }
        return json.dumps(retry_response)
    summary = resp["summary"]
    top_image = resp["top_image"]
    fulfillment_messages = [{"text": {"text": [msg]}} for msg in summary.split("\n")]
    fulfillment_messages.append({"text": {"text": ["===================="]}})
    fulfillment_messages.append({"text": {"text": ["Is this good enough? or you want first to test this shit?"]}})
    # noinspection PyTypeChecker
    fulfillment_messages.append(
        {
            "buttons": [
                {
                    "postback": "yes",
                    "text": "yes"
                },
                {
                    "postback": "no",
                    "text": "no"
                },
                {
                    "postback": "test",
                    "text": "test"
                }
            ],
            "imageUrl": top_image
        }
    )
    bot_resp = {
        "fulfillmentMessages": fulfillment_messages,
        "outputContexts": [
            {
                "name": "{}/contexts/tldr-showed".format(session),
                "lifespanCount": 3,
                "parameters": {
                    "url": url
                }
            }
        ]
    }
    return json.dumps(bot_resp)


def get_status(request_json):
    if "status" in request_json["queryResult"]["parameters"]:
        status = request_json["queryResult"]["parameters"]["status"]
        return status
    return status_preview


def publish_url(url, test=False):
    print("publishing URL: {}".format(url))
    from google.cloud import pubsub_v1
    global publisher
    if not publisher:
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path("tldr-278619", topic)
    msg_dict = {
        "url": url,
        "test": test
    }
    # msg data must be a bytestring
    msg_str = json.dumps(msg_dict)
    print("msg to post: {}".format(msg_str))
    msg_data = msg_str.encode("utf-8")
    publisher.publish(
        topic_path, msg_data
    )
    resp = {
        "fulfillmentMessages": [
            {
                "text": {
                    "text": ["published"]
                }
            }
        ]
    }
    return json.dumps(resp)


def process_function_request(request):
    print("request initiated")
    # Yes the following three lines are horrible, there is a reason for this, and it will be fixed ASAP.
    bearer_from_request = request.headers["bearer"]
    if bearer_from_request != bearer:
        print("incorrect bearer")
        return "error"
    request_json = request.get_json()
    print("request: {}".format(str(request_json)))
    status = get_status(request_json)
    print("status: {}".format(status))
    if status == status_publish or status == status_test:
        test = status == status_test
        print("test status: {}".format(test))
        url = request_json["queryResult"]["outputContexts"][0]["parameters"]["url"]
        return publish_url(url, test=test)
    if status == status_preview:
        url = request_json["queryResult"]["parameters"]["url"]
        session = request_json["session"]
        retry_count = request_json["queryResult"]["parameters"].get("retry_count", 0)
        return preview_url(url, session, retry_count)
    resp = {
        "fulfillmentMessages": [
            {
                "text": {
                    "text": ["0_o something just horrible happen"]
                }
            }
        ]
    }
    return json.dumps(resp)


if "__main__" == __name__:
    publish_url("https://www.itnews.com/article/3561496/"
                "google-meet-denoiser-video-shows-shockingly-good-noise-filtering.html",
                True)
