from flask import Response
import json

def ok(data = None):
    if data:
        package = {
            'status': 'ok',
            'data': data
        }
    else:
        package = {
            'status': 'ok'
        }

    return Response(response = json.dumps(package), status = 200, mimetype = 'application/json')

def created(data = None):
    if data:
        package = {
            'status': 'ok',
            'data': data
        }
    else:
        package = {
            'status': 'ok'
        }

    return Response(response = json.dumps(package), status = 201, mimetype = 'application/json')

def badRequest(data = None):
    
    if data:
        package = {
            'status': 'error',
            'data': data
        }
    else:
        package = {
            'status': 'bad_request'
        }
    return Response(response = json.dumps(package), status = 400, mimetype = 'application/json')

def unauthorized(data = None):
    
    if data:
        package = {
            'status': 'error',
            'data': data
        }
    else:
        package = {
            'status': 'unauthorized'
        }

    return Response(response = json.dumps(package), status = 401, mimetype = 'application/json')

def forbidden(data = None):

    if data:
        package = {
            'status': 'error',
            'data': data
        }
    else:
        package = {
            'status': 'forbidden'
        }

    return Response(response = json.dumps(package), status = 403, mimetype = 'application/json')

def notFound(data = None):
    if data:
        package = {
            'status': 'error',
            'data': data
        }
    else:
        package = {
            'status': 'not_found'
        }

    return Response(response = json.dumps(package), status = 404, mimetype = 'application/json')

def internalServerError(data = None):
    if data:
        package = {
            'status': 'error',
            'data': data
        }
    else:
        package = {
            'status': 'internal_server_error'
        }

    return Response(response = json.dumps(package), status = 500, mimetype = 'application/json')