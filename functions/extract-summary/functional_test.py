import utils
import constants
import requests


test_url = "https://www.cnn.com/2020/06/08/politics/defund-the-police-blm/index.html"
bearer = utils.get_bearer()

resp = requests.post(url=constants.SUMMARY_EXTRACTOR_URL, json={"url": test_url, "bearer": bearer})
print(resp.json())

resp = requests.post(url=constants.SUMMARY_EXTRACTOR_URL)
print(resp.content)

resp = requests.post(
    url=constants.SUMMARY_EXTRACTOR_URL,
    json={
        "url": test_url,
        "bearer": bearer,
        "bert_summary": True
    })
print(resp.content)
print(resp.json())
