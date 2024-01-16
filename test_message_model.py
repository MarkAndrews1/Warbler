import os
from unittest import TestCase
from models import db, User, Message, Likes
from app import app

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

class MessageModelTestCase(TestCase):
    """Test views for messages."""

    def create_app(self):
        """Creates the app."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        """Create test client, add sample data."""
        with app.app_context():
            db.drop_all()
            db.create_all()

            self.uid = 94566
            u = User.signup("testing", "testing@test.com", "password", None)
            u.id = self.uid
            db.session.commit()

            self.u = User.query.get(self.uid)
            self.client = app.test_client()

    def tearDown(self):
        with app.app_context():
            res = super().tearDown()
            db.session.rollback()
            return res

def test_message_model(self):
    """Does basic model work?"""
    with app.app_context():
        m = Message(
            text="a warble",
            user_id=self.uid
        )

        db.session.add(m)
        db.session.commit()

        # Refresh the user object to ensure it's attached to the session
        self.u = User.query.get(self.uid)

        # User should have 1 message
        self.assertEqual(len(self.u.messages), 1)
        self.assertEqual(self.u.messages[0].text, "a warble")


    def test_message_likes(self):
        with app.app_context():
            m1 = Message(
                text="a warble",
                user_id=self.uid
            )

            m2 = Message(
                text="a very interesting warble",
                user_id=self.uid
            )

            u = User.signup("yetanothertest", "t@email.com", "password", None)
            uid = 888
            u.id = uid
            db.session.add_all([m1, m2, u])
            db.session.commit()

            u.likes.append(m1)

            db.session.commit()

            l = Likes.query.filter(Likes.user_id == uid).all()
            self.assertEqual(len(l), 1)
            self.assertEqual(l[0].message_id, m1.id)