from core import Database

class RoomBooking:
    # Static methods which retrieve data from the database.
    @staticmethod
    def findById(id):
        rows = Database.getRows('SELECT * FROM `RoomBooking` WHERE `id` = %s', (id,))

        if len(rows) == 0:
            return None

        booking = RoomBooking()
        booking.setId(rows[0]['id'])
        booking.setRoom(rows[0]['room'])
        booking.setTimeFrom(rows[0]['time_from'])
        booking.setTimeTo(rows[0]['time_to'])
        booking.setModuleSession(rows[0]['module_session'])

        return booking

    @staticmethod
    def all():
        rows = Database.getRows('SELECT * FROM `RoomBooking`')

        out = []

        for i in rows:
            booking = RoomBooking()
            booking.setId(i['id'])
            booking.setRoom(i['room'])
            booking.setTimeFrom(i['time_from'])
            booking.setTimeTo(i['time_to'])
            booking.setModuleSession(i['module_session'])
            out.append(booking)

        return out

    @staticmethod
    def findBy(field, value):
        rows = Database.getRows('SELECT * FROM `RoomBooking` WHERE ' + field +' = %s', (value,))

        out = []

        for i in rows:
            booking = RoomBooking()
            booking.setId(i['id'])
            booking.setRoom(i['room'])
            booking.setTimeFrom(i['time_from'])
            booking.setTimeTo(i['time_to'])
            booking.setModuleSession(i['module_session'])
            out.append(booking)
            
        return out

    def __init__(self):
        self.id = None
        self.row = {}

        return

    def save(self):
        if self.id == None:
            # insert
            Database.execute('INSERT INTO `RoomBooking` (`room`, `time_from`, `time_to`,`module_session`) VALUES (%s, %s, %s, %s)', (self.row['room'], self.row['time_from'], self.row['time_to'],self.row['module_session'],))

            rows = Database.getRows('SELECT LAST_INSERT_ID() AS insert_id')
            self.id = rows[0]['insert_id']
        else:
            # update
            Database.execute('UPDATE `RoomBooking` SET `room` = %s, `time_from` = %s, `time_to` = %s, `module_session` = %s WHERE `id` = %s', (self.row['room'], self.row['time_from'], self.row['time_to'],self.row['module_session'], self.id))
    
    def delete(self):
        if self.id == None:
            return

        Database.execute('DELETE FROM `RoomBooking` WHERE `id` = %s', (self.id,))    

    # Methods for dealing with properties (setters and getters).
  
    def setId(self, id):
        self.id = id
        return self
    def getId(self):
        return self.id
    def setRoom(self, room):
        self.row['room'] = room
        return self
    def getRoom(self):
        return self.row['room']

    def setTimeFrom(self, time_from):
        self.row['time_from'] = time_from
        return self
    def getTimeFrom(self):
        return self.row['time_from']

    def setTimeTo(self, time_to):
        self.row['time_to'] = time_to
        return self
    def getTimeTo(self):
        return self.row['time_to']

    def setModuleSession(self, module_session):
        self.row['module_session'] = module_session
        return self
    def getModuleSession(self):
        return self.row['module_session']
        
