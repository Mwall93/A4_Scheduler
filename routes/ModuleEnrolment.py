from flask import request, Blueprint, render_template, url_for, session

from core import JsonResponse
from core import Database
from core import Config
from core import Authorization
from core import Timetable

import time

from model.Student import Student as StudentModel
from model.StudentModule import StudentModule as StudentModuleModel
from model.Module import Module as ModuleModel

ModuleEnrolment = Blueprint('ModuleEnrolment', __name__)
@ModuleEnrolment.route('/student/<student_id>/modules', methods=['GET'])
def List(student_id):
    """Returns all modules for given student."""
    # Verify user access
    if not Authorization.canAccess(session.get('user'), ('scheduling_admin')):
        return render_template('error/no_access.html')


    student = StudentModel.findById(student_id)

    if not student:
        return render_template('error/resource_not_found.html')

    module_enrolments = StudentModuleModel.findBy('student', student_id)
    modules = []
    module_id = []

    for enrolment in module_enrolments:
        Module = ModuleModel.findById(enrolment.getModule())
        modules.append(Module)
        module_id.append(Module.getId())
     
    AllModules = ModuleModel.all()
    Available_Modules = []

    for module in AllModules:
        if module.getId() not in module_id:
            Available_Modules.append(module)
        
    # get student timetable
    timetable = Timetable.getStudentTimetable(student_id, Timetable.getStartOfMonth(), Timetable.getEndOfMonth())

    return render_template('enrolment_list.html', data ={
        "enroled_modules": modules,
        "available_modules": Available_Modules,
        "student": student,
        "timetable": timetable
    })

@ModuleEnrolment.route('/student/<student_id>/modules', methods=['POST'])
def Create(student_id):

    if not Authorization.canAccess(session.get('user'), ('scheduling_admin')):
        return JsonResponse.unauthorized({'message': 'no_access', 'nice_message': 'You do not have access to this page. Contact system administrator.'})

    module_id = request.form.get('module')

    if not module_id or not student_id:
        return JsonResponse.badRequest({'message': 'missing_parameters', 'nice_message': 'Missing student or module.'})


    newEnrolment = StudentModuleModel()

    dateNow = int(time.time())

    newEnrolment.setEnrolmentDate(dateNow)

    newEnrolment.setStudent(student_id)
    newEnrolment.setModule(module_id)
    newEnrolment.save()
    

    return JsonResponse.ok()

@ModuleEnrolment.route('/student/<student_id>/modules/<module_id>/enrolment', methods=['DELETE'])
def Delete(student_id, module_id):
    if not Authorization.canAccess(session.get('user'), ('scheduling_admin')):
        return JsonResponse.unauthorized({'message': 'no_access', 'nice_message': 'You do not have access to this function. Contact system administrator.'})
    
    if not student_id or not module_id:
        return JsonResponse.badRequest({'message': 'missing_parameters', 'nice_message': 'Missing parameter.'})

    enrolments = StudentModuleModel.findBy('student', student_id)

    for enrolment in enrolments:
        if enrolment.getModule() == int(module_id):
            enrolment.delete()
            return JsonResponse.ok()

    return JsonResponse.notFound({'message': 'not_found', 'nice_message': 'Enrolment does not exist.'})

