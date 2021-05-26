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
                    "email": "john@simplylift_test.co",
                    "points": "13"
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
    def test_purchasePlaces(self):
        """
            Given: A club secretary wishes to redeem points for a place in a competition
            When: The number of places is confirmed
            Then: The amount of club points available remain the same
            Expected: The amount of points used should be deducted from the club's balance.
        """

        # Create a test client using the Flask application configured for testing
        with app.test_client() as test_client:
            response = test_client.post('/purchasePlaces', data=dict(competition='Spring Festival TEST',
                                                                club='Simply Lift TEST',
                                                                places=13),
                                                                follow_redirects=True)
            if int(request.form['places']) > 12:
                assert b"You may not reserve more than 12 places per competition!" in response.data
            else:
                assert b"Great-booking complete!" in response.data

if __name__ == '__main__':
    unittest.main()