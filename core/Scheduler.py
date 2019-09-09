dayStart = 9
dayEnd = 17
maxSessionDuration = 3

from datetime import datetime
import math

from model.Term import Term as TermModel
from model.ModuleSessionType import ModuleSessionType as ModuleSessionTypeModel
from model.ModuleSession import ModuleSession as ModuleSessionModel
from model.Module import Module as ModuleModel
from model.Teacher import Teacher as TeacherModel
from model.CampusBuilding import CampusBuilding as CampusBuildingModel
from model.CampusBuildingRoom import CampusBuildingRoom as CampusBuildingRoomModel
from model.RoomBooking import RoomBooking as RoomBookingModel
from model.StudentModule import StudentModule as StudentModuleModel


def scheduleOneOff(building_id, duration, capacity, day, hour, sessionType = None, session = None):
    # getTimestampGivenDayAndHour(day, theStartHour)
    # getTimestampGivenDayAndHour(day, theStartHour + duration)
    duration = int(duration)
    capacity = int(capacity)
    day = int(day)
    hour = int(hour)
    sessionType = int(sessionType)
    session = int(session)
    
    timedate = getTimestampGivenDayAndHour(day, hour)

    if duration > maxSessionDuration:
        raise Error()
    
    # Book Room for session
    if session:
        # Get session and module object
        session = ModuleSessionModel.findById(session)
        module  = ModuleModel.findById(session.getModule())

        # Check teacher availability
        teacher = TeacherModel.findById(session.getStaff())

        if not isTeacherAvailable(teacher.getId(), timedate, timedate + hr2sec(duration)):
            return None

        # Check student availability
        enrolments = StudentModuleModel.findBy('module', module.getId())

        for enrolment in enrolments:
            if not isStudentAvailable(enrolment.getStudent(), timedate, timedate + hr2sec(duration)):
                return None

        # Get room
        room = getAvailableRoom(building_id, len(enrolments), session.getType(), timedate, timedate + hr2sec(duration))

        if not room:
            return None
        
        roomBooking = RoomBookingModel()

        roomBooking.setRoom(room.getId()) \
                   .setTimeFrom(timedate) \
                   .setTimeTo(timedate + hr2sec(duration)) \
                   .setModuleSession(session.getId()) \
                   .save()

        return roomBooking

    # Book Room for not session
    if not session:
        # Get free room that fits the requirements
        room = getAvailableRoom(building_id, capacity, sessionType, timedate, timedate + hr2sec(duration))

        if not room:
            raise None
        
        roomBooking = RoomBookingModel()

        roomBooking.setRoom(room.getId()) \
                   .setTimeFrom(timedate) \
                   .setTimeTo(timedate + hr2sec(duration)) \
                   .save()

        return roomBooking

    return None # fail safe


# building_id: Building ID
# day_of_week: Day of Week in form: 1 - 5 (monday = 1, friday = 5)
# frequency: Every X Weeks (every 1 week, every 2 weeks) (0 = one-off)
# duration: How long the session lasts for (in hours) (integer)
# type: lecture/seminar/lab/workshop/tutorials (string)
def scheduleRecurring(term_id, session_id, building_id, day_of_week, frequency, duration, sessionType):
    maxStartTime = dayEnd - duration

    # Sanity check
    if duration > maxSessionDuration:
        raise Error()
    
    roomBookings = []
    bookingFailures = []

    # get session
    session = ModuleSessionModel.findById(session_id)

    teacher_id = session.getStaff()

    # Get term and dates
    term = TermModel.findById(term_id)

    termStartDate = term.getStartDate()
    termEndDate = term.getEndDate()
    
    firstDay = getFirstDayOfWeekAfterDate(termStartDate, day_of_week)
    sessionDays = getDays(firstDay, termEndDate, frequency) # Every X weeks

    for day in sessionDays:
        for theStartHour in list(closed_range(dayStart, dayEnd - duration)):
            res = bookRoomOnDay(theStartHour, day, session_id, teacher_id, building_id, duration, sessionType)

            if res:
                break

        if res:
            roomBookings.append(res)
        else:
            bookingFailures.append(day) 
        
    return {'bookings': roomBookings, 'failures': bookingFailures}

