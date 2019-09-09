from core import Database

class ModuleSession:
    # Static methods which retrieve data from the database.
    @staticmethod
    def findById(id):
        rows = Database.getRows('SELECT * FROM `ModuleSession` WHERE `id` = %s', (id,))

        if len(rows) == 0:
            return None

        session = ModuleSession()
        session.setId(rows[0]['id'])
        session.setModule(rows[0]['module'])
        session.setStaff(rows[0]['staff'])
        session.setType(rows[0]['type'])

        return session

    @staticmethod
    def all():
        rows = Database.getRows('SELECT * FROM `ModuleSession`')

        out = []

        for i in rows:
            session = ModuleSession()
            session.setId(i['id'])
            session.setModule(i['module'])
            session.setStaff(i['staff'])
            session.setType(i['type'])
            out.append(session)

        return out

    @staticmethod
    def findBy(field, value):
        rows = Database.getRows('SELECT * FROM `ModuleSession` WHERE ' + field +' = %s', (value,))

        out = []

        for i in rows:
            session = ModuleSession()
            session.setId(i['id'])
            session.setModule(i['module'])
            session.setStaff(i['staff'])
            session.setType(i['type'])
            out.append(session)

        return out


    def __init__(self):
        self.id = None
        self.row = {}

        return

    def save(self):
        if self.id == None:
            # insert
            Database.execute('INSERT INTO `ModuleSession` (`module`, `staff`, `type`) VALUES (%s, %s, %s)', (self.row['module'], self.row['staff'], self.row['type'],))

            rows = Database.getRows('SELECT LAST_INSERT_ID() AS insert_id')
            self.id = rows[0]['insert_id']
        else:
            # update
            Database.execute('UPDATE `ModuleSession` SET `module` = %s, `staff` = %s, `type` = %s WHERE `id` = %s', (self.row['module'],self.row['staff'],self.row['type'], self.id))
    
    def delete(self):
        if self.id == None:
            return

        Database.execute('DELETE FROM `ModuleSession` WHERE `id` = %s', (self.id,))    

    # Methods for dealing with properties (setters and getters).
    
    def setId(self, id):
        self.id = id
        return self
    def getId(self):
        return self.id
    
    def setModule(self, module):
        self.row['module'] = module
        return self
    def getModule(self):
        return self.row['module']

    def setStaff(self, staff):
        self.row['staff'] = staff
        return self
    def getStaff(self):
        return self.row['staff']

    def setType(self, types):
        self.row['type'] = types
        return self
    def getType(self):
        return self.row['type']
