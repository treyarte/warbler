"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows
from sqlalchemy.exc import IntegrityError

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app


app.config["SQLALCHEMY_ECHO"] = False
# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

        u = User.signup(
            "testuser",
            "test@test.com",
            "HASHED_PASSWORD",
            None
        )

        u1 = User.signup(
            "userTest1",
            "usertest1@test.com",
            "secret_password",
            None
        )

        u2 = User.signup(
            "userTest2",
            "usertest2@test.com",
            "This_password",
            None
        )

        
    
        db.session.commit()

        self.u = u
        self.u1 = u1
        self.u2 = u2

    def tearDown(self):
        """Get rid of any previous transactions"""
        db.session.rollback()

    def test_user_model(self):
        """Does basic model work?"""

        # User should have no messages & no followers
        self.assertEqual(len(self.u.messages), 0)
        self.assertEqual(len(self.u.followers), 0)

        #User repr should work correctly
        self.assertEqual(f'{self.u}', f"<User #{self.u.id}: {self.u.username}, {self.u.email}>")

    def test_user_following(self):
        """Test following feature"""

        #make sure user1 is not following user2
        self.assertFalse(self.u1.is_following(self.u2))
        self.assertFalse(self.u2.is_followed_by(self.u1))

        self.u1.following.append(self.u2)
        db.session.commit()

        #check if user1 is following user2 and user2 have user1 as a follower
        self.assertTrue(self.u1.is_following(self.u2))
        self.assertTrue(self.u2.is_followed_by(self.u1))
        self.assertFalse(self.u1.is_followed_by(self.u2))
    
    def test_user_creation_same_username(self):
        """Tests that a user cannot be created with the same username"""

        #check if error is raised when trying to create users with the same username 
        with self.assertRaises(IntegrityError):
            new_u = User.signup("userTest2","123@123.com",  "asdfgh", None)
            db.session.add(new_u)
            db.session.commit()
        
    def test_user_creation_no_email(self):
        """Test that user cannot be created without an email"""
        with self.assertRaises(IntegrityError):
            new_u = User(username="newUsername123", password="asdfgh")
            
            db.session.add(new_u)
            db.session.commit()
    
    def test_user_authentication(self):
        """Test if a user is returned when authenticated"""

        u = User.authenticate("falseuser", "falsepassword")
        u2 = User.authenticate("userTest2", "This_password")

        self.assertFalse(u)
        self.assertTrue(u2)
        self.assertEqual(u2, self.u2)

