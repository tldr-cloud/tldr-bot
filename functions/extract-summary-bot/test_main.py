import unittest
import main
import json


class TestMain(unittest.TestCase):

    def test_extract(self):
        expected_value = {
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            "\"Not only will Sleepy Joe Biden DEFUND THE POLICE, but he will DEFUND OUR MILITARY!"
                        ]
                    }
                }, {
                    "text": {
                        "text": [
                            "\"Sleepy Joe Biden and the Radical Left Democrats want to \"DEFUND THE POLICE\"."
                        ]
                    }
                }, {
                    "text": {
                        "text": [
                            "Bass's quote gets at the heart of the political problem for Democrats in the \"defund\""
                            " effort."
                        ]
                    }
                }, {
                    "text": {
                        "text": [
                            "The political problem for Democrats is this: They are now being backed into a corner by "
                            "activists who are demanding radical change."
                        ]
                    }
                }, {
                    "text": {
                        "text": [
                            "But it's not at all clear that a majority of the country supports a policy that would "
                            "defund the police."
                        ]
                    }
                }
            ]
        }

        result = main.extract_summary("https://www.cnn.com/2020/06/08/politics/defund-the-police-blm/index.html")
        result_dict = json.loads(result)
        self.assertDictEqual(result_dict, expected_value)


if __name__ == '__main__':
    unittest.main()
