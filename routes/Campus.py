from flask import request, Blueprint, render_template, url_for, session

from core import JsonResponse
from core import Database
from core import Config
from core import Authorization

from model.Campus import Campus as CampusModel

Campus = Blueprint('Campus', __name__)

@Campus.route('/campus', methods=['GET'])
def List():
    """ Lists all campuses using campus_list.html """
    # Authenticate user
    if not Authorization.canAccess(session.get('user'), ('building_admin', 'fire_officer', 'scheduling_admin')):
        return render_template('error/no_access.html')
    
    # Get list of campuses
    campuses = CampusModel.all()

    return render_template('campus_list.html', data = {
        'campuses': campuses
    })


@Campus.route('/campus', methods=['POST'])
def Create():
    """ Creates a new Campus """
    # Authenticate user
    if not Authorization.canAccess(session.get('user'), ('building_admin')):
        return JsonResponse.unauthorized({'message': 'no_access', 'nice_message': 'You do not have access to this function. Contact system administrator.'})

    name = request.form.get('campus_name')

    if not name:
        return JsonResponse.badRequest({'message': 'name_missing', 'nice_message': 'Missing Campus Name'})
        
    campus = CampusModel()

    campus.setName(name) \
          .save()

    return JsonResponse.ok()


@Campus.route('/campus/<id>', methods=['GET'])
def View(id):
    """ Gets campus information and displays it using campus_view.html """
    # Authenticate user
    if not Authorization.canAccess(session.get('user'), ('building_admin', 'fire_officer', 'scheduling_admin')):
        return render_template('error/no_access.html')
    
    campus = CampusModel.findById(id)   

    if not campus:
        return render_template('error/resource_not_found.html')    

    return render_template('campus_view.html', data = {
        'campus': campus
    })
    

@Campus.route('/campus/<id>', methods=['POST'])
def Update(id):
    """ Updates information for a Campus """
    if not Authorization.canAccess(session.get('user'), ('building_admin')):
        return JsonResponse.unauthorized({'message': 'no_access', 'nice_message': 'You do not have access to this function. Contact system administrator.'})
  
    name = request.form.get('campus_name')

    if not name:
        return JsonResponse.badRequest({'message': 'name_missing', 'nice_message': 'Missing campus name.'})

    campus = CampusModel.findById(id)

    if not campus:
        return JsonResponse.notFound({'message': 'not_found', 'nice_message': 'Campus could not be found.'})

    campus.setName(name) \
          .save()

    return JsonResponse.ok()


@Campus.route('/campus/<id>', methods=['DELETE'])
def Delete(id):
    """ Deletes a Campus """
    if not Authorization.canAccess(session.get('user'), ('building_admin')):
        return JsonResponse.unauthorized({'message': 'no_access', 'nice_message': 'You do not have access to this function. Contact system administrator.'})

    campus = CampusModel.findById(id)

    if not campus:
        return JsonResponse.notFound({'message': 'not_found', 'nice_message': 'Campus could not be found.'})

    campus.delete()
    
    return JsonResponse.ok()
