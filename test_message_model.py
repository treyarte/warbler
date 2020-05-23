"""Message model tests"""

import os
from unittest import TestCase

from models import db, User, Message, Likes
from sqlalchemy.exc import IntegrityError

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app

app.config["SQLALCHEMY_ECHO"] = False

db.create_all()

class MessageModelTestCase(TestCase):
    """Test cases for the message model"""

    def setUp(self):
        """add sample data"""
        Message.query.delete()
        User.query.delete()
        Likes.query.delete()

        self.client = app.test_client()

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

        db.session.add_all([u1,u2])
        db.session.commit()

        self.u1 = u1
        self.u2 = u2
        
        msg1 = Message(user_id=u1.id, text="This is a test message.")
        msg2 = Message(user_id=u2.id, text="Testing testing 1, 2, 3.")
     

        db.session.add_all([msg1, msg2])
        db.session.commit()

        self.msg1 = msg1
        self.msg2 = msg2


    def tearDown(self):
        """remove the previous transaction"""
        db.session.rollback()

    def testMessageCreation(self):
        """Testing the creation of messages"""

        #test message with invalid user
        with self.assertRaises(IntegrityError):
            test_msg = Message(user_id=12, text="This should raise an error")
            db.session.add(test_msg)
            db.session.commit()
        
        #test if a message is created
        self.assertIsInstance(self.msg2, Message)
    

    def testLikingMessage(self):
        """Testing the ability to like messages"""

        like = Likes(user_id=self.u1.id, message_id=self.msg1.id)

        db.session.add(like)
        db.session.commit()

        #check if like has an id. That means it successfully saved to the database
        self.assertTrue(like.id)

        #check if message is the same message that was liked
        self.assertEqual(like.message_id, self.msg1.id)
        self.assertEqual(like.user_id, self.u1.id)
    
