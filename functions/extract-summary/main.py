import nltk
import requests
import utils
import urllib

from boilerpy3 import extractors
from newspaper import Article, fulltext
from flask import jsonify

nltk.download("punkt")

extractor = extractors.ArticleExtractor()
bearer = utils.get_bearer()


def generate_id_from_url(url):
    return url.replace("/", "_").replace(":", "_")


def extract_data(url, bert_summary):
    article = Article(url)
    print("article object created")
    article.download()
    print("download completed")
    article.parse()
    print("parsing completed")

    # Not always article extracts correctly text from the HTML. In case text has not been extracted using alternative
    # way.
    if not article.text or len(article.text) < 100:
        print("looks like article text is not extracted, most likely download has failed")
        html = urllib.request.urlopen(url).read() 
        article.text = fulltext(html)

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
    char_count = float(len(text))
    if (char_count * 0.1) > 550:
        ratio = 0.05
    else:
        ratio = 0.1

    resp = requests.post(url="http://10.128.0.2:5000/summarize?ratio={}".format(str(ratio)),
                         data=text.encode('utf-8'),
                         headers={
                             "Content-type": "text/plain"
                         }, timeout=60)
    return resp.json()["summary"]


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
        utils.inform_boss_about_an_error(str(e), "extract-summary")
