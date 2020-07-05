import unittest
import main
import utils

from google.cloud import firestore


class TestMain(unittest.TestCase):

    def test_process_url_doc_gc(self):
        urls_collection = firestore.Client().collection(u"urls")

        url = "https://test.com/1234"
        doc_id = utils.generate_id_from_url(url)
        try:
            main.process_url(doc_id, True)
            raise ValueError("looks like process not crashed")
        except:
            if urls_collection.document(doc_id).get().exists:
                raise ValueError("doc still exist!")

if __name__ == '__main__':
    unittest.main()
