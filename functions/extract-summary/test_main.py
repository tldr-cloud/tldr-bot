import unittest
import main


class TestMain(unittest.TestCase):

    def test_extract(self):
        result = main.process_url("https://www.cnn.com/2020/06/08/politics/defund-the-police-blm/index.html", False)
        self.assertIsNotNone(result["summary"])
        self.assertIsNotNone(result["top_image"])
        self.assertIsNotNone(result["title"])
        self.assertIsNotNone(result["url"])


if __name__ == '__main__':
    unittest.main()
