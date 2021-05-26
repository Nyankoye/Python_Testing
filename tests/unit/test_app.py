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
    def test_purchasePlaces(self):
        """
            Given: A club secretary wishes to redeem points for a place in a competition
            When: The number of places is confirmed
            Then: The amount of club points available remain the same
            Expected: - The amount of points used should be deducted from the club's balance.
                      - They should be able to book no more than 12 places.
                      - The UI should prevent them from booking more than 12 places.
                      - They should not be able to redeem more points than available
        """

        # Create a test client using the Flask application configured for testing
        with app.test_client() as test_client:
            club_name = 'Simply Lift TEST'
            club_balance_before = [int(club['points']) for club in self.clubs if club['name'] == club_name][0]
            response = test_client.post('/purchasePlaces', data=dict(competition='Spring Festival TEST',
                                                                club=club_name,
                                                                places=7),
                                                                follow_redirects=True)

            # check if places required are no more than 12 places
            if int(request.form['places']) <= 12 and int(request.form['places']) > 0:
                # check if places required are no more than club points
                if club_balance_before < int(request.form['places']):
                    assert b"you don&#39;t have enough points!" in response.data
                else:
                    # check if the club current balance have changed
                    assert str(club_balance_before - int(request.form['places'])) in str(response.data)
                    assert b"Great-booking complete!" in response.data
            else:
                assert b"You may not reserve more than 12 places per competition!" in response.data

if __name__ == '__main__':
    unittest.main()