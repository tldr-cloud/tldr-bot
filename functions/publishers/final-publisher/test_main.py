import unittest
import main
import utils
import constants

from google.cloud import firestore

from unittest.mock import MagicMock

from google.cloud import pubsub_v1

publisher = pubsub_v1.PublisherClient()
mailsender_topic_path = publisher.topic_path("mailsender-288100",
                                             "publish-newsletter")


class TestMain(unittest.TestCase):

    def test_notify_newsletter_publisher(self):
        new_doc = MagicMock()
        new_doc.set = MagicMock()

        newsletter_collection = MagicMock()
        newsletter_collection.document = MagicMock(return_value=new_doc)

        publisher = MagicMock()
        publisher.publish = MagicMock()

        ids_for_newsletter = ["1", "2"]
        newsletter_id = "123"

        main.notify_newsletter_publisher(ids_for_newsletter,
                                         publisher=publisher,
                                         collection=newsletter_collection,
                                         id=newsletter_id,
                                         test=False)

        newsletter_collection.document.assert_called_with(newsletter_id)
        new_doc.set.assert_called_with({
            "news_ids": ids_for_newsletter,
            "test": False
        })
        publisher.publish.assert_called_with(
            mailsender_topic_path, newsletter_id.encode("utf-8")
        )


if __name__ == '__main__':
    unittest.main()
