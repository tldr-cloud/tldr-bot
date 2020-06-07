import nltk

from boilerpy3 import extractors

from newspaper import Article

from flask import jsonify

nltk.download("punkt")

extractor = extractors.ArticleExtractor()


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
     article.nlp()
     print("nlp step completed")
     return (article.summary, article.top_image, article.title)


def process_url(url):
    summary, top_image, title = extract_data(url)
    doc_data = {
        "summary": summary,
        "top_image": top_image,
        "url": url,
        "title": title
    }
    return doc_data


def process_call(request):
    request_json = request.get_json()
    if "url" in request_json:
        url = request_json["url"]
        return jsonify(process_url(url))
    else:
        return f"There is not url key in the request!"
