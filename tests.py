import unittest

from party import app
from model import db, example_data, connect_to_db


class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn("board games, rainbows, and ice cream sundaes", result.data)

    def test_no_rsvp_yet(self):
        """Tests homepage to see RSVP form and no details if not RSVP yet"""
        
        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertNotIn('123 Magic Unicorn Way', result.data)
        self.assertIn('Please RSVP', result.data)

    def test_rsvp(self):
        """Tests homepage to see party details if already RSVP"""
        result = self.client.post("/rsvp",
                                  data={"name": "Jane",
                                        "email": "jane@jane.com"},
                                  follow_redirects=True)

        self.assertEqual(result.status_code, 200)        
        self.assertIn('123 Magic Unicorn Way', result.data)
        self.assertNotIn('Please RSVP', result.data)


class PartyTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'

        with self.client as c:
            with c.session_transaction() as sess:
                sess['RSVP'] = True

        # Connect to test database (uncomment when testing database)
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data (uncomment when testing database)
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        # (uncomment when testing database)
        db.session.close()
        db.drop_all()

    def test_games(self):
        """Test to see if game name and description loads on page"""
        result = self.client.get("/games")
        self.assertEqual(result.status_code, 200)
        self.assertIn('Donkey', result.data)
        self.assertIn('Tic', result.data)


if __name__ == "__main__":
    unittest.main()
