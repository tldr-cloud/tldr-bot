import base64
import nltk
import requests
import constants
import json
import utils

from boilerpy3 import extractors

from google.cloud import firestore
from google.cloud import pubsub_v1
from google.api_core import exceptions

nltk.download("punkt")

urls_collection = firestore.Client().collection(u"urls")
extractor = extractors.ArticleExtractor()

publisher = pubsub_v1.PublisherClient()
test_topic = "processed-urls-test"
test_topic_path = publisher.topic_path(constants.PROJECT_ID, test_topic)

bearer = utils.get_bearer()

summary_extractor_url = "https://us-central1-tldr-278619.cloudfunctions.net/extract-summary"


def extract_data(url):
     resp = requests.post(url=summary_extractor_url, json={"url": url, "bearer": bearer, "bert_summary": True}).json()
     return resp["summary"], resp["top_image"], resp["title"]


def publish_id_to_test(doc_id):
    msg_data = doc_id.encode("utf-8")
    publisher.publish(
        test_topic_path, msg_data
    )
    print("msg published")


def process_url(url, test):
    doc_id = utils.generate_id_from_url(url)
    print("url_id: {}".format(url))
    try:
        urls_collection.add({}, doc_id)
        print("new doc created")
    except exceptions.AlreadyExists:
        print("exceptions.AlreadyExists")
        publish_id_to_test(doc_id)
        return

    try:
        summary, top_image, title = extract_data(url)
    except:
        print("doc ref deleted")
        # deleting the document since it is empty
        urls_collection.document(doc_id).delete()
        raise
    publish = not test
    published = False
    doc_data = {
        "summary": summary,
        "top_image": top_image,
        "url": url,
        "title": title,
        "publish": publish,
        "published": published,
        "new": True
    }
    print("adding record to db")
    urls_collection.document(doc_id).set(doc_data)
    print("added")
    publish_id_to_test(doc_id)


def process_function_all(event, context):
    print("function started")
    data = base64.b64decode(event["data"]).decode("utf-8")
    data_dict = json.loads(data)
    print("data: {}".format(str(data_dict)))
    process_url(data_dict["url"], data_dict["test"])
