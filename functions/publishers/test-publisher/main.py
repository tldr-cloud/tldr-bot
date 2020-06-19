import base64
import utils
import publish_utils

test_chat_id = "@tldrtest"


def function_call_publish(event, context):
    try:
        print("final-publisher invoked")
        doc_id = base64.b64decode(event["data"]).decode("utf-8")
        print("msg data: {}".format(doc_id))
        publish_utils.publish_doc_id(doc_id, test_chat_id)
    except Exception as e:
        utils.inform_boss_about_an_error(str(e), "test-publisher")


if "__main__" == __name__:
    publish_utils.publish_doc("https___9to5mac.com_2020_06_15_apple-developer-app-updated-ahead-of-wwdc-2020-with-macos-version_amp_", test_chat_id)
