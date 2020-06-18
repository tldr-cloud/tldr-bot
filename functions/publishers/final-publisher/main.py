import base64
import utils
import publish_utils

prod_chat_id = "@techtldr"


def function_call_publish(event, context):
    try:
        print("final-publisher invoked")
        doc_id = base64.b64decode(event["data"]).decode("utf-8")
        publish_utils.publish_doc(doc_id, prod_chat_id)
    except Exception as e:
        utils.inform_boss_about_an_error(str(e), "final-publisher")
