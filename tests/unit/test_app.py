import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from server import app, loadClubs, loadCompetitions


class TestServer(unittest.TestCase):
    clubs = [
        {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13"
        },
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4"
        },
        {"name": "She Lifts",
         "email": "kate@shelifts.co.uk",
         "points": "12"
         }
    ]
    competitions = [
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        }
    ]

    def test_loadClubs(self):
        clubs = loadClubs()
        assert self.clubs == clubs

    def test_loadCompetitions(self):
        competitions = loadCompetitions()
        assert self.competitions == competitions

    def test_index(self):
        with app.test_client() as test_client:
            response = test_client.get('/')
            assert response.status_code == 200
            assert b'Please enter your secretary email to continue' in response.data

    def test_logout(self):
        with app.test_client() as test_client:
            response = test_client.get('/logout')
            assert b'You should be redirected automatically to target URL:' in response.data


if __name__ == '__main__':
    unittest.main()
