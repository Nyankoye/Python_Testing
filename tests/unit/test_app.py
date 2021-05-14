from server import app

def test_purchasePlaces():
    """
        Given: A club secretary wishes to redeem points for a place in a competition
        When: The number of places is confirmed
        Then: The amount of club points available remain the same
        Expected: The amount of points used should be deducted from the club's balance.
    """

    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        response = test_client.post('/purchasePlaces', data=dict(competition='Spring Festival',
                                                            club='Simply Lift',
                                                            places=2),
                                                            follow_redirects=True)
        print(response.data.decode('utf8'))
        assert response.status_code == 200
        assert b'Number of Places: 23' in response.data
        assert b'Points available: 11' in response.data