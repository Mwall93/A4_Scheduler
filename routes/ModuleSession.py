from flask import request, Blueprint, render_template, url_for, session

from datetime import datetime

from core import JsonResponse
from core import Database
from core import Config
from core import Authorization
from core import Scheduler

from model.ModuleSessionType import ModuleSessionType as ModuleSessionTypeModel
from model.ModuleSession import ModuleSession as ModuleSessionModel
from model.Module import Module as ModuleModel
from model.Teacher import Teacher as TeacherModel
from model.RoomBooking import RoomBooking as RoomBookingModel
from model.Campus import Campus as CampusModel
from model.CampusBuilding import CampusBuilding as CampusBuildingModel
from model.CampusBuildingRoom import CampusBuildingRoom as CampusBuildingRoomModel
from model.StudentModule import StudentModule as StudentModuleModel
from model.Term import Term as TermModel

ModuleSession = Blueprint('ModuleSession', __name__)

@ModuleSession.route('/module/<module_id>/session', methods=['GET'])
def List(module_id):
    """ Lists all sessions for given module. """
    # Verify user access
    if not Authorization.canAccess(session.get('user'), ('scheduling_admin')):
        return render_template('error/no_access.html')

    # Get module object
    module = ModuleModel.findById(module_id)

    if not module:
        return render_template('error/resource_not_found.html')
    
    # Get list of module sessions for given module
    sessions = ModuleSession.findBy('module', module_id)

    # Get a list of all teachers
    teachers = TeacherModel.all()

    # Get a list of all module session types
    session_types = ModuleSessionTypeModel.all()
    
    return render_template('session_list.html', data = {
        'module': module,
        'sessions': sessions,
        'teachers': teachers,
        'session_types': session_types
    })

    
@ModuleSession.route('/module/<module_id>/session', methods=['POST'])
def Create(module_id):
    """ Creates a new module session. """
    # Verify user access
    if not Authorization.canAccess(session.get('user'), ('scheduling_admin')):
        return JsonResponse.unauthorized({'message': 'no_access', 'nice_message': 'You do not have access to this page. Contact system administrator.'})

    # Get module object
    module = ModuleModel.findById(module_id)

    if not module:
        return JsonResponse.notFound({'message': 'not_found', 'nice_message': 'Module not found.'})

    # Parse and validate request body
    teacher      = request.form.get('teacher')
    sessionType  = request.form.get('type')

    if not TeacherModel.findById(teacher):
        return JsonResponse.badRequest({'message': 'not_found', 'nice_message': 'Teacher not found.'})
    
    if not ModuleSessionTypeModel.findById(sessionType):
        return JsonResponse.badRequest({'message': 'not_found', 'nice_message': 'Module session not found.'})

    # Save new data to database
    moduleSession = ModuleSessionModel()    

    moduleSession.setModule(module.getId()) \
                 .setStaff(teacher) \
                 .setType(sessionType) \
                 .save()

    return JsonResponse.ok()

    
@ModuleSession.route('/module/<module_id>/session/<session_id>', methods=['GET'])
def View(module_id, session_id):
    """ Returns module session information. """
    # Verify user access
    if not Authorization.canAccess(session.get('user'), ('scheduling_admin')):
        return render_template('error/no_access.html')
    
    # Get module object
    module = ModuleModel.findById(module_id)

    if not module:
        return render_template('error/resource_not_found.html')

    # Get session object
    theSession = ModuleSessionModel.findById(session_id)

    if not theSession:
        return render_template('error/resource_not_found.html')

    # Get the campus objects
    campus_list = CampusModel.all()
    campuses = []

    for campus in campus_list:
        buildings = CampusBuildingModel.findBy('campus', campus.getId())
        if(len(buildings) > 0):
            campuses.append({
                'campus': campus,
                'buildings': buildings
            })

    theSession = {
        'session': theSession,
        'staff': TeacherModel.findById(theSession.getStaff()),
        'type': ModuleSessionTypeModel.findById(theSession.getType()),
        'campuses': CampusModel.all()
    }

    # Get list of teachers
    teachers = TeacherModel.all()

    # Get list of session types
    session_types = ModuleSessionTypeModel.all()

    # Get terms
    terms = TermModel.all()
    term_list = []

    for term in terms:
        term_list.append({
            'term': term,
            'startDate': datetime.utcfromtimestamp(term.getStartDate()).strftime("%B %Y"),
            'endDate': datetime.utcfromtimestamp(term.getEndDate()).strftime("%B %Y")
        })

    # Get list of room bookings
    room_bookings = RoomBookingModel.findBy('module_session', session_id)
    room_bookings2 = []

    for booking in room_bookings:
        room = CampusBuildingRoomModel.findById(booking.getRoom())
        building = CampusBuildingModel.findById(room.getBuilding())
        campus = CampusModel.findById(building.getCampus())
        timeFrom = datetime.utcfromtimestamp(booking.getTimeFrom()).strftime("%Y-%m-%d %H:%M")
        timeTo   = datetime.utcfromtimestamp(booking.getTimeTo()).strftime("%Y-%m-%d %H:%M")

        room_bookings2.append({
            'booking': booking,
            'room': room,
            'building': building,
            'campus': campus,
            'timeFrom': timeFrom,
            'timeTo': timeTo
        })

    return render_template('session_view.html', data = {
        'module': module,
        'session': theSession,
        'teachers': teachers,
        'sessionTypes': session_types,
        'roomBookings': room_bookings2,
        'campuses': campuses,
        'terms': term_list
    })


