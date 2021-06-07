import os
import sys
import unittest
from unittest.mock import patch
from flask import request
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from server import app

clubs = [
            {
                "name": "Simply Lift TEST",
                "email": "yves.loua@gmail.com",
                "points": "6"
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
                        "numberOfPlaces": "13"
                    },
                    {
                        "name": "TEST Competitiion",
                        "date": "2021-10-22 13:30:00",
                        "numberOfPlaces": "13"
                    }
                ]
class Test_showClubs(unittest.TestCase):
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
            self.check_list_elements_in_response(clubs, response)

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

class Test_purchasePlaces(unittest.TestCase):
    """
        Given: A club secretary wishes to redeem points for a place in a competition
        When: The number of places is confirmed
        Then: The amount of club points available remain the same
        Expected: - The amount of points used should be deducted from the club's balance.
                - They should be able to book no more than 12 places.
                - The UI should prevent them from booking more than 12 places.
                - They should not be able to redeem more points than available
    """
    @patch('server.clubs',clubs)
    @patch('server.competitions',competitions)
    def test_good_booking(self):
        # Create a test client using the Flask application configured for testing
        with app.test_client() as test_client:
            club_name = 'Simply Lift TEST'
            club_balance_before = [int(club['points']) for club in clubs if club['name'] == club_name][0]
            response = test_client.post('/purchasePlaces', data=dict(competition='TEST Competitiion',
                                                                club=club_name,
                                                                places=2),
                                                                follow_redirects=True)
            assert response.status_code == 200
            # check if the club current balance have changed
            assert str(club_balance_before - int(request.form['places'])*3) in str(response.data)
            assert b"Great-booking complete!" in response.data
    
    @patch('server.clubs',clubs)
    @patch('server.competitions',competitions)
    def test_not_enough_point(self):
        with app.test_client() as test_client:
            club_name = 'Simply Lift TEST'
            response = test_client.post('/purchasePlaces', data=dict(competition='TEST Competitiion',
                                                                club=club_name,
                                                                places=3),
                                                                follow_redirects=True)

            assert b"you don&#39;t have enough points!" in response.data
    
    @patch('server.clubs',clubs)
    @patch('server.competitions',competitions)
    def test_not_more_than_12(self):
        with app.test_client() as test_client:
            club_name = 'Simply Lift TEST'
            response = test_client.post('/purchasePlaces', data=dict(competition='TEST Competitiion',
                                                                club=club_name,
                                                                places=13),
                                                                follow_redirects=True)
        assert b"You may not reserve more than 12 places per competition!" in response.data


class Test_book(unittest.TestCase):
    """
        When: They book a number of places on a competition that has happened in the past
        Then: They receive a confirmation message
        Expected: They should not be able to book a place on a post-dated competition 
        (but past competitions should be visible). 
    """

    @patch('server.competitions', competitions)
    @patch('server.clubs', clubs)
    def test_competition_not_passed(self):
        with app.test_client() as c:
            response = c.get('/book/TEST Competitiion/Simply Lift TEST')
            assert b'How many places' in response.data
    
    @patch('server.competitions', competitions)
    @patch('server.clubs', clubs)
    def test_competition_passed(self):
        with app.test_client() as c:
            response = c.get('/book/Spring Festival TEST/Simply Lift TEST')
            assert b"This competition is passed you can&#39;t book places anymore" in response.data

class Test_showSummary(unittest.TestCase):
    """
        When: A user types in an email not found in the system
        Then: App crashes
        Expected: Display an error message like "Sorry, that email wasn't found." 
    """

    @patch('server.clubs',clubs)
    @patch('server.competitions',competitions)
    def test_email_good(self):
        # Create a test client using the Flask application configured for testing
        with app.test_client() as test_client:
            email = "admin@irontemple.com"
            club =  [club for club in clubs if club['email'] == email]
            response = test_client.post('/showSummary', data=dict(email=email),follow_redirects=True)
            assert club[0]['email'] in str(response.data)


    @patch('server.clubs',clubs)
    @patch('server.competitions',competitions)
    def test_email_bad(self):
        with app.test_client() as test_client:
            response = test_client.post('/showSummary', data=dict(email="vgvhh"),follow_redirects=True)
            assert b"Sorry, that email wasn&#39;t found" in response.data
