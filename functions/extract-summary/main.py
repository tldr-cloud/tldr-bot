import nltk
import requests
import utils
import urllib
import traceback
import time

from random import randint
from time import sleep

import google.auth
import google.auth.transport.requests

from newspaper import Article
from newspaper.article import ArticleDownloadState
from flask import jsonify

nltk.download("punkt")

bearer = utils.get_bearer()

cred = None
latest_cred_refresh_sec = None
token_refresh_interval = 60 * 5


def maybe_initiate_credentials():
    global cred
    global latest_cred_refresh_sec

    def refresh_token():
        global latest_cred_refresh_sec
        global cred
        cred, projects = google.auth.default()
        auth_req = google.auth.transport.requests.Request()
        cred.refresh(auth_req)
        latest_cred_refresh_sec = time.time()

    if not latest_cred_refresh_sec:
        refresh_token()
    elif time.time() - latest_cred_refresh_sec >= token_refresh_interval:
        refresh_token()


maybe_initiate_credentials()


def extract_data(url, bert_summary):
    article = Article(url)
    print("article object created")
    article.download()
    if article.download_state != ArticleDownloadState.SUCCESS:
       article.html = urllib.request.urlopen(url).read()
       # Hacking the library
       article.download_state = ArticleDownloadState.SUCCESS
    print("download completed")
    article.parse()
    print("parsing completed")

    top_image = article.top_image
    title = article.title

    if bert_summary:
        print("extracting bert summary")
        summary = extract_bert_summary(article.text)
    else:
        print("extracting short summary")
        summary = extract_short_summary(article)

    return summary, top_image, title


def extract_bert_summary(text):
    maybe_initiate_credentials()
    token = cred.token
    char_count = float(len(text))
    if (char_count * 0.1) > 550:
        ratio = 0.05
    else:
        ratio = 0.1

    print("ratio for the summary: {}".format(str(ratio)))
    print("length of the original text is: {}".format(str(len(text))))

    print("about to request cloud AI Prediction")
    retry_count = 0
    while retry_count < 5:
        resp = requests.post(url="https://alpha-ml.googleapis.com/v1/projects/tldr-278619/models/bert_summaryzer/"
                                 "versions/v5:predict",
                             json={
                                 "summary": text,
                                 "ratio": ratio
                             },
                             headers={
                                 "Content-type": "application/json",
                                 "Authorization": "Bearer {}".format(token)
                             },
                             timeout=240)
        resp_json = resp.json()
        print("resp from cloud AI Prediction: {}".format(str(resp_json)))
        if "error" in resp_json:
            error_code = resp_json["error"]["code"]
            if error_code  == 503:
                print("prediction error, retrying")
                retry_count = retry_count + 1
                time.sleep(5)
                continue
            elif error_code == 429:
                # 429 means: "Rate of traffic exceeds serving capacity"
                sleep(randint(1, 5))
                continue
        break

    if "summary" not in resp_json:
        raise ValueError("there is no summary in the response from Cloud AI prediction")

    return resp_json["summary"]


def extract_short_summary(article):
    article.nlp()
    return article.summary


def process_url(url, bert_summary):
    summary, top_image, title = extract_data(url, bert_summary)
    doc_data = {
        "summary": summary,
        "top_image": top_image,
        "url": url,
        "title": title
    }
    return doc_data


def process_request(request):
    request_json = request.get_json()
    if not request_json:
        # Assuming this is a request from cloud scheduler to keep function HOT
        # Find a better way to do this
        return "PING_OK"

    if "url" in request_json:
        url = request_json["url"]
        bert_summary = request_json.get("bert_summary", False)
        return jsonify(process_url(url, bert_summary))
    else:
        return f"There is not url key in the request!"


def process_call(request):
    try:
        return process_request(request)
    except Exception as e:
        tb = traceback.format_exc()
        exception_str = "{}\n{}".format(str(e), tb)
        utils.inform_boss_about_an_error("url: {}, error: {}".format(str(request.get_json()["url"]), exception_str),
                                         "extract-summary")
        # raising exception will force Cloud Function to have a cold start with the next execution.
        traceback.print_exc()
