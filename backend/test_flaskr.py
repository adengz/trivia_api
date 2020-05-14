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
            # create test db entries
            category = Category(type='category')
            cls.db.session.add(category)
            question = Question(question='question?', answer='answer',
                                category=1, difficulty=1)
            cls.db.session.add(question)
            cls.db.session.commit()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            cls.db.drop_all()

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreater(len(data['questions']), 0)
        self.assertGreater(data['total_questions'], 0)
        self.assertGreater(len(data['categories']), 0)
        self.assertIsNone(data['current_category'])

    def test_404_get_paginated_questions_out_of_range(self):
        res = self.client().get('/questions?page=100')
        self.assertEqual(res.status_code, 404)
        self.assertFalse(json.loads(res.data)['success'])

    def test_search_questions(self):
        res = self.client().post('/questions/searches', json={'searchTerm': 'question'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreater(len(data['questions']), 0)
        self.assertGreater(data['total_questions'], 0)
        self.assertIsNone(data['current_category'])
        self.assertNotIn('categories', data)

    def test_422_search_questions_empty_term(self):
        res = self.client().post('/questions/searches', json={'searchTerm': ''})
        self.assertEqual(res.status_code, 422)
        self.assertFalse(json.loads(res.data)['success'])

    def test_200_search_questions_no_results(self):
        res = self.client().post('/questions/searches', json={'searchTerm': 'answer'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_questions'], 0)
        self.assertIsNone(data['current_category'])
        self.assertNotIn('categories', data)

    def test_get_questions_in_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreater(len(data['questions']), 0)
        self.assertGreater(data['total_questions'], 0)
        self.assertIsNotNone(data['current_category'])
        self.assertNotIn('categories', data)

    def test_404_get_questions_in_category_empty(self):
        res = self.client().get('/categories/100/questions')
        self.assertEqual(res.status_code, 404)
        self.assertFalse(json.loads(res.data)['success'])

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()