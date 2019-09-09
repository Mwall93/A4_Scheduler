from flask import request, Blueprint, render_template, url_for, session
from core import JsonResponse
from core import Database
from core import Config
from core import Security
from core import Authorization

from model.Staff import Staff as StaffModel
from model.StaffRole import StaffRole as StaffRoleModel

Staff = Blueprint('Staff', __name__)
@Staff.route('/staff', methods=['GET'])
def List():
    """GET /staff - Lists all staff members (Template: staff_list.html)"""
    if not Authorization.canAccess(session.get('user'), ('admin')):
        return render_template('error/no_access.html')
        
    roles = StaffRoleModel.all()
    
    allStaff = StaffModel.all()

    return render_template("staff_list.html", data = {
        "staff": allStaff,
        "roles": roles
    })

@Staff.route('/staff', methods=['POST'])
def Create():
    """POST /staff - Creates a new staff member (JSON) 
    (Post variables: first_name, last_name, email, mobile_phone, salt, password, role (integer))"""
    if not Authorization.canAccess(session.get('user'), ('admin')):
        return JsonResponse.unauthorized({'message': 'no_access', 'nice_message': 'You do not have access to this function. Contact system administrator.'})

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    mobile_phone = request.form.get('mobile_phone')
    role = request.form.get('role')
    password = request.form.get('password')

    #password = 'password1' #generatePassword()
    salt = Security.generateSalt()
    hashedPassword = Security.hashPassword(password, salt)
    
    staff = StaffModel()

    staff.setFirstName(first_name)
    staff.setLastName(last_name)
    staff.setEmail(email)
    staff.setMobile(mobile_phone)
    staff.setRole(role)
    staff.setPassword(hashedPassword)
    staff.setSalt(salt)
 
    try:
        staff.save()
    except:
        return JsonResponse.badRequest({'error': 'database_error'})
    
    return JsonResponse.ok()


@Staff.route('/staff/<id>', methods=['GET'])
def View(id):
    """GET /staff/[id] - Returns staff information (Template: staff_view.html)"""
    if not Authorization.canAccess(session.get('user'), ('admin')):
        return render_template('error/no_access.html')

    staff = StaffModel.findById(id)
    roles = StaffRoleModel.all()

    return render_template("staff_view.html", data={
        "staff": staff,
        "roles": roles
    })


@Staff.route('/staff/<id>', methods=['POST'])
def Update(id):
    """POST /staff/[id] - Updates staff information (JSON) (Post variables: first_name, last_name, email, mobile_phone, salt, password, role (integer))"""
    #Auth
    if not Authorization.canAccess(session.get('user'), ('admin')):
        return JsonResponse.unauthorized({'message': 'no_access', 'nice_message': 'You do not have access to this function. Contact system administrator.'})
     
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    mobile_phone = request.form.get('mobile_phone')
    password = request.form.get('password')
    role = request.form.get('role')

    if not first_name and not last_name and not email and not mobile_phone and not password and not role:
        #Bad request
        return JsonResponse.badRequest({'message': 'missing_parameters', 'nice_message': 'Pleaase enter new details for the staff member'})

    staff = StaffModel.findById(id)
    #Not sure on method names
    if first_name:
        staff.setFirstName(first_name)
    if last_name:
        staff.setLastName(last_name)
    if email:
        staff.setEmail(email)
    if mobile_phone:
        staff.setMobile(mobile_phone)
    if role:
        staff.setRole(role)
    #Password hashed here

    if password:
        salt = staff.getSalt()
        hashedPassword = Security.hashPassword(password, salt)
        staff.setPassword(hashedPassword)

    try:
        staff.save()
    except:
        return JsonResponse.badRequest({'error': 'database_error'})

    return JsonResponse.ok()



@Staff.route('/staff/<id>', methods=['DELETE'])
def Delete(id):
    """DELETE /staff/[id] - Deletes a staff member. (JSON)"""
    #Authorise 
    if not Authorization.canAccess(session.get('user'), ('admin')):
        return JsonResponse.unauthorized({'message': 'no_access', 'nice_message': 'You do not have access to this function. Contact system administrator.'})
    
    #Find student and check they exist
    staff = StaffModel.findById(id)

    if not staff:
        return JsonResponse.notFound({'message': 'not_found', 'nice_message': 'Staff member not found.'})
        
    #Delete record of student
    staff.delete()
    return JsonResponse.ok()
