from flask import request, Blueprint, render_template, url_for, session
from core import Database
from core import Config
from core import JsonResponse
from core import Security
from core import Authorization

from model.Teacher import Teacher as TeacherModel
from model.Module import Module as ModuleModel
from model.ModuleSession import ModuleSession as ModuleSessionModel


Teacher = Blueprint('Teacher', __name__)
@Teacher.route('/teacher', methods=['GET'])
def List():
    """ Return list of all teachers """
    if not Authorization.canAccess(session.get('user'), ('admin')):
        return render_template('error/no_access.html')
    
    teachers = TeacherModel().all()

    return render_template('teacher_list.html', data = {
        'teachers': teachers
    })


@Teacher.route('/teacher', methods=['POST'])
def Create():
    """ Creates a new teacher """
    if not Authorization.canAccess(session.get('user'), ('admin')):
        return JsonResponse.unauthorized({'message': 'no_access', 'nice_message': 'You do not have access to this function. Contact system administrator'})

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    mobile_phone = request.form.get('mobile_phone')

    password = request.form.get('password')
    salt = Security.generateSalt()
    hashedPassword = Security.hashPassword(password, salt)

    teachers = TeacherModel()

    if not teachers:
        return JsonResponse.notFound({'message': 'not_found', 'nice_message': 'Teacher not found.'})

    teachers.setFirstName(first_name)
    teachers.setLastName(last_name)
    teachers.setEmail(email)
    teachers.setMobile(mobile_phone)
    teachers.setPassword(hashedPassword)
    teachers.setSalt(salt)

    try:
        teachers.save()
    except:
        return JsonResponse.badRequest({'error': 'database_error'})

    return JsonResponse.ok()


@Teacher.route('/teacher/<id>', methods=['GET'])
def View(id):
    """ Returns teachers information """
    if not Authorization.canAccess(session.get('user'), ('admin')):
        return render_template('error/no_access.html')
    
    teachers = TeacherModel.findById(id)
    if not teachers:
        return render_template('error/resource_not_found.html')

    return render_template('teacher_view.html', data = {
        'teacher': teachers
    })
    

@Teacher.route('/teacher/<id>', methods=['POST'])
def Update(id):
    """ Updates teachers information """
    if not Authorization.canAccess(session.get('user'), ('admin')):
        return JsonResponse.unauthorized({'message': 'no_access', 'nice_message': 'You do not have access to this function. Contact system administrator.'})
    
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    mobile_phone = request.form.get('mobile_phone')
    password = request.form.get('password')

    if not first_name and not last_name and not email and not mobile_phone and not password:
        return JsonResponse.badRequest({'message': 'missing_parameters', 'nice_message': 'Please enter details for the teacher.'})
    
    teachers = TeacherModel.findById(id)

    if not teachers:
        return JsonResponse.notFound({'message': 'not_found', 'nice_message': 'Teacher not found.'})

    if first_name:
        teachers.setFirstName(first_name)
        
    if last_name:
        teachers.setLastName(last_name)

    if email:
        teachers.setEmail(email)

    if mobile_phone:
        teachers.setMobile(mobile_phone)

    if password:
        salt = teachers.getSalt()
        hashedPassword = Security.hashPassword(password, salt)
        teachers.setPassword(hashedPassword)


    try:
        teachers.save()
    except:
        return JsonResponse.badRequest({'error': 'database_error'})

    return JsonResponse.ok()


@Teacher.route('/teacher/<id>', methods=['DELETE'])
def Delete(id):
    """ Deletes teacher """
    if not Authorization.canAccess(session.get('user'), ('admin')):
        return JsonResponse.unauthorized({'message': 'no_access', 'nice_message': 'You do not have access to this function. Contact system administrator'})
    
    teachers = TeacherModel.findById(id)

    if not teachers:
        return JsonResponse.notFound({'message': 'not_found', 'nice_message': 'Teacher not found.'})

    modules = ModuleModel.findBy('leader', id)

    if len(modules) !=0:
        return JsonResponse.badRequest({'message': 'bad_request', 'nice_message': 'Modules exist with this teacher as module leader.'})

    sessions = ModuleSessionModel.findBy('staff', id)
    
    if len(sessions)!=0:
        return JsonResponse.badRequest({'message': 'bad_request', 'nice_message': 'Sessions exist for this teacher.'})

    teachers.delete()

    return JsonResponse.ok()
