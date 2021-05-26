import os
import sys
import unittest
from unittest.mock import patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from server import app


class TestServer(unittest.TestCase):

    clubs = [
                {
                    "name": "Simply Lift TEST",
                    "email": "john@simplylift_test.co",
                    "points": "13"
                },
                {
                    "name": "Iron Temple",
                    "email": "admin@irontemple.com",
                    "points": "4"
                },
            ]

    @patch('server.clubs', clubs)
    def test_showClubs(self):
        """
        WHEN a secretary logs into the app
        THEN They should be able to see the list of clubs and their associated current points balance
        """

        with app.test_client() as test_client:
            response = test_client.get('/clubs')
            assert response.status_code == 200 
            # check if all items of the list are in response.data
            self.check_list_elements_in_response(self.clubs, response)

    @staticmethod
    def check_list_elements_in_response(iterable, response):
        """
            This method allow to check if all elements of an iterable of dict are 
            in response.data

            :param iterable: its a list of dict
            :param response: its a response from a client
            :type iterable: list
            :type response: flask.wrappers.Response
        """
        for club in iterable:
            assert club['name'] in response.data.decode('utf8')
            assert club['points'] in response.data.decode('utf8')


if __name__ == '__main__':
    unittest.main()
