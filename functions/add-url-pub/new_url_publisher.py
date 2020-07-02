import json
import logging

from google.cloud import pubsub_v1


class NewUrlPublisher(object):

    def __init__(self, publisher: pubsub_v1.PublisherClient, topic_path: str, logger: logging.Logger):
        self.publisher = publisher
        self.topic_path = topic_path
        self.logger = logger

    def publish_url(self, url: str):
        self.logger.info("publishing URL: {}".format(url))
        msg_dict = {
            "url": url,
            "test": True
        }
        msg_str = json.dumps(msg_dict)
        self.logger.info("msg to post: {}".format(msg_str))
        msg_data = msg_str.encode("utf-8")
        self.publisher.publish(
            self.topic_path, msg_data
        )
