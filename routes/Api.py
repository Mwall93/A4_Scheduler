from flask import request, Blueprint
from core import JsonResponse
from core import Config
from core import ApiSession
from core import Timetable
from core import Security

from model.Student import Student as StudentModel
from model.Teacher import Teacher as TeacherModel

Api = Blueprint('Api', __name__)

@Api.route('/api', methods=['GET'])
def route():
    """ Example route, show information about system and current session. """
    userId = -1

    if 'X-App-Token' in request.headers:
        userId = ApiSession.getUserId(request.headers['X-App-Token'])

    return JsonResponse.ok({
        'application': 'A4Scheduler',
        'environment': Config.getValue('ENVIRONMENT'),
        'userId': userId
    })

@Api.route('/api/session', methods=['POST'])
def SessionLogin():
    if 'X-App-Token' in request.headers and ApiSession.isValid(request):
        return JsonResponse.ok({'token': request.headers['X-App-Token']})
    
    userEmail = request.form.get('email')
    userPassword = request.form.get('password')
    userType = request.form.get('user_type')

    # Step 1: Verify presence of values and validate them
    if not userEmail or not userPassword or not userType:
        return JsonResponse.badRequest({'message': 'post_property_missing', 'nice_message': 'Missing POST property.'})
    
    if userType not in ('student', 'teacher'):
        return JsonResponse.badRequest({'message': 'invalid_user_type', 'nice_message': 'Given user type is invalid! Allowable types are: student/teacher.'})

    # Step 2: Verify password
    if userType == 'student':
        user = StudentModel.findBy('email', userEmail)
    elif userType == 'teacher':
        user = TeacherModel.findBy('email', userEmail)
    else:
        return JsonResponse.internalServerError({'message': 'unexpected_user_type', 'nice_message': 'Unexpected user type. Contact system administrator.'})

    if len(user) != 1:
        return JsonResponse.unauthorized({'message': 'invalid_credentials', 'nice_message': 'Supplied credentials (email/password) are invalid.'})

    user = user[0]

    salt = user.getSalt()

    hashedPassword = Security.hashPassword(userPassword, salt)

    if hashedPassword != user.getPassword():
        return JsonResponse.unauthorized({'message': 'invalid_credentials', 'nice_message': 'Supplied credentials (email/password) are invalid.'})
    
    userId = user.getId()

    # Step 3: Create session
    ipAddress = request.remote_addr

    if Config.getValue('DEPLOYMENT') == 'heroku':
        ipAddress = request.headers['X-Forwarded-For']

    token = ApiSession.create(userId, userType, ipAddress, request.headers['User-Agent'])

    if token:
        return JsonResponse.ok({'token': token})
    
    return JsonResponse.internalServerError({'message': 'session_generation_failed', 'nice_message': 'Session generation failed. Contact system administrator.'})

@Api.route('/api/session', methods=['DELETE'])
def SessionLogout():
    if 'X-App-Token' not in request.headers or not ApiSession.isValid(request):
        return JsonResponse.ok()
    
    ApiSession.terminate_req(request)
    return JsonResponse.ok()

@Api.route('/api/timetable', methods=['GET'])
def GetTimetable():
    if 'X-App-Token' in request.headers and ApiSession.isValid(request):
        userId, userType = ApiSession.getUserId_req(request)
    else:
        return JsonResponse.unauthorized({'message': 'invalid_session', 'nice_message': 'Invalid session. Did you login?'})
    
    if userType == 'student':
        return JsonResponse.ok({
            'events': Timetable.getStudentTimetable(userId, 1050194809, 1950194809)
        })
    elif userType == 'teacher':
        return JsonResponse.ok({
            'events': Timetable.getTeacherTimetable(userId, 1050194809, 1950194809)
        })
    
    return JsonResponse.internalServerError({'message': 'unexpected_user_type', 'nice_message': 'Unexpected user type. Contact system administrator.'})


# Routes below are for DEBUG purposes ONLY

@Api.route('/api/student/timetable/<student_id>', methods=['GET'])
def DebugStudentTimetable(student_id):
    return JsonResponse.ok({
        'events': Timetable.getStudentTimetable(student_id, 1050194809, 1950194809)
    })

@Api.route('/api/teacher/timetable/<teacher_id>', methods=['GET'])
def DebugTeacherTimetable(teacher_id):
    return JsonResponse.ok({
        'events': Timetable.getTeacherTimetable(teacher_id, 1050194809, 1950194809)
    })