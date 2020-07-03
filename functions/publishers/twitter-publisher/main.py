import base64
import logging

import json

import constants
import twitter

from google.cloud import secretmanager

logger = logging.getLogger(__name__)

twitter_api_key_secret_id = "twitter-api-key"
twitter_api_secret_key_secret_id = "twitter-api-secret-key"
twitter_api_access_token_secret_id = "twitter-api-access-token"
twitter_api_access_token_secret_secret_id = "twitter-api-access-token-secret"

client = secretmanager.SecretManagerServiceClient()
twitter_api_key_secret_name = client.secret_version_path(constants.PROJECT_ID, twitter_api_key_secret_id, "1")
twitter_api_secret_key_secret_name = client.secret_version_path(constants.PROJECT_ID, twitter_api_secret_key_secret_id, "1")
twitter_api_access_token_secret_name = client.secret_version_path(constants.PROJECT_ID, twitter_api_access_token_secret_id, "1")
twitter_api_access_token_secret_secret_name = client.secret_version_path(constants.PROJECT_ID, twitter_api_access_token_secret_secret_id, "1")

twitter_api_key_secret_response = client.access_secret_version(twitter_api_key_secret_name)
twitter_api_secret_key_secret_response = client.access_secret_version(twitter_api_secret_key_secret_name)
twitter_api_access_token_secret_response = client.access_secret_version(twitter_api_access_token_secret_name)
twitter_api_access_token_secret_secret_response = client.access_secret_version(twitter_api_access_token_secret_secret_name)

twitter_api_key = twitter_api_key_secret_response.payload.data.decode('UTF-8')
twitter_api_secret_key = twitter_api_secret_key_secret_response.payload.data.decode('UTF-8')
twitter_api_access_token = twitter_api_access_token_secret_response.payload.data.decode('UTF-8')
twitter_api_access_token_secret = twitter_api_access_token_secret_secret_response.payload.data.decode('UTF-8')

api = twitter.Api(consumer_key=twitter_api_key,
                  consumer_secret=twitter_api_secret_key,
                  access_token_key=twitter_api_access_token,
                  access_token_secret=twitter_api_access_token_secret)


def tweet(title, link):
    message = f"{title}.\n\n{link}"
    api.PostUpdate(message)


def process_function_all(event, context):
    logger.info("function started")
    data = base64.b64decode(event["data"]).decode("utf-8")
    data_dict = json.loads(data)
    logger.info("data: {}".format(str(data_dict)))
    if data_dict["test"]:
        return

    title = data_dict["title"]
    url = data_dict["url"]
    tweet(title, url)


if "__main__" == __name__:
    from google.cloud import pubsub_v1
    publisher = pubsub_v1.PublisherClient()
    twitter_topic_path = publisher.topic_path(constants.PROJECT_ID, constants.TWITTER_PUBLISH_QUEUE_TOPIC_NAME)
    msg_dict = {
        "title": "test_title",
        "url": "test_url",
        "test": False
    }
    msg_str = json.dumps(msg_dict)
    msg_data = msg_str.encode("utf-8")
    publisher.publish(
        twitter_topic_path, msg_data
    )
