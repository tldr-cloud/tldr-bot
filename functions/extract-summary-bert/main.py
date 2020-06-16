import base64

import nltk
import requests
import utils

from boilerpy3 import extractors
from newspaper import Article
from flask import jsonify

nltk.download("punkt")

extractor = extractors.ArticleExtractor()
bearer = utils.get_bearer()


def generate_id_from_url(url):
     return url.replace("/", "_").replace(":", "_")


def extract_data(url):
     article = Article(url)
     print("article object created")
     article.download()
     print("download completed")
     article.parse()
     print("parsing completed")
     if not article.text or len(article.text) < 100:
         article.text = extractor.get_content(article.html)

     try:
         print("attempting to extract summary")
         summary = attempt_extract_summary_bert(article.text)
         print("bert summary extracted")
     except Exception as e:
         utils.inform_boss_about_an_error(str(e), "extract-summary")
         article.nlp()
         summary = article.summary
         print("good old summary extracted")
     # article.nlp()
     # summary = article.summary
     print("nlp step completed")
     return (summary, article.top_image, article.title)


def attempt_extract_summary_bert(text):
    resp = requests.post(url="http://10.128.0.2:5000/summarize?ratio=0.05", data=text.encode('utf-8'), headers={
        "Content-type": "text/plain"
    }, timeout=60)
    return resp.json()["summary"]


def process_url(url):
    summary, top_image, title = extract_data(url)
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
        return jsonify(process_url(url))
    else:
        return f"There is not url key in the request!"


def process_call(request):
    try:
        return process_request(request)
    except Exception as e:
        utils.inform_boss_about_an_error(str(e), "extract-summary")
