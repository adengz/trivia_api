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
            db.session.rollback()
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
            db.session.rollback()
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

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        data = request.get_json()
        try:
            asked_questions = set(data['previous_questions'])
            c_id = data['quiz_category']['id']
        except KeyError:
            abort(400)

        query = Question.query.with_entities(Question.id)
        all_questions = query.all() if c_id == 0 else query.filter_by(category=c_id).all()
        if not all_questions:
            abort(404)

        response = {'success': True}
        if len(asked_questions) == len(all_questions):
            return jsonify(response)

        new_questions = [i[0] for i in all_questions if i[0] not in asked_questions]
        q_id = random.choice(new_questions)
        new_question = Question.query.get(q_id)
        response['question'] = new_question.format()
        return jsonify(response)

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
