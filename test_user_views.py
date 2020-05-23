"""Test user views"""

import os
from unittest import TestCase

from models import db, connect_db, User, Follows

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app, CURR_USER_KEY

app.config["SQLALCHEMY_ECHO"] = False

db.create_all()

app.config["WTF_CSRF_ENABLED"] = False

class UserViewTestCase(TestCase):
    """Test user views"""

    def setUp(self):
        """create sample users and test client"""

        User.query.delete()
        
        self.client = app.test_client()

        self.user1 = User.signup("testuser", "test@123.com", "asdfgh", None)
        self.user2 = User.signup("testuser2", "test2@123.com", "asdfgh", None)
        self.user3 = User.signup("testuser3", "test3@123.com", "asdfgh", None)

        db.session.commit()

        self.user1.following.append(self.user2)
        self.user2.following.append(self.user3)

        db.session.commit()

    def tearDown(self):
        """rollback transactions"""
        db.session.rollback()
    
    def test_show_following(self):
        """can authenticated users see a who a user is following"""
        u2_id = self.user2.id
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id
            
            resp = c.get(f"/users/{u2_id}/following", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<p>@testuser3</p>", html)
        
    def test_not_logged_in_following(self):
        """Test if a non logged in users can see who a user is following"""

        u2_id = self.user2.id
        with self.client as c:
            resp = c.get(f"/users/{u2_id}/following", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<div class="alert alert-danger">Access unauthorized.</div>', html)
    
    def test_show_followers(self):
        """can authenticated users see a who a user followers"""
        u3_id = self.user3.id
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id
            
            resp = c.get(f"/users/{u3_id}/followers", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<p>@testuser2</p>", html)
        
    def test_not_logged_in_followers(self):
        """Test if a non logged in users can see who a user is following"""

        u3_id = self.user3.id
        with self.client as c:
            resp = c.get(f"/users/{u3_id}/followers", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<div class="alert alert-danger">Access unauthorized.</div>', html)