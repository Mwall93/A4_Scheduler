from core import Database

import time
import calendar
from datetime import datetime

def getStudentTimetable(studentId, timeFrom, timeTo):
    query = "SELECT r.`identifier` as room, b.`name` as building, c.`name` as campus, rb.`time_from`, rb.`time_to`, st.`display_name` as session_type, ss.`first_name` AS staff_first_name, ss.`last_name` AS staff_last_name, m.`name` AS module FROM `Room` r, `Building` b, `Campus` c, `RoomBooking` rb, `ModuleSessionType` st, `ModuleSession` s, `Teacher` ss, `Module` m WHERE rb.`module_session` IN (SELECT `id` FROM `ModuleSession` WHERE `module` IN (SELECT `module` FROM `StudentModule` WHERE `student` = %s)) AND rb.`time_from` >= %s AND rb.`time_to` <= %s AND rb.`room` = r.`id` AND r.`building` = b.`id` AND b.`campus` = c.`id` AND rb.`module_session` = s.`id` AND s.`type` = st.`id` AND s.`staff` = ss.`id` AND s.`module` = m.`id`"

    return Database.getRows(query, (studentId, timeFrom, timeTo))

def getTeacherTimetable(teacherId, timeFrom, timeTo):
    query = "SELECT r.`identifier` as room, b.`name` as building, c.`name` as campus, rb.`time_from`, rb.`time_to`, st.`display_name` as session_type, m.`name` FROM `Room` r, `Building` b, `Campus` c, `RoomBooking` rb, `ModuleSessionType` st, `ModuleSession` s, `Module` m WHERE rb.`module_session` IN (SELECT `id` FROM `ModuleSession` WHERE `staff` = %s) AND rb.`time_from` > %s AND rb.`time_to` < %s AND rb.`room` = r.`id` AND r.`building` = b.`id` AND b.`campus` = c.`id` AND rb.`module_session` = s.`id` AND s.`type` = st.`id` AND s.`module` = m.`id`"

    return Database.getRows(query, (teacherId, timeFrom, timeTo))

def getStartOfMonth(curTime=None):
    #returns start of month 6am
    if not curTime:
        curTime = time.time()

    newdate = datetime.utcfromtimestamp(curTime)

    newdate = newdate.replace(day=1) 
    newdate = newdate.replace(hour=6)
    newdate = newdate.replace(minute=0) 
    newdate = newdate.replace(second=0)

    unixtime = time.mktime(newdate.timetuple())

    return unixtime

def getEndOfMonth(curTime=None):
    #returns end of month 9pm

    if not curTime:
        curTime = time.time()

    newdate = datetime.utcfromtimestamp(curTime)

    #day = newdate.day()
    month = newdate.month
    year = newdate.year

    dateRange = calendar.monthrange(year,month)

    newdate = newdate.replace(day=dateRange[1])
    newdate = newdate.replace(hour=20)
    newdate = newdate.replace(minute=0) 
    newdate = newdate.replace(second=0)

    unixtime = time.mktime(newdate.timetuple())

    return unixtime