from flask import request, Blueprint, render_template, url_for, session

from core import JsonResponse
from core import Database
from core import Config
from core import Authorization

from model.CampusBuilding import CampusBuilding as CampusBuildingModel
from model.Campus import Campus as CampusModel

CampusBuilding = Blueprint('CampusBuilding', __name__)

@CampusBuilding.route('/campus/<campus_id>/building', methods=['GET'])
def List(campus_id):
    """ List all buildings given the campus """
    # Verify user access
    if not Authorization.canAccess(session.get('user'), ('building_admin', 'fire_officer', 'scheduling_admin')):
        return render_template('error/no_access.html')

    # Get campus object
    campus = CampusModel.findById(campus_id)

    if not campus:
        return render_template('error/resource_not_found.html')

    # Get list of campus buildings
    buildings = CampusBuildingModel.findBy('campus', campus_id)
    
    return render_template('building_list.html', data = {
        'campus': campus,
        'buildings': buildings
    })


@CampusBuilding.route('/campus/<campus_id>/building', methods=['POST'])
def Create(campus_id):
    """ Creates new campus building """
    # Verify user access
    if not Authorization.canAccess(session.get('user'), ('building_admin',)):
        return JsonResponse.unauthorized()

    # Ensure campus exists
    campus = CampusModel.findById(campus_id)

    if not campus:
        return JsonResponse.notFound()
    
    # Parse and validate request body
    name       = request.form.get('building_name')
    floorCount = request.form.get('floor_count')

    if not name or not floorCount:
        return JsonResponse.badRequest()

    # Save new data to database
    building = CampusBuildingModel()

    building.setName(name) \
            .setFloorCount(floorCount) \
            .setCampus(campus_id) \
            .save()

    return JsonResponse.ok()
    

@CampusBuilding.route('/campus/<campus_id>/building/<building_id>', methods=['GET'])
def View(campus_id, building_id):
    """ Get building information """
    # Verify user access
    if not Authorization.canAccess(session.get('user'), ('building_admin', 'fire_officer', 'scheduling_admin')):
        return render_template('error/no_access.html')

    # Get campus object
    campus = CampusModel.findById(campus_id)

    if not campus:
        return render_template('error/resource_not_found.html')

    # Get building object
    building = CampusBuildingModel.findById(building_id)

    if not building:
        return render_template('error/resource_not_found.html')

    return render_template('building_view.html', data = {
        'campus': campus,
        'building': building
    })


@CampusBuilding.route('/campus/<campus_id>/building/<building_id>', methods=['POST'])
def Update(campus_id, building_id):
    """ Update information for given building """
    # Verify user access
    if not Authorization.canAccess(session.get('user'), ('building_admin',)):
        return JsonResponse.unauthorized({'message': 'no_access', 'nice_message': 'You do not have access to this function. Contact system administrator.'})

    # Get building object
    building = CampusBuildingModel.findById(building_id)

    if not building:
        return JsonResponse.notFound({'message': 'not_found', 'nice_message': 'Building not found.'})

    # Save new values to database
    name       = request.form.get('building_name')
    floorCount = request.form.get('floor_count')

    if not name and not floorCount:
        return JsonResponse.badRequest({'message': 'missing_parameter', 'nice_message': 'Please enter a new name or floor count.'})
    
    if name:
        building.setName(name)
    
    if floorCount:
        building.setFloorCount(floorCount)
    
    building.save()

    return JsonResponse.ok()


@CampusBuilding.route('/campus/<campus_id>/building/<building_id>', methods=['DELETE'])
def Delete(campus_id, building_id):
    """ Deletes a building """
    # Verify user access
    if not Authorization.canAccess(session.get('user'), ('building_admin',)):
        return JsonResponse.unauthorized({'message': 'no_access', 'nice_message': 'You do not have access to this function. Contact system administrator.'})

    # Get building object
    building = CampusBuildingModel.findById(building_id)

    if not building:
        return JsonResponse.notFound({'message': 'not_found', 'nice_message': 'Building not found.'})
    
    # Delete from database
    building.delete()
    
    return JsonResponse.ok()