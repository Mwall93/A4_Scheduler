from raven import Client
from flask import Flask, request, session, redirect, url_for
from dotenv import load_dotenv
from core import Config
from core import Authorization
from core import Database
import os

# Setup the .env file
env_file = os.path.join(os.path.dirname(__file__), '.env')

if os.path.isfile(env_file) == True: #TODO: ONLY try to load the .env file if the environment is dev and NOT production
    load_dotenv(env_file)

# Setup the raven client for Sentry
client = Client(
    dsn = Config.getValue('SENTRY_DSN'),
    environment = Config.getValue('ENVIRONMENT')
)

db_file = os.path.join(os.path.dirname(__file__), 'system.db')

# Setup database if not exists
if Config.getValue('SQLITE') == 'yes':
    if os.path.isfile(db_file) == False:
        Database.createSQLite()
        

app = Flask(__name__)
app.debug = True

if Config.getValue('ENVIRONMENT') == 'local':
    @app.after_request
    def apply_caching(response):
        response.headers["Access-Control-Allow-Origin"] = '*'
        response.headers["Access-Control-Allow-Headers"] = 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,App-Token'
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, PUT, PATCH, DELETE"
        return response

# Dynamically load of all of the routes
for file in os.listdir('routes'):
    if file.endswith('.py') and file != '__init__.py':
        _ = file.replace('.py', '')
        module = __import__('routes.' + _)
        module = getattr(getattr(module, _), _)
        app.register_blueprint(module)


app.secret_key = b'\xfe%\xa7\x1a.\x14\xe2>\x00\xa7\xe6~-\x98i`'

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.before_request
def hook():
    if not request.endpoint == 'static':
        Database.connect()
    #return

    if request.endpoint == 'static':
        return

    if request.endpoint is None:
        return

    if request.endpoint.startswith('Api.') or request.endpoint.startswith('Auth.'):
        return

    if not Authorization.isLoggedIn( session.get('user') ):
        return redirect( url_for('Auth.Login') )
    
@app.after_request
def afterHook(response):
    if not request.endpoint == 'static':
        Database.disconnect()

    return response


@app.route('/')
def main():
    return redirect( url_for('Campus.List') )

# disable Dont panic debugger when in production, see: https://stackoverflow.com/a/21346137
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Config.getRawValue('PORT'))