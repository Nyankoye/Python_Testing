import os
import sys
import unittest
from unittest.mock import patch
from datetime import datetime, timedelta
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from server import app


class TestServer(unittest.TestCase):

    clubs = [
                {
                    "name": "Simply Lift",
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
                        },
                        {
                            "name": "TEST Competitiion",
                            "date": "2021-10-22 13:30:00",
                            "numberOfPlaces": "13"
                        }
                    ]

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
            response = c.get('/book/'+competition_name+'/Simply Lift')
            competition_date = [competition['date'] for competition in self.competitions if competition['name'] == competition_name][0]
            
            date = datetime.now() - timedelta(days=2)
            if datetime.strptime(competition_date,'%Y-%m-%d %H:%M:%S') < date:
                assert b"This competition is passed you can&#39;t book places anymore" in response.data
            else:
                assert b'How many places' in response.data


if __name__ == '__main__':
    unittest.main()