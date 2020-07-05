import nltk
import requests
import utils
import urllib
import traceback

import google.auth
import google.auth.transport.requests

from newspaper import Article
from newspaper.article import ArticleDownloadState
from flask import jsonify

nltk.download("punkt")

bearer = utils.get_bearer()

cred = None


def maybe_initiate_credentials():
    global cred
    if not cred:
        cred, projects = google.auth.default()
        auth_req = google.auth.transport.requests.Request()
        cred.refresh(auth_req)


maybe_initiate_credentials()


def generate_id_from_url(url):
    return url.replace("/", "_").replace(":", "_")


def extract_data(url, bert_summary, token):
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
        summary = extract_bert_summary(article.text, token)
    else:
        print("extracting short summary")
        summary = extract_short_summary(article)

    return summary, top_image, title


def extract_bert_summary(text, token):
    char_count = float(len(text))
    if (char_count * 0.1) > 550:
        ratio = 0.05
    else:
        ratio = 0.1

    print("about to request cloud AI Prediction")
    resp = requests.post(url="https://alpha-ml.googleapis.com/v1/projects/tldr-278619/models/bert_summaryzer:predict",
                         json={
                             "summary": text,
                             "ratio": ratio
                         },
                         headers={
                             "Content-type": "application/json",
                             "Authorization": "Bearer {}".format(token)
                         },
                         timeout=240)
    print("resp from cloud AI Prediction: {}".format(str(resp.json())))
    return resp.json()["summary"]


def extract_short_summary(article):
    article.nlp()
    return article.summary


def process_url(url, bert_summary, token=cred.token):
    summary, top_image, title = extract_data(url, bert_summary, token)
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
    # Yes the following three lines are horrible, there is a reason for this, and it will be fixed ASAP.
    bearer_from_request = request_json["bearer"]
    if bearer_from_request != bearer:
        return "error"
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
