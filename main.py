from flask import Flask, jsonify, render_template, request, redirect
from flask_restful import Api, reqparse
from flask_mail import Mail, Message
from MySQL import MySQL
from create_auth import *
from settings import *
from waitress import serve


sql = MySQL(host=HOST, port=PORT, user=LOGIN, password=PASSWORD, database=DATABASE)

app = Flask('MyFirstAPI')
app.config.from_pyfile('config.py')

mail = Mail(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/main')
def main_page():
    return render_template('main_page.html')


@app.route('/incorrect-email')
def incorrect_email_page():
    return render_template('incorrect-email.html')


@app.route('/user-exists')
def user_exists_page():
    return render_template('user-exist.html')


@app.route('/best', methods=['GET', 'POST'])
@app.route('/best/', methods=['GET', 'POST'], strict_slashes=False)
def get_best():
    parser = reqparse.RequestParser()
    parser.add_argument('count', type=int)
    parser.add_argument('token')
    params = parser.parse_args()
    if params['token'] is None:
        return "Missing 1 required parameter 'token'", 400
    if get_hash(params['token']) not in sql.users:
        return "Invalid token, access denied", 403
    if params['count'] is None:
        return jsonify(sql.get_best()[0])
    return jsonify(sql.get_best(params['count']))


@app.route('/last', methods=['GET', 'POST'])
@app.route('/last/', methods=['GET', 'POST'], strict_slashes=False)
def get_last():
    parser = reqparse.RequestParser()
    parser.add_argument('count', type=int)
    parser.add_argument('token')
    params = parser.parse_args()
    if params['token'] is None:
        return "Missing 1 required parameter 'token'", 400
    if get_hash(params['token']) not in sql.users:
        return "Invalid token, access denied", 403
    if params['count'] is None:
        return jsonify(sql.get_last()[0])
    return jsonify(sql.get_last(params['count']))


@app.route('/random', methods=['GET', 'POST'])
@app.route('/random/', methods=['GET', 'POST'], strict_slashes=False)
def get_random():
    parser = reqparse.RequestParser()
    parser.add_argument('count', type=int)
    parser.add_argument('token')
    params = parser.parse_args()
    if params['token'] is None:
        return "Missing 1 required parameter 'token'", 400
    if get_hash(params['token']) in sql.users:
        if params['count'] is None:
            return jsonify(sql.get_random()[0])
        return jsonify(sql.get_random(params['count']))
    return "Invalid token, access denied", 403


@app.route('/place', methods=['GET', 'POST'])
@app.route('/place/', methods=['GET', 'POST'], strict_slashes=False)
def get_place_by_score():
    parser = reqparse.RequestParser()
    parser.add_argument('score')
    parser.add_argument('token')
    params = parser.parse_args()
    if params['token'] is None:
        return "Missing 1 required parameter 'token'", 400
    if get_hash(params['token']) not in sql.users:
        return "Invalid token, access denied", 403
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
    parser.add_argument('token')
    params = parser.parse_args()
    if params['token'] is None:
        return "Missing 1 required parameter 'token'", 400
    if get_hash(params['token']) not in sql.users:
        return "Invalid token, access denied", 403
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
    if params['token'] is None:
        return "Invalid token, access denied", 403
    if get_hash(params['token']) not in sql.admins:
        return "Invalid token, access denied", 403

    return sql.is_new()


@app.route('/delete', methods=['GET'])
@app.route('/delete/', methods=['GET', 'POST'], strict_slashes=False)
def delete_user():
    parser = reqparse.RequestParser()
    parser.add_argument('token')
    parser.add_argument('email')
    params = parser.parse_args()
    if params['token'] is None:
        return "Invalid token, access denied", 403
    if get_hash(params['token']) not in sql.admins:
        return "Invalid token, access denied", 403
    return sql.delete_user(params['email'])


@app.route('/users', methods=['GET'])
@app.route('/users/', methods=['GET', 'POST'], strict_slashes=False)
def show_users():
    parser = reqparse.RequestParser()
    parser.add_argument('token')
    params = parser.parse_args()
    if params['token'] is None:
        return "Invalid token, access denied", 403
    if get_hash(params['token']) not in sql.admins:
        return "Invalid token, access denied", 403
    return jsonify([user['email'] for user in sql.get_users_list()])


@app.route('/get-token', methods=['GET', 'POST'])
@app.route('/get-token/', methods=['GET', 'POST'], strict_slashes=False)
def get_token():
    if request.method == 'GET':
        return '<form action="/" method="POST"><input name="email"><input type="submit"></form>'

    email = request.form["email"]
    if email in sql.emails:
        return redirect('/user-exists')

    if '@' not in email:
        return redirect('/incorrect-email')

    msg = Message('VVSU API TOKEN', sender=EMAIL, recipients=[email])
    msg.body = f'Your token is {sql.create_user(email)}'
    mail.send(msg)

    sql.update_bd()
    return redirect('/main')


@app.route('/admin', methods=['GET', 'POST'])
@app.route('/admin/', methods=['GET', 'POST'], strict_slashes=False)
def admin_page():
    parser = reqparse.RequestParser()
    parser.add_argument('password')
    params = parser.parse_args()
    if params['password'] is None:
        return "Invalid password, access denied", 403
    try:
        if get_hash(params['password']) == ADMIN_PASSWORD:
            return jsonify({
                'admin_token': ADMIN_TOKEN})
        else:
            return "Invalid password, access denied", 403
    except AttributeError:
        return "Invalid password, access denied", 403


api = Api(app)
serve(app, host='0.0.0.0', port=5000)
