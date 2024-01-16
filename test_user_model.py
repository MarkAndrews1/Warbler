import os
from unittest import TestCase
from flask import g

from models import db, User

# Set the environment variable before importing the app
os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# Import app after setting the environment variable
from app import app

class UserModelTestCase(TestCase):
    """Test views for messages."""

    def create_app(self):
        """Creates the app."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        """Creates test client, add sample data."""
        self.client = app.test_client()

        # Establishs a Flask application context before creating tables
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Tear down the test environment."""
        # Pop the Flask application context after dropping tables
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

        self.assertEqual(u.email, "test@test.com")
        self.assertEqual(u.username, "testuser")
        self.assertEqual(u.image_url, "/static/images/default-pic.png")
        self.assertEqual(u.header_image_url, "/static/images/warbler-hero.jpg")

    def test_user_following(self):
        """Test following and followers relationships"""

        # Creates users
        user1 = User(
            username="user1",
            email="user1@gmail.com",
            password='password1')
        
        user2 = User(
            username="user2",
            email="user2@gmail.com",
            password='password2')
        db.session.add_all([user1,user2])
        db.session.commit()


        # Make user1 follow user2
        user1.following.append(user2)
        db.session.commit()

        # Test following
        self.assertEqual(len(user1.following), 1)
        self.assertEqual(len(user2.followers), 1)
        self.assertEqual(user1.is_following(user2), True)
        self.assertEqual(user2.is_followed_by(user1), True)

        # Make user1 stop following user2
        user1.following.remove(user2)
        db.session.commit()

        # Test unfollowing
        self.assertEqual(len(user1.following), 0)
        self.assertEqual(len(user2.followers), 0)
        self.assertEqual(user1.is_following(user2), False)
        self.assertEqual(user2.is_followed_by(user1), False)

    def test_user_login(self):
        '''Tests login'''

        u = User(
            email="test@test.com",
            username="testuser",
            password="password"
        )
        db.session.add(u)
        db.session.commit()

        # Test if credentails are correct
        res = self.client.post('/login', data={'username': 'testuser', 'password': 'password'})
        self.assertEqual(res.status_code, 200)

    def test_user_logout(self):
        '''Test Logout'''

        u = User(
            email="test@test.com",
            username="testuser",
            password="password"
        )
        db.session.add(u)
        db.session.commit()

        # Login the user
        with self.client:
            self.client.post('/login', data={'username': 'testuser', 'password': 'testpassword'}, follow_redirects=True)

            # Test logout
            response = self.client.get('/logout', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

