import json

import logging

import unittest
import new_url_publisher

from google.cloud import pubsub_v1
from unittest.mock import MagicMock

logger = logging.getLogger(__name__)


class TestMain(unittest.TestCase):

    def test_publish_url(self):
        topic_path = "path/test-topic"
        url = "https://test.com/123"
        publisher = pubsub_v1.PublisherClient()
        publisher.publish = MagicMock()

        expected_msg_dict = {
            "url": url,
            "test": True
        }
        expected_msg_str = json.dumps(expected_msg_dict)
        expected_msg_data = expected_msg_str.encode("utf-8")

        under_test = new_url_publisher.NewUrlPublisher(publisher, topic_path, logger)
        under_test.publish_url(url)

        publisher.publish.assert_called_with(topic_path, expected_msg_data)


if __name__ == '__main__':
    unittest.main()
