from google.cloud import firestore

urls_collection = firestore.Client().collection(u"urls")


def get_yes_or_no(text):
    answer = input(text)
    if not answer:
        return False

    answer = answer.lower()
    if answer == "y":
        return True
    elif answer == "n":
        return False
    else:
        print("yes or no only")
        return get_yes_or_no(text)


def ask_to_approve(title, url, top_image, text):
    print("title: {}".format(title))
    print("URL: {}".format(url))
    print("top_image url: {}".format(top_image))
    print("################# SUMMARY ###############")
    print(text)
    print("################### END #################")

    return get_yes_or_no("Approve? (y/N)")


def main():
    docs = urls_collection.where(u"publish", u"==", False).where(u"published", u"==", False).where(u"new",
                                                                                                   u"==",
                                                                                                   True).stream()
    for doc in docs:
        title = doc.get("title")
        url = doc.get("url")
        top_image = doc.get("top_image")
        text = doc.get("summary")
        if ask_to_approve(title, url, top_image, text):
            publish = True
            print("approved")
        else:
            publish = False
            print("skipping")

        updated_doc_data = {
            "publish": publish,
            "new": False
        }
        urls_collection.document(doc.id).set(updated_doc_data, merge=True)


if "__main__" == __name__:
    main()
