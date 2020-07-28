import json


def process_call(request):
    bot_resp = {
      "payload": {
        "google": {
          "expectUserResponse": True,
          "richResponse": {
            "items": [
              {
                "simpleResponse": {
                  "textToSpeech": "news one"
                }
              }
            ]
          }
        }
      }
    }

    return json.dumps(bot_resp)