# on success returns a RoomBooking object, on failure returns None
def bookRoomOnDay(theStartHour, day, session, teacher, building, duration, sessionType):
    # Check teacher availability
    if not isTeacherAvailable(teacher, getTimestampGivenDayAndHour(day, theStartHour), getTimestampGivenDayAndHour(day, theStartHour + duration)):
        return None
    
    # Check student availability
    session = ModuleSessionModel.findById(session)
    module = ModuleModel.findById(session.getModule())

    enrolments = StudentModuleModel.findBy('module', module.getId())

    for enrolment in enrolments:
        if not isStudentAvailable(enrolment.getStudent(), getTimestampGivenDayAndHour(day, theStartHour), getTimestampGivenDayAndHour(day, theStartHour + duration)):
            return None

    # Check room availability
    room = getAvailableRoom(building, len(enrolments), session.getType(), getTimestampGivenDayAndHour(day, theStartHour), getTimestampGivenDayAndHour(day, theStartHour + duration))

    if not room:
        return None
        
    booking = RoomBookingModel()

    booking.setRoom(room.getId()) \
           .setTimeFrom(getTimestampGivenDayAndHour(day, theStartHour)) \
           .setTimeTo(getTimestampGivenDayAndHour(day, theStartHour + duration)) \
           .setModuleSession(session.getId()) \
           .save()
                
    return booking

# ts = timestamp
def getAvailableRoom(building_id, num_students, session_type, ts_from, ts_to):
    rooms = getAppropriateRooms(building_id, num_students, session_type)

    for room in rooms:
        if _getAvailableRoomWork(room.getId(), ts_from, ts_to):
            return room
        
    return None

def _getAvailableRoomWork(room_id, ts_from, ts_to):
    bookings = RoomBookingModel.findBy('room', room_id)

    for booking in bookings:
        if hasClash(ts_from, ts_to, booking.getTimeFrom(), booking.getTimeTo()):
            return False
    
    return True

def isTeacherAvailable(teacher_id, ts_from, ts_to):
    sessions = ModuleSessionModel.findBy('staff', teacher_id)

    for session in sessions:
        bookings = RoomBookingModel.findBy('module_session', session.getId())

        for booking in bookings:
            if hasClash(ts_from, ts_to, booking.getTimeFrom(), booking.getTimeTo()):
                return False
    
    return True

def isStudentAvailable(student_id, ts_from, ts_to):
    enrolments = StudentModuleModel.findBy('student', student_id)
    modules = []

    for enrolment in enrolments:
        modules.append( ModuleModel.findById(enrolment.getModule()) )

    for module in modules:
        sessions = ModuleSessionModel.findBy('module', module.getId())

        for session in sessions:
            bookings = RoomBookingModel.findBy('module_session', session.getId())

            for booking in bookings:
                if hasClash(ts_from, ts_to, booking.getTimeFrom(), booking.getTimeTo()):
                    return False
    
    return True

def getAppropriateRooms(building_id, num_students, sessionType):
    rooms = CampusBuildingRoomModel.findBy('building', building_id)
    rooms.sort(key=lambda x: x.getCapacity(), reverse=False) # sort by capacity ascending
    out = []

    for room in rooms:
        if room.getCapacity() >= num_students:
            out.append(room)
    
    return out

def getDays(startDate, maxDate, weekFrequency):
    days = [startDate,]
    
    date = startDate
    date = date + (604800 * weekFrequency)
    while(date <= maxDate):
        days.append(date)
        date = date + (604800 * weekFrequency)

    return days

def getTimestampGivenDayAndHour(day, hour):
    #Day in Seconds
    DayInSeconds = 86400

    day = math.floor(day/DayInSeconds)

    day *= DayInSeconds

    hourInSeconds = 3600

    day += hour*hourInSeconds

    return day

def hr2sec(hour):
    return hour * 60 * 60

def closed_range(start, stop, step=1):
    dir = 1 if (step > 0) else -1
    return range(start, stop + dir, step)

def isAvailable(session, teacher, day_of_week, frequency, duration, sessionType, startHour, maxStartTime):
    # Check teacher availability
    teacher_sessions = ModuleSessionModel.findBy('staff', teacher.getId())

    for session in teacher_sessions:
        session_bookings = RoomBookingModel.findBy('module_session', session.getId())

        for booking in session_bookings:
            if hasClash(startHour, startHour + duration, booking.getTimeFrom(), booking.getTimeTo()):
                return False

def hasClash(start_a, end_a, start_b, end_b):
    if (start_a < end_b) and (end_a > start_b):
        return True
    
    return False

def getFirstDayOfWeekAfterDate(date, dayToFind = 1):
    if not dayToFind:
        dayToFind = 1

    #Day in Seconds
    DayInSeconds = 86400
    tdt = datetime.utcfromtimestamp(date)
    curWeekday = int(tdt.strftime("%w"))

    if dayToFind == curWeekday:
        return date

    if dayToFind > curWeekday:
        return date + (DayInSeconds * (dayToFind - curWeekday))

    # otherwise dayToFind < curWeekday therefore we need to get to end of week then add dayToFind
    remainingDays = 7 - curWeekday

    daysToAdd = remainingDays + dayToFind

    return date + (DayInSeconds * daysToAdd)