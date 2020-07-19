import time
import json

import constants
import utils
import publish_utils

from google.cloud import firestore
from google.cloud import pubsub_v1

publisher = pubsub_v1.PublisherClient()
twitter_topic_path = publisher.topic_path(constants.PROJECT_ID, constants.TWITTER_PUBLISH_QUEUE_TOPIC_NAME)

prod_chat_id = "@techtldr"
urls_collection = firestore.Client().collection(u"urls")


def publish_to_twitter_topic(title, telegram_url):
    msg_dict = {
        "title": title,
        "url": telegram_url,
        "test": False
    }
    msg_str = json.dumps(msg_dict)
    msg_data = msg_str.encode("utf-8")
    publisher.publish(
        twitter_topic_path, msg_data
    )


def publish_all_unpublished_docs():
    docs = urls_collection.where(u"publish", u"==", True).where(u"published", u"==", False).stream()

    for doc in docs:
        print("doc found: {}".format(str(doc.id)))
        updated_doc_data = {
            "publish": False,
            "published": True
        }
        urls_collection.document(doc.id).set(updated_doc_data, merge=True)
        telegram_message = publish_utils.publish_doc(doc, prod_chat_id)
        title = doc.get("title")
        link = publish_utils.generate_telegram_link(prod_chat_id, telegram_message.message_id)
        publish_to_twitter_topic(title, link)
        time.sleep(3)


def function_call_publish(event, context):
    try:
        print("final-publisher invoked")
        publish_all_unpublished_docs()
    except Exception as e:
        utils.inform_boss_about_an_error(str(e), "final-publisher")


if "__main__" == __name__:
    publish_all_unpublished_docs()