@ModuleSession.route('/module/<module_id>/session/<session_id>', methods=['POST'])
def Update(module_id, session_id):
    """ Updates a module session. """
    # Verify user access
    if not Authorization.canAccess(session.get('user'), ('scheduling_admin')):
        return JsonResponse.unauthorized({'message': 'no_access', 'nice_message': 'You do not have access to this function. Contact system administrator.'})

    # Get session object
    session = ModuleSessionModel.findById(session_id)

    if not session:
        return JsonResponse.notFound({'message': 'not_found', 'nice_message': 'Session not found.'})
    
    # Save new values to database
    teacher     = request.form.get('teacher')
    sessionType = request.form.get('type')

    if not teacher and not sessionType:
        return JsonResponse.badRequest({'message': 'missing_parameters', 'nice_message': 'Please enter a teacher and session type.'})

    if teacher:
        if not TeacherModel.findById(teacher):
            return JsonResponse.badRequest({'message': 'not_found', 'nice_message': 'Teacher not found.'})

        session.setStaff(teacher)
    
    if sessionType:
        if not ModuleSessionModel.findById(sessionType):
            return JsonResponse.badRequest({'message': 'not_found', 'nice_message': 'Session type not found.'})
        
        session.setType(sessionType)
    
    session.save()

    return JsonResponse.ok()

    
@ModuleSession.route('/module/<module_id>/session/<session_id>', methods=['DELETE'])
def Delete(module_id, session_id):
    """ Deletes a module session. """
    # Verify user access
    if not Authorization.canAccess(session.get('user'), ('scheduling_admin')):
        return JsonResponse.unauthorized({'message': 'no_access', 'nice_message': 'You do not have access to this function. Contact system administrator.'})
    
    # Get session object
    theSession = ModuleSessionModel.findById(session_id)

    if not theSession:
        return JsonResponse.notFound({'message': 'not_found', 'nice_message': 'Session not found.'})
    
    # Delete from database
    theSession.delete()

    return JsonResponse.ok()
    
@ModuleSession.route('/module/<module_id>/session/<session_id>/booking', methods=['POST'])
def CreateBooking(module_id, session_id):
    """ Creates a new room booking. """
    # Verify user access
    if not Authorization.canAccess(session.get('user'), ('scheduling_admin')):
        return JsonResponse.unauthorized({'message': 'no_access', 'nice_message': 'You do not have access to this function. Contact sytem administrator.'})

    # Get session object
    theSession = ModuleSessionModel.findById(session_id)

    if not theSession:
        return JsonResponse.notFound({'message': 'not_found', 'nice_message': 'Session not found.'})

    module = ModuleModel.findById(theSession.getModule())

    if not module:
        return JsonResponse.internalServerError({'message': 'not_found', 'nice_message': 'Module not found.'})

    enrolments = StudentModuleModel.findBy('module', module.getId())
    
    # Get post values
    building_id = request.form.get('building')
    duration    = request.form.get('duration')
    day         = request.form.get('day')
    hour        = request.form.get('hour')

    duration = int(duration)

    if duration <= 0 or duration > 3:
        return JsonResponse.badRequest({'message': 'bad_request', 'nice_message': 'Please enter a duration between 1 and 3.'})

    if not building_id or not duration or not day or not hour:
        return JsonResponse.badRequest({'message': 'missing_parameters', 'nice_message': 'Please ensure you enter a buildng, duration and time.'})

    day = day + " 03:00" # Daylight savings time fix

    ts = int(datetime.strptime(day + " UTC", "%Y-%m-%d %H:%M %Z").strftime("%s"))

    building = CampusBuildingModel.findById(building_id)

    if not building:
        return JsonResponse.notFound({'message': 'not_found', 'nice_message': 'Building not found.'})

    #def scheduleOneOff(building_id, duration, capacity, day, hour, sessionType = None, session = None):
    res = Scheduler.scheduleOneOff(building_id, duration, len(enrolments), ts, hour, theSession.getType(), theSession.getId())

    if not res:
        return JsonResponse.badRequest({'message': 'booking_failed', 'nice_message': 'Booking not made.'})
    
    return JsonResponse.ok()

