from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random

from models import db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(config_object='config.Config'):
    # create and configure the app
    app = Flask(__name__)
    if app.config['ENV'] == 'development':
        config_object = 'config.DevelopmentConfig'
    app.config.from_object(config_object)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.all()
        if not categories:
            abort(404)
        return jsonify({'success': True,
                        'categories': {c.id: c.type for c in categories}})

    @app.route('/questions', methods=['GET'])
    def get_paginated_questions():
        page = request.args.get('page', 1, type=int)
        questions = Question.query.order_by(Question.id).all()
        start = QUESTIONS_PER_PAGE * (page - 1)
        end = start + QUESTIONS_PER_PAGE
        paginated = questions[start:end]

        if not paginated:
            abort(404)
        categories = Category.query.all()
        return jsonify({'success': True,
                        'questions': [q.format() for q in paginated],
                        'total_questions': len(questions),
                        'categories': {c.id: c.type for c in categories},
                        'current_category': None})

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)
        if not question:
            abort(404)

        try:
            question.delete()
        except:
            abort(500)
        return jsonify({'success': True})

    @app.route('/questions', methods=['POST'])
    def add_question():
        data = request.get_json()
        try:
            question = Question(**data)
        except (TypeError, ValueError):
            abort(400)

        try:
            assert len(question.question) > 0
            assert len(question.answer) > 0
            question.difficulty = int(question.difficulty)
            assert 1 <= question.difficulty <= 5
            question.category = int(question.category)
        except (AssertionError, ValueError):
            abort(422)

        try:
            question.insert()
        except:
            abort(500)
        return jsonify({'success': True})

    @app.route('/questions/searches', methods=['POST'])
    def search_questions():
        data = request.get_json()
        if 'searchTerm' not in data:
            abort(400)
        search_term = data['searchTerm']
        if not search_term:
            abort(422)

        questions = Question.query.filter(Question.question.like('%{}%'.format(search_term))).order_by(Question.id).all()
        return jsonify({'success': True,
                        'questions': [q.format() for q in questions],
                        'total_questions': len(questions),
                        'current_category': None})

    @app.route('/categories/<int:category>/questions', methods=['GET'])
    def get_questions_in_category(category):
        questions = Question.query.filter_by(category=category).order_by(Question.id).all()
        if not questions:
            abort(404)

        return jsonify({'success': True,
                        'questions': [q.format() for q in questions],
                        'total_questions': len(questions),
                        'current_category': category})


    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 
  
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'success': False, 'error': 400, 'message': 'Bad request'}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'success': False, 'error': 404, 'message': 'Not found'}), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({'success': False, 'error': 422, 'message': 'Unprocessable enitty'}), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({'success': False, 'error': 500, 'message': 'Internal server error'}), 500

    return app

    