from re import match
from werkzeug.exceptions import NotFound, BadRequest
from flask import render_template, request, make_response, jsonify, abort

from flaskr.models import db, Question, Category


QUESTIONS_PER_PAGE = 10


def verify_valid_num(n):
    if isinstance(n, str):
        if match(r'^[0-9]+$', n) is None:
            abort(400)
        else:
            return True

    if isinstance(n, int):
        return True

    return abort(400)


def create_routes(app):
    @app.route('/categories')
    def retrieve_categories():
        try:
            categories = Category.query.order_by(Category.id).all()

            formatted_categories = {}
            for category in categories:
                category = category.format()
                formatted_categories.update(category)

            return jsonify({
                'success': True,
                'categories': formatted_categories
            })

        except:
            abort(500)

    @app.route('/questions')
    def retrieve_questions():
        try:
            page = request.args.get('page', 1, type=int)

            questions = Question.query.order_by(Question.id).\
                paginate(page=page, per_page=QUESTIONS_PER_PAGE)

            categories = Category.query.order_by(Category.id).all()

            formatted_categories = {}
            for category in categories:
                category = category.format()
                formatted_categories.update(category)

            return jsonify({
                'success': True,
                'questions': [question.format() for question in questions.items],
                'total_questions': questions.total,
                'categories': formatted_categories,
                'current_category': {'0': 'click'}
            })

        except NotFound:
            abort(404)
        except:
            abort(500)

    @app.route('/questions/<questions_id>', methods=['DELETE'])
    def delete_question(questions_id):
        try:
            # check if questions_id can be converted to integer
            if match(r'^[0-9]+$', questions_id) is None:
                abort(400)

            questions_id = int(questions_id)

            question = Question.query.get_or_404(questions_id)

            question.delete()

            return jsonify({
                'success': True,
                'deleted': questions_id
            })

        except BadRequest:
            abort(400)
        except NotFound:
            abort(404)
        except:
            abort(500)

    @app.route('/questions', methods=['POST'])
    def create_question():
        try:
            data = request.get_json() if request.is_json else None

            if data is None or len(data) == 0:
                abort(400)

            ''' 
                verify that data does contain (question and answer, category, and difficulty),
                as well as no additional key/value data that is not required,
                and finally verify that data has not empty strings.
                
                Note: I executed it this way so
                 it can dynamically verify needed data from user if i added extra column to Question Model.
                 all i should do when adding a new column to Question is to represent this coulumn as
                 name:type pair in required_question_args
            '''
            required_question_args = {'question': str, 'answer': str, 'difficulty': int, 'category': str}
            for k in data:
                if len(data) != len(required_question_args) \
                        or k not in required_question_args \
                        or type(data[k]) is not required_question_args[k] \
                        or isinstance(data[k], str) and len(data[k]) == 0:
                    abort(400)

            new_question = Question(**data)
            new_question.insert()

            return jsonify({
                'success': True,
                'created': new_question.id
            })

        except BadRequest:
            abort(400)
        except:
            abort(500)

    @app.route('/questionssearch', methods=['POST'])
    def search_questions():
        try:
            data = request.get_json() if request.is_json else None
            if data is None or len(data) == 0:
                abort(400)

            search_term = data.get('searchTerm', None)
            if search_term is None\
                    or not isinstance(search_term, str)\
                    or len(search_term) == 0:
                abort(400)

            page = request.args.get('page', 1, type=int)

            questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).\
                order_by(Question.id).\
                paginate(page=page, per_page=QUESTIONS_PER_PAGE)

            return jsonify({
                'success': True,
                'questions': [question.format() for question in questions.items],
                'total_questions': questions.total,
                'current_category': {'0': 'click'}
            })

        except BadRequest:
            abort(400)

        except NotFound:
            abort(404)
        except:
            abort(500)

    @app.route('/categories/<category_id>/questions')
    def retrieve_questions_by_category(category_id):
        try:
            # verify that category_id is a valid id
            if match(r'^[0-9]+$', category_id) is None:
                abort(400)

            page = request.args.get('page', 1, type=int)

            questions = Question.query.filter(Question.category == category_id).order_by(Question.id).paginate(page=page, per_page=QUESTIONS_PER_PAGE)

            current_questions = questions.items

            if len(current_questions) == 0:
                abort(404)

            current_category = Category.query.get_or_404(category_id)

            return jsonify({
                'success': True,
                'questions': [question.format() for question in current_questions],
                'total_questions': questions.total,
                'current_category': current_category.format()
            })

        except BadRequest:
            abort(400)
        except NotFound:
            abort(404)
        except:
            abort(500)

    @app.route('/quizzes', methods=['POST'])
    def retrieve_next_question():
        try:
            data = request.get_json() if request.is_json else None

            if data is None or len(data) == 0:
                abort(400)

            previous_questions = data.get('previous_questions', None)
            quiz_category = data.get('quiz_category', None)

            # verify that previous_questions and quiz_category exists in valid format
            if not isinstance(quiz_category, dict) \
                    or quiz_category.get('id', None) is None\
                    or (not isinstance(quiz_category['id'], int) and not isinstance(quiz_category['id'], str)) \
                    or not isinstance(previous_questions, list):
                abort(400)

            if isinstance(quiz_category['id'], str) \
                    and match(r'^[0-9]+$', quiz_category['id']) is None:
                abort(400)
            else:
                quiz_category['id'] = str(quiz_category['id'])

            for i in previous_questions:
                verify_valid_num(i)

            next_question = None

            if int(quiz_category['id']) == 0:
                next_question = Question.query.filter(db.not_(Question.id.in_(previous_questions))).\
                    limit(1).one_or_none()
            else:
                next_question = Question.query.filter(db.not_(Question.id.in_(previous_questions)), Question.category == quiz_category['id']).\
                    limit(1).one_or_none()

            if next_question is not None:
                next_question = next_question.format()
                previous_questions.append(next_question['id'])

            return jsonify({
                    'success': True,
                    'question': next_question,
                    'previous_questions': previous_questions
                })

        except BadRequest:
            abort(400)
        except:
            abort(500)
