from os import environ
from dotenv import load_dotenv

load_dotenv('.env')
HOST = environ['HOST']
PORT = int(environ['PORT'])
LOGIN = environ['LOGIN']
PASSWORD = environ['PASSWORD']
DATABASE = environ['DATABASE']
SALT = environ['SALT']
ADMIN_PASSWORD = environ['ADMIN_PASSWORD']
ADMIN_TOKEN = environ['ADMIN_TOKEN']
EMAIL = environ['EMAIL']
EMAIL_PASSWORD = environ['EMAIL_PASSWORD']
SECRET_KEY = environ['SECRET_KEY']
