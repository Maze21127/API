from flask import Flask, jsonify, render_template
from flask_restful import Api, reqparse
from MySQL import MySQL
import hashlib

from settings import *


sql = MySQL(host=HOST, port=PORT, user=LOGIN, password=PASSWORD, database=DATABASE)

app = Flask('MyFirstAPI')
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/best', methods=['GET', 'POST'])
@app.route('/best/', methods=['GET', 'POST'], strict_slashes=False)
def get_best():
    parser = reqparse.RequestParser()
    parser.add_argument('count', type=int)
    params = parser.parse_args()
    if params['count'] is None:
        return jsonify(sql.get_best()[0])
    return jsonify(sql.get_best(params['count']))


@app.route('/last', methods=['GET', 'POST'])
@app.route('/last/', methods=['GET', 'POST'], strict_slashes=False)
def get_last():
    parser = reqparse.RequestParser()
    parser.add_argument('count', type=int)
    params = parser.parse_args()
    if params['count'] is None:
        return jsonify(sql.get_last()[0])
    return jsonify(sql.get_last(params['count']))


@app.route('/random', methods=['GET', 'POST'])
@app.route('/random/', methods=['GET', 'POST'], strict_slashes=False)
def get_random():
    parser = reqparse.RequestParser()
    parser.add_argument('count', type=int)
    params = parser.parse_args()
    if params['count'] is None:
        return jsonify(sql.get_random()[0])
    return jsonify(sql.get_random(params['count']))


@app.route('/place', methods=['GET', 'POST'])
@app.route('/place/', methods=['GET', 'POST'], strict_slashes=False)
def get_place_by_score():
    parser = reqparse.RequestParser()
    parser.add_argument('score')
    params = parser.parse_args()
    try:
        return jsonify(sql.get_place(int(params['score'])))
    except ValueError:
        return "Score is incorrect", 400
    except TypeError:
        return "Missing 1 required parameter 'score'", 400


@app.route('/find', methods=['GET', 'POST'])
@app.route('/find/', methods=['GET', 'POST'], strict_slashes=False)
def find_student():
    parser = reqparse.RequestParser()
    parser.add_argument('place')
    parser.add_argument('snils', type=str)
    params = parser.parse_args()
    if params['place'] is not None:
        try:
            return jsonify(sql.find_student_by_place(int(params['place'])))
        except ValueError:
            return "Place is incorrect", 400
    elif params['snils'] is not None:
        return jsonify(sql.find_student_by_snils(params['snils']))
    return "Missing one of required parameters 'place or snils\n'%20' instead space in snils'", 400


@app.route('/update', methods=['GET'])
@app.route('/update/', methods=['GET', 'POST'], strict_slashes=False)
def update_db():
    parser = reqparse.RequestParser()
    parser.add_argument('token')
    params = parser.parse_args()
    if params['token'] == UPDATE_TOKEN:
        return sql.is_new()
    else:
        return "Invalid token, access denied", 403


@app.route('/admin', methods=['GET', 'POST'])
@app.route('/admin/', methods=['GET', 'POST'], strict_slashes=False)
def admin_page():
    parser = reqparse.RequestParser()
    parser.add_argument('password')
    params = parser.parse_args()
    temp = params['password'] + SALT
    try:
        if hashlib.md5(temp.encode()).hexdigest() == ADMIN_PASSWORD:
            return jsonify({
                'update_token': UPDATE_TOKEN})
        else:
            return "Invalid password, access denied", 403
    except AttributeError:
        return "Invalid password, access denied", 403


api = Api(app)
app.run(debug=True)
