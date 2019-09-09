from flask import request, Blueprint, render_template, url_for, session

from core import JsonResponse
from core import Database
from core import Config
from core import Authorization

from model.CampusBuildingRoom import CampusBuildingRoom as CampusBuildingRoomModel
from model.CampusBuilding import CampusBuilding as CampusBuildingModel
from model.Campus import Campus as CampusModel

CampusBuildingRoom = Blueprint('CampusBuildingRoom', __name__)

@CampusBuildingRoom.route('/campus/<campus_id>/building/<building_id>/room', methods=['GET'])
def List(campus_id, building_id):
    """ Lists all rooms for a given campus building. """
    # Verify user access
    if not Authorization.canAccess(session.get('user'), ('building_admin', 'fire_officer', 'scheduling_admin')):
        return render_template('error/no_access.html')

    # Get the campus object
    campus = CampusModel.findById(campus_id)

    if not campus:
        return render_template('error/resource_not_found.html')

    # Get the building object
    building = CampusBuildingModel.findById(building_id)

    if not building:
        return render_template('error/resource_not_found.html')

    # Get all rooms
    rooms = CampusBuildingRoomModel.findBy('building', building_id)
    
    return render_template('room_list.html', data = {
        'campus': campus,
        'building': building,
        'rooms': rooms
    })


@CampusBuildingRoom.route('/campus/<campus_id>/building/<building_id>/room', methods=['POST'])
def Create(campus_id, building_id):
    """ Create a room in a given campus building. """
    # Verify user access
    if not Authorization.canAccess(session.get('user'), ('building_admin')):
        return JsonResponse.unauthorized({'message': 'no_acces', 'nice_message': 'You do not have acess to this page. Contact system administrator.'})

    # Get building object
    building = CampusBuildingModel.findById(building_id)

    if not building:
        return JsonResponse.notFound({'message': 'not_found', 'nice_message': 'Building not found.'})

    # Parse and validate request body
    name  = request.form.get('room_name')
    floor = request.form.get('floor')
    capacity = request.form.get('capacity')


    if not name or not floor or not capacity:
        return JsonResponse.badRequest({'message': 'bad_request', 'nice_message': 'Please enter a capacity, name and floor.'})

    # Save new data to database
    room = CampusBuildingRoomModel()

    room.setIdentifier(name) \
        .setBuildingFloor(floor) \
        .setBuilding(building_id) \
        .setCapacity(capacity) \
        .save()

    return JsonResponse.ok()


@CampusBuildingRoom.route('/campus/<campus_id>/building/<building_id>/room/<room_id>', methods=['GET'])
def View(campus_id, building_id, room_id):
    """ Retrieve information for a given campus building room. """
    # Verify user access
    if not Authorization.canAccess(session.get('user'), ('building_admin', 'fire_officer', 'scheduling_admin')):
        return render_template('error/no_access.html')

    # Get the campus object
    campus = CampusModel.findById(campus_id)

    if not campus:
        return render_template('error/resource_not_found.html')

    # Get the building object
    building = CampusBuildingModel.findById(building_id)

    if not building:
        return render_template('error/resource_not_found.html')
    
    # Get the room object
    room = CampusBuildingRoomModel.findById(room_id)

    if not room:
        return render_template('error/resource_not_found.html')

    return render_template('room_view.html', data = {
        'campus': campus,
        'building': building,
        'room': room
    })

@CampusBuildingRoom.route('/campus/<campus_id>/building/<building_id>/room/<room_id>', methods=['POST'])
def Update(campus_id, building_id, room_id):
    """ Update a given campus building room. """
    # Verify user access
    if not Authorization.canAccess(session.get('user'), ('building_admin', 'fire_officer')):
        return JsonResponse.unauthorized({'message': 'no_access', 'nice_message': 'You do not have accdss to this page. Contact system administrator.'})

    # Get room object
    room = CampusBuildingRoomModel.findById(room_id)

    if not room:
        return JsonResponse.notFound({'message': 'room_missing', 'nice_message': 'Room not found.'})
    
    # Save new values to database
    name = request.form.get('room_name')
    floor = request.form.get('floor')
    capacity = request.form.get('capacity')


    if not name and not floor and not capacity:
        return JsonResponse.badRequest({'message': 'missing_parameters', 'nice_message': 'Please enter a floor, capacity or name.'})
    
    if name:
        room.setIdentifier(name)
    
    if floor:
        room.setBuildingFloor(floor)
    
    if capacity:
        room.setCapacity(capacity)

    room.save()

    return JsonResponse.ok()

@CampusBuildingRoom.route('/campus/<campus_id>/building/<building_id>/room/<room_id>', methods=['DELETE'])
def Delete(campus_id, building_id, room_id):
    """ Deletes a given campus building room. """
    # Verify user access
    if not Authorization.canAccess(session.get('user'), ('building_admin')):
        return JsonResponse.unauthorized({'message': 'no_access', 'nice_message': 'You do not have access to this function. Contact system administrator.'})

    # Get room object
    room = CampusBuildingRoomModel.findById(room_id)

    # Delete from database
    room.delete()

    return JsonResponse.ok()
