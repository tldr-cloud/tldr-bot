import base64
import nltk
import requests
import constants
import json

from boilerpy3 import extractors

from google.cloud import firestore
from google.cloud import pubsub_v1
from google.api_core import exceptions

from google.cloud import secretmanager

secret_id = "bearer"

nltk.download("punkt")

urls_collection = firestore.Client().collection(u"urls")
extractor = extractors.ArticleExtractor()

publisher = pubsub_v1.PublisherClient()
prod_topic = "processed-urls"
prod_topic_path = publisher.topic_path(constants.PROJECT_ID, prod_topic)
test_topic = "processed-urls-test"
test_topic_path = publisher.topic_path(constants.PROJECT_ID, test_topic)

client = secretmanager.SecretManagerServiceClient()
secret_name = client.secret_version_path(constants.PROJECT_ID, secret_id, "1")
secret_response = client.access_secret_version(secret_name)
bearer = secret_response.payload.data.decode('UTF-8')

summary_extractor_url = "https://us-central1-tldr-278619.cloudfunctions.net/extract-summary-bert"


def generate_id_from_url(url):
     return url.replace("/", "_").replace(":", "_")


def extract_data(url):
     resp = requests.post(url=summary_extractor_url, json={"url": url, "bearer": bearer}).json()
     return (resp["summary"], resp["top_image"], resp["title"])


def publish_id(doc_id, test):
    msg_data = doc_id.encode("utf-8")
    if test:
        topic_path = test_topic_path
    else:
        topic_path = prod_topic_path
    publisher.publish(
        topic_path, msg_data
    )
    print("msg published")


def process_url(url, test):
    doc_id = generate_id_from_url(url)
    print("url_id: {}".format(url))
    try:
        urls_collection.add({}, doc_id)
        print("new doc created")
    except exceptions.AlreadyExists:
        print("exceptions.AlreadyExists")
        publish_id(doc_id, test)
        return
    summary, top_image, title = extract_data(url)
    doc_data = {
        "summary": summary,
        "top_image": top_image,
        "url": url,
        "title": title
    }
    print("adding record to db")
    urls_collection.document(doc_id).set(doc_data)
    print("added")
    publish_id(doc_id, test)


def process_function_all(event, context):
    print("function started")
    data = base64.b64decode(event["data"]).decode("utf-8")
    data_dict = json.loads(data)
    print("data: {}".format(str(data_dict)))
    process_url(data_dict["url"], data_dict["test"])


def main():
    process_url("https://thehustle.co/05282020-remote-work-pay/")


if "__main__" == __name__:
    main()