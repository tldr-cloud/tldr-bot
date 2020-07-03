from google.cloud import firestore

from flask import jsonify


urls_collection = firestore.Client().collection(u"urls")


def process_function_request(request):
    docs_stream = urls_collection.where(u"publish", u"==", False).where(u"published", u"==", False).where(u"new",
                                                                                                          u"==",
                                                                                                          True).stream()

    docs = [{
        "title": doc.get("title"),
        "url": doc.get("url"),
        "top_image": doc.get("top_image"),
        "summary": doc.get("summary")
    } for doc in docs_stream]
    return jsonify(docs)
