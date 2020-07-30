import datetime

from google.cloud import firestore

urls_collection = firestore.Client().collection(u"urls")


def get_answer_from(text, answer_space, default):
    answer = input(text)
    if not answer:
        return default

    answer = answer.lower()
    if answer in answer_space:
        return answer
    else:
        return get_answer_from(text, answer_space, default)


def ask_to_approve(title, url, top_image, text):
    print("title: {}".format(title))
    print("URL: {}".format(url))
    print("top_image url: {}".format(top_image))
    print("################# SUMMARY ###############")
    print(text)
    print("################### END #################")

    answer = get_answer_from("Approve? (y/N)", "yn", "n")
    if answer == "y":
        return True
    elif answer == "n":
        return False


def main():
    docs_stream = urls_collection.where(u"publish", u"==", False).where(u"published", u"==", False).where(u"new",
                                                                                                          u"==",
                                                                                                          True).stream()
    # Stream is timing out so we need to convert lazy stream to a normal list
    # this is ok since we never will have huge list for a review (or this is a bug that needs to be fixed)
    docs = [doc for doc in docs_stream]
    for doc in docs:
        title = doc.get("title")
        url = doc.get("url")
        top_image = doc.get("top_image")
        text = doc.get("summary")
        if ask_to_approve(title, url, top_image, text):
            publish = True
            print("approved")
            skip_reason = None
        else:
            publish = False
            skip_reason = get_answer_from("Reason? (B)ad news/already (p)ublished/news is good bud (s)ummary is bad",
                                          "bps", "b")
            print("skipped with the reason: {}".format(skip_reason))

        updated_doc_data = {
            "publish": publish,
            "new": False,
            "skip_reason": skip_reason,
            "date": datetime.datetime.now()
        }
        urls_collection.document(doc.id).set(updated_doc_data, merge=True)


if "__main__" == __name__:
    main()
