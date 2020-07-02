import constants
import logging
import json
import new_url_publisher
import utils

from google.cloud import pubsub_v1

new_url_publisher_obj = None

response = json.dumps({
    "fulfillmentMessages": [
        {
            "text": {
                "text": [
                    "done"
                ]
            }
        }
    ]
})

logger = logging.getLogger(__name__)


def process_function_request(request):
    try:
        global new_url_publisher_obj
        if not new_url_publisher_obj:
            publisher = pubsub_v1.PublisherClient()
            topic_path = publisher.topic_path(constants.PROJECT_ID, constants.NEW_URLS_TOPIC_NAME)
            new_url_publisher_obj = new_url_publisher.NewUrlPublisher(publisher, topic_path, logger)
        logger.info("request initiated")
        request_json = request.get_json()
        logger.info("request: {}".format(str(request_json)))
        url = request_json["queryResult"]["parameters"]["url"]
        logger.info("url to publish: {}".format(url))
        new_url_publisher_obj.publish_url(url)
        return response
    except Exception as e:
        utils.inform_boss_about_an_error(str(e), "add-url-pub")
        raise e
