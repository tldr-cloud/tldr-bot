import json
import datetime

from google.cloud import firestore

urls_collection = firestore.Client().collection(u"urls")


def process_call(request):
  today = datetime.datetime.now()
  delta = datetime.timedelta(days=2)
  target = today - delta
  docs = urls_collection.where(u"published", u"==", True).where("date", ">", target).stream()
  titles = []
  for doc in docs:
    print("doc found: {}".format(str(doc.id)))
    titles.append(doc.get("title"))

  final_text = ". ".join(titles)

  bot_resp = {
    "payload": {
      "google": {
        "expectUserResponse": False,
        "richResponse": {
          "items": [
            {
              "simpleResponse": {
                "textToSpeech": final_text
              }
            }
          ]
        }
      }
    }
  }

  return json.dumps(bot_resp)


if __name__ == "__main__":
  print(process_call(None))