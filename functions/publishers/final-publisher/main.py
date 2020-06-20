import utils
import publish_utils

from google.cloud import firestore


prod_chat_id = "@techtldr"
urls_collection = firestore.Client().collection(u"urls")


def publish_all_unpublished_docs():
    docs = urls_collection.where(u"publish", u"==", True).where(u"published", u"==", False).stream()

    for doc in docs:
        publish_utils.publish_doc(doc, prod_chat_id)
        updated_doc_data = {
            "publish": False,
            "published": True
        }
        urls_collection.document(doc.id).set(updated_doc_data, merge=True)
        print("doc found: {}".format(str(doc.id)))


def function_call_publish(event, context):
    try:
        print("final-publisher invoked")
        publish_all_unpublished_docs()
    except Exception as e:
        utils.inform_boss_about_an_error(str(e), "final-publisher")


if "__main__" == __name__:
    publish_all_unpublished_docs()