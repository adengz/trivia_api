import os
import unittest
import json

from flaskr import create_app
from models import db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('config.TestingConfig')
        cls.client = cls.app.test_client
        cls.db = db
        cls.db.init_app(cls.app)

        # binds the app to the current context
        with cls.app.app_context():
            # create all tables
            cls.db.create_all()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            cls.db.drop_all()

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()