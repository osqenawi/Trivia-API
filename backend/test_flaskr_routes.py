import os
import unittest
from flaskr import create_app
from flaskr.models import db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""
    @classmethod
    def setUpClass(cls):
        """Define test variables and initialize app."""
        cls.app = create_app('config.TestingConfig')
        cls.client = cls.app.test_client()

        os.system('psql trivia_test < trivia_test.psql')

    def tearDown(self):
        db.session.remove()

    @classmethod
    def tearDownClass(cls):
        """Executed after all tests"""
        db.drop_all()

    def test_retrieve_categories(self):
        # ---------------------SUCCESS------------------ #
        res = self.client.get('/categories')
        self.assertEqual(res.status_code, 200)

        # ---------------------FAILURE------------------ #
        res = self.client.post('/categories', json={'type': 'linguistic'})
        self.assertEqual(res.status_code, 405)

    def test_retrieve_questions(self):
        # ---------------------SUCCESS------------------ #
        res = self.client.get('/questions', query_string='page=1')
        self.assertEqual(res.status_code, 200)

        res = self.client.get('/questions')
        self.assertEqual(res.status_code, 200)

        # ---------------------FAILURE------------------ #
        res = self.client.get('/questions', query_string='page=1000')
        self.assertEqual(res.status_code, 404)

    def test_delete_question(self):
        # ---------------------SUCCESS------------------ #
        res = self.client.delete('/questions/1')
        self.assertEqual(res.status_code, 200)

        # ---------------------FAILURE------------------ #
        res = self.client.delete('/questions/s')
        self.assertEqual(res.status_code, 400)

        res = self.client.delete('/questions/10000')
        self.assertEqual(res.status_code, 404)

    def test_create_question(self):
        # ---------------------SUCCESS------------------ #
        res = self.client.post('/questions', json={'question': 'Ask?', 'answer': 'answered', 'difficulty': 1, 'category': 'science'})
        self.assertEqual(res.status_code, 200)

        # ---------------------FAILURE------------------ #
        res = self.client.post('/questions', json={'ques': 'Ask?', 'answer': 'answered', 'difficulty': 1, 'category': 'science'})
        self.assertEqual(res.status_code, 400)

        res = self.client.post('/questions', json={'question': 'Ask?', 'answer': 'answered', 'difficulty': None, 'category': 'science'})
        self.assertEqual(res.status_code, 400)

        res = self.client.post('/questions', json={'question': '', 'answer': 'answered', 'difficulty': '1', 'category': 'science'})
        self.assertEqual(res.status_code, 400)

        res = self.client.post('/questions', json={'question': 'Ask?', 'answer': 'answered', 'difficulty': '1', 'category': 'science', 'num': 1})
        self.assertEqual(res.status_code, 400)

        res = self.client.post('/questions', json={'question': 'Ask?', 'answer': 'answered', 'difficulty': '1'})
        self.assertEqual(res.status_code, 400)

        res = self.client.post('/questions', json={})
        self.assertEqual(res.status_code, 400)

        res = self.client.post('/questions')
        self.assertEqual(res.status_code, 400)

    def test_search_questions(self):
        # ---------------------SUCCESS------------------ #
        res = self.client.post('/questionssearch', json={'searchTerm': 'title'})
        self.assertEqual(res.status_code, 200)

        # ---------------------FAILURE------------------ #
        res = self.client.post('/questionssearch', json={'searchTerm': 1})
        self.assertEqual(res.status_code, 400)

        res = self.client.post('/questionssearch', json={'searchTerm': ''})
        self.assertEqual(res.status_code, 400)

        res = self.client.post('/questionssearch', json={})
        self.assertEqual(res.status_code, 400)

        res = self.client.post('/questionssearch')
        self.assertEqual(res.status_code, 400)

    def test_retrieve_questions_by_category(self):
        # ---------------------SUCCESS------------------ #
        res = self.client.get('/categories/1/questions')
        self.assertEqual(res.status_code, 200)

        # ---------------------FAILURE------------------ #
        res = self.client.get('/categories/1000/questions')
        self.assertEqual(res.status_code, 404)

        res = self.client.get('/categories/0/questions')
        self.assertEqual(res.status_code, 404)

        res = self.client.get('/categories/a/questions')
        self.assertEqual(res.status_code, 400)

    def test_retrieve_next_question(self):
        # ---------------------SUCCESS------------------ #
        res = self.client.post('/quizzes', json={'previous_questions': [1], 'quiz_category': {'type': 'Science', 'id': '1'}})
        self.assertEqual(res.status_code, 200)

        res = self.client.post('/quizzes', json={'previous_questions': [1, '16'], 'quiz_category': {'type': 'Science', 'id': '1'}})
        self.assertEqual(res.status_code, 200)

        res = self.client.post('/quizzes', json={'previous_questions': [], 'quiz_category': {'type': 'Science', 'id': '1'}})
        self.assertEqual(res.status_code, 200)

        # ---------------------FAILURE------------------ #
        res = self.client.post('/quizzes', json={'previous_questions': [1, '16'], 'quiz_category': {'type': 'Science'}})
        self.assertEqual(res.status_code, 400)

        res = self.client.post('/quizzes', json={'previous_questions': [], 'quiz_category': {'type': 'Science', 'id': 'aa'}})
        self.assertEqual(res.status_code, 400)

        res = self.client.post('/quizzes', json={'previous_questions': []})
        self.assertEqual(res.status_code, 400)

        res = self.client.post('/quizzes', json={'quiz_category': {'type': 'Science', 'id': '1'}})
        self.assertEqual(res.status_code, 400)

        res = self.client.post('/quizzes', json={'previous_questions': [''], 'quiz_category': {'type': 'Science', 'id': '1'}})
        self.assertEqual(res.status_code, 400)

        res = self.client.post('/quizzes', json={'previous_questions': [{}], 'quiz_category': {'type': 'Science', 'id': '1'}})
        self.assertEqual(res.status_code, 400)

        res = self.client.post('/quizzes', json={'': ''})
        self.assertEqual(res.status_code, 400)

        res = self.client.post('/quizzes')
        self.assertEqual(res.status_code, 400)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
