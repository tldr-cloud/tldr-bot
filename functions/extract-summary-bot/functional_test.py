import utils
import constants
import requests


test_url = ("https://www.extremetech.com/internet/"
            "311436-windows-10-begins-showing-ads-for-edge-when-you-search-for-other-browsers")


request = {
  "responseId": "f1e7b49d-b0d2-4dbc-973e-bc74de68398c-2db64ae0",
  "queryResult": {
    "queryText": test_url,
    "parameters": {
      "url": test_url
    },
    "allRequiredParamsPresent": True,
    "fulfillmentText": "Looks like cloud function is not yet started (cold start problem :( ), please try again in"
                       " ~5sec",
    "fulfillmentMessages": [
      {
        "text": {
          "text": [
            "Looks like cloud function is not yet started (cold start problem :( ), please try again in ~5sec"
          ]
        }
      }
    ],
    "outputContexts": [
      {
        "name": "projects/tldr-bot-gptwtw/agent/sessions/41486328-b492-9400-e1fd-0f12d9d66fcd/contexts/"
                "__system_counters__",
        "parameters": {
          "no-input": 0,
          "no-match": 0,
          "url": test_url,
          "url.original": test_url
        }
      }
    ],
    "intent": {
      "name": "projects/tldr-bot-gptwtw/agent/intents/b0cfbc7f-f7b1-4a85-b258-2a4679594675",
      "displayName": "Summarize URL",
      "endInteraction": True
    },
    "intentDetectionConfidence": 1,
    "languageCode": "en"
  },
  "originalDetectIntentRequest": {
    "payload": {}
  },
  "session": "projects/tldr-bot-gptwtw/agent/sessions/41486328-b492-9400-e1fd-0f12d9d66fcd"
}

bearer = utils.get_bearer()

resp = requests.post(url=constants.SUMMARY_BOT_URL, json=request, headers={"bearer": bearer})
print(resp.json())
resp = requests.post(url=constants.SUMMARY_BOT_URL)
print(resp.content)