from core import Database

class Timetable:
    # Static methods which retrieve data from the database.
    @staticmethod
    def timetableStudent(id):
        Mrows = Database.getRows('SELECT module FROM `studentModule` WHERE `student` = %s', (id,))

        if len(Mrows) == 0:
            return None
        
        module = rows[0]
    
        srows = Database.getRows('SELECT id FROM `moduleSession` WHERE `module` = %s', (module,))
        
        if len(srows) == 0:
            return None
        
        session = rows[0]
        
        rows = Database.getRows('SELECT all FROM `roombooking` WHERE `module_session` = %s', (session,))
        
        if len(srows) == 0:
            return None
        
        times = timetable()
        times.setmodule(rows[0]['id'])
        times.setStart(rows[0]['identifier'])
        times.setEnd(rows[0]['building_floor'])
        times.setRoom(rows[0]['building'])
        

        return times

    @staticmethod
    def TimetableStaff(id):
    
        srows = Database.getRows('SELECT id FROM `moduleSession` WHERE `staff` = %s', (module,))
        
        if len(srows) == 0:
            return None
        
        session = rows[0]
        
        rows = Database.getRows('SELECT all FROM `roombooking` WHERE `module_session` = %s', (session,))
        
        if len(srows) == 0:
            return None
        
        times = timetable()
        times.setmodule(rows[0]['id'])
        times.setStart(rows[0]['identifier'])
        times.setEnd(rows[0]['building_floor'])
        times.setRoom(rows[0]['building'])
        

        return times