import json


publisher = None
topic = "new-urls"
topic_path = None
status_publish = "publish"
status_preview = "preview"


def get_status(request_json):
    if "status" in request_json["queryResult"]["parameters"]:
        status = request_json["queryResult"]["parameters"]["status"]
        return status
    return status_preview


def publish_url(url, test=False):
    print("publishing URL: {}".format(url))
    from google.cloud import pubsub_v1
    global publisher
    global topic_path
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
    text = "published"
    if test:
        text = "published to test, do u want to publish to prod?"
    resp = {
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [ text ]
                }
            }
        ]
    }
    return json.dumps(resp)


def process_function_request(request):
    print("request initiated")
    request_json = request.get_json()
    print("request: {}".format(str(request_json)))
    status = get_status(request_json)
    print("status: {}".format(status))
    if status == status_publish:
        url = request_json["queryResult"]["outputContexts"][0]["parameters"]["url"]
        return publish_url(url, test=False)
    if status == status_preview:
        url = request_json["queryResult"]["parameters"]["url"]
        return publish_url(url, test=True)
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
