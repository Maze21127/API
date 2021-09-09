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
UPDATE_TOKEN = environ['UPDATE_TOKEN']
