import hashlib, uuid, time
from core import Database
from core import Config

def isValidToken(token, ip_addr, user_agent):
    """ Checks if the specified authentication token is valid """
    session = Database.getRows('SELECT `user_id`, `signature`, `expires` FROM `ApiSession` WHERE `token` = %s LIMIT 1', (token,))

    # Check if session exists
    if len(session) != 1:
        return False

    # Check if session expired
    if session[0]['expires'] < time.time():
        Database.execute('DELETE FROM `ApiSession` WHERE token = %s', (token,))
        return False

    # Check if signature matches
    signature = ip_addr + user_agent
    signature = hashlib.sha256(signature.encode('utf-8')).hexdigest()

    if signature != session[0]['signature']:
        Database.execute('DELETE FROM `ApiSession` WHERE token = %s', (token,))
    # Everything is okay, Renew the token
    Database.execute('UPDATE `ApiSession` SET expires = %s WHERE token = %s', (time.time() + 30*60, token))

    return True

def isValid(request):
    """ Checks if the session is valid (wrapper for isValidToken) """
    if 'X-App-Token' not in request.headers:
        return False

    ip_address = request.remote_addr

    if Config.getValue('DEPLOYMENT') == 'heroku':
        ip_address = request.headers['X-Forwarded-For']
    
    return isValidToken(request.headers['X-App-Token'], ip_address, request.headers['User-Agent'])

def getUserId(token):
    """ Gets the user ID that is assigned to the token """
    session = Database.getRows('SELECT `user_id`, `user_type` FROM `ApiSession` WHERE token = %s', (token,))

    # Do a sanity check
    if len(session) != 1:
        return None

    return int(session[0]['user_id']), session[0]['user_type']

def getUserId_req(request):
    """ Gets the user ID that is assigned to the token using the request object """
    if 'X-App-Token' not in request.headers:
        return None

    return getUserId(request.headers['X-App-Token'])

def create(user_id, user_type, ip_addr, user_agent):
    """ Creates a session in the database """
    signature = ip_addr + user_agent
    signature = hashlib.sha256(signature.encode('utf-8')).hexdigest()
    token     = str(uuid.uuid4()).replace('-', '')
    expires   = time.time() + 30*60

    Database.execute('INSERT INTO `ApiSession` (`user_id`, `user_type`, `signature`, `expires`, `token`) VALUES (%s, %s, %s, %s, %s)', (int(user_id), user_type, signature, expires, token))

    return token

def terminate(token):
    """ Terminates a given session """
    Database.execute('DELETE FROM `ApiSession` WHERE token = %s', (token,))

def terminate_req(request):
    if 'X-App-Token' not in request.headers:
        return False

    terminate(request.headers['X-App-Token'])
    return True

def terminateAll(user_id):
    """ Terminates all sessions for a user """
    Database.execute('DELETE FROM `ApiSession` WHERE user_id = %s', (user,))