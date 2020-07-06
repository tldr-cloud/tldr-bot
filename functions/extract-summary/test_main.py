import unittest
import main


class TestMain(unittest.TestCase):

    def extraction_url_test(self, url, bert: bool):
        result = main.process_url(url, bert, main.cred.token)
        self.assertIsNotNone(result["summary"])
        self.assertIsNotNone(result["top_image"])
        self.assertIsNotNone(result["title"])
        self.assertIsNotNone(result["url"])

    def test_extract_non_bert(self):
        self.extraction_url_test("https://www.cnn.com/2020/06/08/politics/defund-the-police-blm/index.html", False)

    def test_extract_from_forbs_non_bert(self):
        self.extraction_url_test("https://www.forbes.com/sites/rachelsandler/2020/07/01/ceos-of-amazon-apple-facebook-"
                                  "and-google-agree-to-testify-at-house-antitrust-hearing/#466eb97872dc", False)

    def test_extract_from_cbr_non_bert(self):
        self.extraction_url_test("https://www.cbr.com/dceased-dead-planet-cyborg-batman-betrayal/", False)

    def test_extract_bert(self):
        self.extraction_url_test("https://www.cnn.com/2020/06/08/politics/defund-the-police-blm/index.html", True)

    def test_extract_from_forbs_bert(self):
        self.extraction_url_test("https://www.forbes.com/sites/rachelsandler/2020/07/01/ceos-of-amazon-apple-facebook-"
                                  "and-google-agree-to-testify-at-house-antitrust-hearing/#466eb97872dc", True)

    def test_extract_from_cbr_bert(self):
        self.extraction_url_test("https://www.cbr.com/dceased-dead-planet-cyborg-batman-betrayal/", True)

    def test_extract_from_engaged_bert(self):
        self.extraction_url_test("https://www.engadget.com/"
                                 "animal-crossing-nookphone-user-review-roundup-130033026.html", True)


if __name__ == '__main__':
    unittest.main()
