from flask import request, Blueprint, render_template, url_for, session

from core import JsonResponse
from core import Database
from core import Config
from core import Authorization
from core import Scheduler

from model.Student import Student as StudentModel
from model.ModuleSession import ModuleSession as ModuleSessionModel
from model.ModuleSessionType import ModuleSessionType as ModuleSessionTypeModel
from model.Module import Module as ModuleModel
from model.Teacher import Teacher as TeacherModel
from model.StudentModule import StudentModule as StudentModuleModel 

Module = Blueprint('Module', __name__)

@Module.route('/module', methods=['GET'])
def List():
    """ Lists all modules. """
    # Verify user access
    if not Authorization.canAccess(session.get('user'), ('scheduling_admin')):
        return render_template('error/no_access.html')

    # Get list of all teachers
    teachers = TeacherModel.all()

    # Get list of modules
    modules = ModuleModel.all()
    
    return render_template('module_list.html', data = {
        'modules': modules,
        'teachers': teachers
    })


@Module.route('/module', methods=['POST'])
def Create():
    """ Creates a new module. """
    # Verify user access
    if not Authorization.canAccess(session.get('user'), ('scheduling_admin')):
        return JsonResponse.unauthorized({'message': 'no_access', 'nice_message': 'You do not have access to this page. Contact system administrator.'})

    # Parse and validate request body
    name   = request.form.get('module_name')
    leader = request.form.get('leader')

    if not name or not leader:
        return JsonResponse.badRequest({'message': 'missing_parameters', 'nice_message': 'Please make sure you enter a name and leader.'})

    # Make sure leader is a valid staff member
    if not TeacherModel.findById(leader):
        return JsonResponse.badRequest({'message': 'not_found', 'nice_message': 'Teacher not found'})
            # Save new data to database
    module = ModuleModel()

    module.setName(name) \
          .setLeader(leader) \
          .save()
    
    return JsonResponse.ok()

@Module.route('/module/<id>/enrol', methods=['POST'])
def Enrol(id):
    """Enrols Student to a Module"""

    if not Authorization.canAccess(session.get('user'), ('scheduling_admin')):
        return JsonResponse.unauthorized({'message': 'no_access', 'nice_message': 'You do not have access to this page. Contact system administrator..'})

    studentId = request.form.get(student)

    if not studentId:
        return JsonResponse.notFound({'message': 'not_found', 'nice_message': 'Student not found'})
    
    enrol = StudentModuleModel()
    enrol.setModule(id)
    enrol.setStudent(studentId)

    enrol.save()




@Module.route('/module/<id>', methods=['GET'])
def View(id):
    """ Gets information for given module. """
    # Verify user access
    if not Authorization.canAccess(session.get('user'), ('scheduling_admin')):
        return render_template('error/no_access.html')

    # Get module object
    module = ModuleModel.findById(id)

    if not module:
        return render_template('error/resource_not_found.html')

    # Get leader (teacher) object
    leader = TeacherModel.findById(module.getLeader())

    if not module:
        return render_template('error/server_error.html')

    # Get teachers object
    teachers = TeacherModel.all()

    # Get enrolled students
    students = []
    enrolments = StudentModuleModel.findBy('module', id)

    for enrolment in enrolments:
        students.append(StudentModel.findById(enrolment.getStudent()))
    
    # Get module sessions (+ teachers)
    sessions = ModuleSessionModel.findBy('module', id)
    sessions_list = []

    for session2 in sessions:
        sessions_list.append({
            'session': session2,
            'staff': TeacherModel.findById(session2.getStaff()),
            'type': ModuleSessionTypeModel.findById(session2.getType())
        })

    # Get session types
    sessionTypes = ModuleSessionTypeModel.all()

    return render_template('module_view.html', data = {
        'module': module,
        'leader': leader,
        'teachers': teachers,
        'students': students,
        'sessionTypes': sessionTypes,
        'sessions': sessions_list
    })


@Module.route('/module/<id>', methods=['POST'])
def Update(id):
    """ Updates a given module. """
    # Verify user access
    if not Authorization.canAccess(session.get('user'), ('scheduling_admin')):
        return JsonResponse.unauthorized({'message': 'no_access', 'nice_message': 'You do not have access to this page. Contact system administrator.'})

    # Get module object
    module = ModuleModel.findById(id)

    if not module:
        return JsonResponse.notFound({'message': 'not_found', 'nice_message': 'Module not found.'})
    
    # Save new values to database
    name   = request.form.get('module_name')
    leader = request.form.get('leader')

    if not name and not leader:
        return JsonResponse.badRequest({'message': 'missing_parameters', 'nice_message': 'Please enter a new name or module leader.'})
    
    if name:
        module.setName(name)
    
    if leader:
        if not TeacherModel.findById(leader):
            return JsonResponse.badRequest({'message': 'not_found', 'nice_message': 'Teacher not found.'})
        
        module.setLeader(leader)
    
    module.save()

    return JsonResponse.ok()


@Module.route('/module/<id>', methods=['DELETE'])
def Delete(id):
    """ Deletes a given module. """
    # Verify user access
    if not Authorization.canAccess(session.get('user'), ('scheduling_admin')):
        return JsonResponse.unauthorized({'message': 'no_access', 'nice_message': 'You do not have access to this page. Contact system administrator.'})
    
    # Get module object
    module = ModuleModel.findById(id)
    
    if not module:
        return JsonResponse.notFound({'message': 'not_found', 'nice_message': 'Module not found.'})
    
    # Delete from database
    module.delete()
    
    return JsonResponse.ok()

@Module.route('/module/<module_id>/session/<session_id>/schedule', methods=['GET'])
def ScheduleSessionTest(module_id, session_id):
    Scheduler.bookRooms(1, 1, 1, 2, 1, 2, 2)

    return JsonResponse.ok({
        'bookRooms': 'ok'
    })

    #def bookRooms(term_id, session_id, building_id, day_of_week, frequency, duration, sessionType)