@ModuleSession.route('/module/<module_id>/session/<session_id>/booking/<booking_id>', methods=['DELETE'])
def DeleteBooking(module_id, session_id, booking_id):
    # Verify user access
    if not Authorization.canAccess(session.get('user'), ('scheduling_admin')):
        return JsonResponse.unauthorized({'message': 'no_access', 'nice_message': 'You do not have access to this function. Contact system administrator'})
    
    theBooking = RoomBookingModel.findById(booking_id)

    if not theBooking:
        return JsonResponse.notFound({'message': 'not_found', 'nice_message': 'Booking not found.'})
    
    theBooking.delete()

    return JsonResponse.ok()

@ModuleSession.route('/module/<module_id>/session/<session_id>/recurring_booking', methods=['POST'])
def CreateRecurringBooking(module_id, session_id):
    """ Updates a module session. """
    # Verify user access
    if not Authorization.canAccess(session.get('user'), ('scheduling_admin')):
        return JsonResponse.unauthorized({'message': 'no_access', 'nice_message': 'You do not have access to this function. Contact system administrator'})

    # Get session object
    theSession = ModuleSessionModel.findById(session_id)

    if not theSession:
        return JsonResponse.notFound({'message': 'not_found', 'nice_message': 'Session not found.'})

    module = ModuleModel.findById(theSession.getModule())

    if not module:
        return JsonResponse.internalServerError({'message': 'not_found', 'nice_message': 'Module not found.'})

    enrolments = StudentModuleModel.findBy('module', module.getId())
    
    # Get post values
    building_id = request.form.get('building')
    duration    = request.form.get('duration')
    day         = request.form.get('day')
    frequency   = request.form.get('frequency')
    term_id     = request.form.get('term')

    if not building_id or not duration or not day or not frequency or not term_id:
        return JsonResponse.badRequest({'message': 'missing_parameters', 'nice_message': 'Please enter a building, duration, day, frequency and term'})
    
    if day not in ('1', '2', '3', '4', '5'):
        return JsonResponse.badRequest({'message': 'bad_request', 'nice_message': 'Please choose a day Monday to Friday.'})
    
    day = int(day)
    
    if frequency not in ('1', '2', '3', '4', '5', '6', '7', '8'):
        return JsonResponse.badRequest({'message': 'bad_request', 'nice_message': 'Please select a frequency.'})

    frequency = int(frequency)
    duration = int(duration)

    if duration <= 0 or duration > 3:
        return JsonResponse.badRequest({'message': 'bad_requst', 'nice_message': 'Please select a duration betweene 1 and 3 hours.'})

    building = CampusBuildingModel.findById(building_id)

    if not building:
        return JsonResponse.notFound({'message': 'not_found', 'nice_message': 'Building not found.'})
    
    term = TermModel.findById(term_id)

    if not term:
        return JsonResponse.notFound({'message': 'not_found', 'nice_message': 'Term not found.'})

    #def scheduleRecurring(term_id, session_id, building_id, day_of_week, frequency, duration, sessionType):
    res = Scheduler.scheduleRecurring(term.getId(), theSession.getId(), building.getId(), day, frequency, duration, theSession.getType())

    #if not res:
    #    return JsonResponse.badRequest()
    
    return JsonResponse.ok()



