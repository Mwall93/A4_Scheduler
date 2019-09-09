from flask import request, Blueprint, render_template, url_for, session
from core import JsonResponse
from core import Database
from core import Config
from core import Security
from core import Authorization

from model.Student import Student as StudentModel

Student = Blueprint('Student', __name__)
@Student.route('/student', methods=['GET'])
def List():
    """Gets a list of all students (Template: student_list.html)"""
    #Authorise (change who can authorise)
    if not Authorization.canAccess(session.get('user'), ('admin')):
        return render_template('error/no_access.html')

    students = StudentModel.all()

    return render_template("student_list.html", data={
        "students": students
    })
      
@Student.route('/student', methods=['POST'])
def Create():
    """Creates a new student (JSON) (Post variables: first_name, last_name, email, mobile_phone)"""
    #Change who is authorised
    if not Authorization.canAccess(session.get('user'), ('admin')):
        return JsonResponse.unauthorized({'message': 'no_access', 'nice_message': 'You do not have access to this function. Contact system administrator.'})

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    mobile_phone = request.form.get('mobile_phone')
    password = request.form.get('password')
    salt = Security.generateSalt()
    hashedPassword = Security.hashPassword(password, salt)
    student = StudentModel()

    if not first_name or not last_name or not email or not mobile_phone or not password:
        return JsonResponse.badRequest({'message': 'missing_parameters', 'nice_message': 'Please fill all fields for the new student.'})
    
    student.setFirstName(first_name)
    student.setLastName(last_name)
    student.setEmail(email)
    student.setMobile(mobile_phone)
    student.setPassword(hashedPassword)
    student.setSalt(salt)

    try:
        student.save()
    except:
        return JsonResponse.badRequest({'error': 'database_error'})

    return JsonResponse.ok()

@Student.route('/student/<id>', methods=['GET'])
def View(id):
    """Returns student information [+ student module enrolments]. (Template: student_view.html)"""

    if not Authorization.canAccess(session.get('user'), ('admin')):
        return render_template('error/no_access.html')

    student = StudentModel.findById(id)
    #Get Modules ?

    return render_template("student_view.html", data={
        "student": student
        #Modules? 
    })


@Student.route('/student/<id>', methods=['POST'])
def Update(id):
    """Updates student information """
    """(JSON) (Post variables: first_name, last_name, email, mobile_phone, password)"""
    #Auth
    if not Authorization.canAccess(session.get('user'), ('admin')):
        return JsonResponse.unauthorized()
     
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    mobile_phone = request.form.get('mobile_phone')
    password = request.form.get('password')

    if not first_name and not last_name and not email and not mobile_phone and not password:
        #Bad request
        return JsonResponse.badRequest({'message': 'missing_parameters', 'nice_message': 'Please fill out new information for the student.'})

    student = StudentModel.findById(id)
    #Not sure on method names
    if first_name:
        student.setFirstName(first_name)
    if last_name:
        student.setLastName(last_name)
    if email:
        student.setEmail(email)
    if mobile_phone:
        student.setMobile(mobile_phone)
    #Password hashed here
    if password:
        salt = student.getSalt()
        hashedPassword = Security.hashPassword(password, salt)
        student.setPassword(hashedPassword)

    try:
        student.save()
    except:
        return JsonResponse.badRequest({'error': 'database_error'})
    
    return JsonResponse.ok()

@Student.route('/student/<id>', methods=['DELETE'])
def Delete(id):
    """Deletes a Student"""
    #Authorise (Change who is authorised)
    if not Authorization.canAccess(session.get('user'), ('admin')):
        return JsonResponse.unauthorized({'message': 'not_access', 'nice_message': 'You do not have access to this function. Contact system administrator.'})
    
    #Find student and check they exist
    student = StudentModel.findById(id)

    if not student:
        return JsonResponse.notFound({'message': 'not_found', 'nice_message': 'Student not found.'})
        
    #Delete record of student
    student.delete()
    return JsonResponse.ok()