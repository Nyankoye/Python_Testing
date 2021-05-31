import os
import sys
import unittest
from unittest.mock import patch
from flask import request
from datetime import datetime, timedelta
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
                        },
                        {
                            "name": "TEST Competitiion",
                            "date": "2021-10-22 13:30:00",
                            "numberOfPlaces": "13"
                        }
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
            assert str(club['points']) in response.data.decode('utf8')

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
            response = test_client.post('/purchasePlaces', data=dict(competition='TEST Competitiion',
                                                                club=club_name,
                                                                places=4),
                                                                follow_redirects=True)
            assert response.status_code == 200
            # check if the club current balance have changed
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
    
    @patch('server.competitions', competitions)
    @patch('server.clubs', clubs)
    def test_book(self):
        """
            When: They book a number of places on a competition that has happened in the past
            Then: They receive a confirmation message
            Expected: They should not be able to book a place on a post-dated competition 
            (but past competitions should be visible). 
        """
        
        with app.test_client() as c:
            competition_name = "TEST Competitiion"
            response = c.get('/book/'+competition_name+'/Simply Lift TEST')
            competition_date = [competition['date'] for competition in self.competitions if competition['name'] == competition_name][0]
            
            date = datetime.now() - timedelta(days=2)
            if datetime.strptime(competition_date,'%Y-%m-%d %H:%M:%S') < date:
                assert b"This competition is passed you can&#39;t book places anymore" in response.data
            else:
                assert b'How many places' in response.data

if __name__ == '__main__':
    unittest.main()