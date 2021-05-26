import os
import sys
import unittest
from unittest.mock import patch
from flask import request

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from server import app


class TestServer(unittest.TestCase):

    clubs = [
                {
                    "name": "Simply Lift TEST",
                    "email": "yves.loua@gmail.com",
                    "points": "5"
                },
                {
                    "name": "Iron Temple",
                    "email": "admin@irontemple.com",
                    "points": "4"
                },
            ]
    competitions = [
                        {
                            "name": "Spring Festival TEST",
                            "date": "2020-03-27 10:00:00",
                            "numberOfPlaces": "25"
                        },
                        {
                            "name": "Fall Classic",
                            "date": "2020-10-22 13:30:00",
                            "numberOfPlaces": "14"
                        }
                    ]

    @patch('server.clubs',clubs)
    @patch('server.competitions',competitions)
    def test_index(self):
        """
            When: A user types in an email not found in the system
            Then: App crashes
            Expected: Display an error message like "Sorry, that email wasn't found." 
        """

        # Create a test client using the Flask application configured for testing
        with app.test_client() as test_client:
            email = "admin@irontemple.com"
            club =  [club for club in self.clubs if club['email'] == email]
            response = test_client.post('/showSummary', data=dict(email=email),follow_redirects=True)
            if len(club)==0:
                assert b"Sorry, that email wasn&#39;t found" in response.data
            else:
                assert club[0]['email'] in str(response.data)

if __name__ == '__main__':
    unittest.main()