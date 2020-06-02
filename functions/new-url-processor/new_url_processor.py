import base64
import nltk

from boilerpy3 import extractors

from google.cloud import firestore
from google.cloud import pubsub_v1
from google.api_core import exceptions

from newspaper import Article

nltk.download("punkt")

urls_collection = firestore.Client().collection(u"urls")
extractor = extractors.ArticleExtractor()

publisher = pubsub_v1.PublisherClient()
topic = "processed-urls"
topic_path = publisher.topic_path("tldr-278619", topic)


def generate_id_from_url(url):
     return url.replace("/", "_").replace(":", "_")


def extract_data(url):
     article = Article(url)
     print("article object created")
     article.download()
     print("download completed")
     article.parse()
     print("parsing completed")
     if not article.text or len(article.text) < 100:
         article.text = extractor.get_content(article.html)
     article.nlp()
     print("nlp step completed")
     return (article.summary, article.top_image, article.title)


def publish_id(doc_id):
    msg_data = doc_id.encode("utf-8")
    publisher.publish(
        topic_path, msg_data
    )
    print("msg published")


def process_url(url):
    doc_id = generate_id_from_url(url)
    print("url_id: {}".format(url))
    try:
        urls_collection.add({}, doc_id)
        print("new doc created")
    except exceptions.AlreadyExists:
        print("exceptions.AlreadyExists")
        publish_id(doc_id)
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
    publish_id(doc_id)


def process_function_all(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    print("function started")
    url = base64.b64decode(event["data"]).decode("utf-8")
    print("url: {}".format(url))
    process_url(url)


def main():
    process_url("https://thehustle.co/05282020-remote-work-pay/")


if "__main__" == __name__:
    main()