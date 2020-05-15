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

    def setUp(self):
        with self.app.app_context():
            self.db.create_all()
            category = Category(type='category')
            self.db.session.add(category)
            question = Question(question='question?', answer='answer',
                                category=1, difficulty=1)
            self.db.session.add(question)
            self.db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            self.db.drop_all()

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

    def test_delete_question(self):
        res = self.client().delete('/questions/1')
        self.assertEqual(res.status_code, 200)
        self.assertTrue(json.loads(res.data)['success'])
        with self.app.app_context():
            self.assertIsNone(Question.query.get(1))

    def test_404_delete_question_not_present(self):
        res = self.client().delete('/questions/100')
        self.assertEqual(res.status_code, 404)
        self.assertFalse(json.loads(res.data)['success'])

    def test_add_question(self):
        res = self.client().post('/questions',
                                 json={'question': 'another question?',
                                       'answer': 'another answer',
                                       'difficulty': 2, 'category': 1})
        self.assertEqual(res.status_code, 200)
        self.assertTrue(json.loads(res.data)['success'])
        with self.app.app_context():
            q = Question.query.get(2)
            self.assertEqual(q.question, 'another question?')
            self.assertEqual(q.answer, 'another answer')
            self.assertEqual(q.difficulty, 2)
            self.assertEqual(q.category, 1)

    def test_400_add_question_wrong_args(self):
        res1 = self.client().post('/questions',
                                  json={'question': 'another question?',
                                        'answer': 'another answer',
                                        'category': 1})
        self.assertEqual(res1.status_code, 400)
        self.assertFalse(json.loads(res1.data)['success'])

        res2 = self.client().post('/questions',
                                  json={'question': 'another question?',
                                        'answer': 'another answer',
                                        'difficulty': 2, 'category': 1,
                                        'wrong_arg': None})
        self.assertEqual(res2.status_code, 400)
        self.assertFalse(json.loads(res2.data)['success'])

    def test_422_add_question_invalid_args(self):
        res1 = self.client().post('/questions',
                                  json={'question': '', 'answer': '',
                                        'difficulty': 2, 'category': 1})
        self.assertEqual(res1.status_code, 422)
        self.assertFalse(json.loads(res1.data)['success'])

        res2 = self.client().post('/questions',
                                  json={'question': 'q', 'answer': 'a',
                                        'difficulty': 10, 'category': 'none'})
        self.assertEqual(res2.status_code, 422)
        self.assertFalse(json.loads(res2.data)['success'])

    def test_search_questions(self):
        res = self.client().post('/questions/searches',
                                 json={'searchTerm': 'question'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreater(len(data['questions']), 0)
        self.assertGreater(data['total_questions'], 0)
        self.assertIsNone(data['current_category'])
        self.assertNotIn('categories', data)

    def test_400_search_questions_wrong_key(self):
        res = self.client().post('/questions/searches',
                                 json={'search_term': ''})
        self.assertEqual(res.status_code, 400)
        self.assertFalse(json.loads(res.data)['success'])

    def test_422_search_questions_empty_term(self):
        res = self.client().post('/questions/searches',
                                 json={'searchTerm': ''})
        self.assertEqual(res.status_code, 422)
        self.assertFalse(json.loads(res.data)['success'])

    def test_200_search_questions_no_results(self):
        res = self.client().post('/questions/searches',
                                 json={'searchTerm': 'answer'})
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

    def test_play_quiz_single_category(self):
        res1 = self.client().post('/quizzes',
                                  json={'previous_questions': [],
                                        'quiz_category': {'id': 1}})
        data1 = json.loads(res1.data)
        self.assertEqual(res1.status_code, 200)
        self.assertTrue(data1['success'])
        self.assertEqual(data1['question']['id'], 1)
        self.assertEqual(data1['question']['category'], 1)

        res2 = self.client().post('/quizzes',
                                  json={'previous_questions': [1],
                                        'quiz_category': {'id': 1}})
        data2 = json.loads(res2.data)
        self.assertEqual(res2.status_code, 200)
        self.assertTrue(data2['success'])
        self.assertNotIn('question', data2)

    def test_play_quiz_all_categories(self):
        with self.app.app_context():
            questions = [Question(f'q{c_id}', f'a{c_id}', c_id, 1)
                         for c_id in [2, 3, 4]]
            self.db.session.add_all(questions)
            self.db.session.commit()

        res = self.client().post('/quizzes',
                                 json={'previous_questions': [],
                                       'quiz_category': {'id': 0}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn(data['question']['category'], [1, 2, 3, 4])

    def test_400_play_quiz_invalid_args(self):
        res1 = self.client().post('/quizzes',
                                  json={'previous_questions': [],
                                        'category': {'id': 1}})
        self.assertEqual(res1.status_code, 400)
        self.assertFalse(json.loads(res1.data)['success'])

        res2 = self.client().post('/quizzes',
                                  json={'previous_questions': [],
                                        'quiz_category': {'category_id': 1}})
        self.assertEqual(res2.status_code, 400)
        self.assertFalse(json.loads(res2.data)['success'])

    def test_404_play_quiz_empty_category(self):
        res = self.client().post('/quizzes',
                                 json={'previous_questions': [],
                                       'quiz_category': {'id': 2}})
        self.assertEqual(res.status_code, 404)
        self.assertFalse(json.loads(res.data)['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
