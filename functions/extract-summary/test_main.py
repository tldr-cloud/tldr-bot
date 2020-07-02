import unittest
import main


class TestMain(unittest.TestCase):

    def test_extract(self):
        result = main.process_url("https://www.cnn.com/2020/06/08/politics/defund-the-police-blm/index.html", False)
        self.assertIsNotNone(result["summary"])
        self.assertIsNotNone(result["top_image"])
        self.assertIsNotNone(result["title"])
        self.assertIsNotNone(result["url"])

    def test_extract_from_forbs(self):
        result = main.process_url("https://www.forbes.com/sites/rachelsandler/2020/07/01/ceos-of-amazon-apple-facebook-"
                                  "and-google-agree-to-testify-at-house-antitrust-hearing/#466eb97872dc", False)
        self.assertIsNotNone(result["summary"])
        self.assertIsNotNone(result["top_image"])
        self.assertIsNotNone(result["title"])
        self.assertIsNotNone(result["url"])

    def test_extract_from_cbr(self):
        result = main.process_url("https://www.cbr.com/dceased-dead-planet-cyborg-batman-betrayal/", False)
        self.assertIsNotNone(result["summary"])
        self.assertIsNotNone(result["top_image"])
        self.assertIsNotNone(result["title"])
        self.assertIsNotNone(result["url"])


if __name__ == '__main__':
    unittest.main()
