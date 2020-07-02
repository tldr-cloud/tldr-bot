import constants
import telegram

from google.cloud import secretmanager
from google.cloud import firestore
from telegram import utils


client = secretmanager.SecretManagerServiceClient()
secret_name = client.secret_version_path(constants.PROJECT_ID, constants.TELEGRAM_TLDR_BOT_SECRET_ID, "1")
secret_response = client.access_secret_version(secret_name)
payload = secret_response.payload.data.decode('UTF-8')
bot = telegram.Bot(payload)

urls_collection = firestore.Client().collection(u"urls")


def publish(chat_id, url, text, title, top_image):
    text = utils.helpers.escape_markdown(text, version=2)

    bot.send_message(chat_id=chat_id,
                     text='<b><a href="{url}">{title}</a></b>.'.format(url=url, title=title),
                     parse_mode=telegram.ParseMode.HTML,
                     disable_web_page_preview=True)
    if top_image:
        bot.send_photo(chat_id=chat_id, photo=top_image)
    bot.send_message(chat_id=chat_id, text=text, parse_mode=telegram.ParseMode.MARKDOWN_V2,
                     disable_web_page_preview=True)


def publish_doc_id(doc_id, chat_id):
    doc_ref = urls_collection.document(doc_id)
    doc = doc_ref.get()
    if not doc.exists:
        return
    publish_doc(doc, chat_id)


def publish_doc(doc, chat_id):
    try:
        top_image = doc.get("top_image")
    "pt Exception as e:
        print(str(e))
        top_image = None
    title = doc.get("title")
    url = doc.get("url")
    text = ""
    points = doc.get("summary").split("\n")
    if len(points) > 1:
        for paragraph in points:
            text = "{}\n* {}".format(text, paragraph)
    else:
        text = doc.get("summary")
    publish(chat_id, url, text, title, top_image)
