from core import Database

class ModuleSessionType:
    # Static methods which retrieve data from the database.
    @staticmethod
    def findById(id):
        rows = Database.getRows('SELECT * FROM `ModuleSessionType` WHERE `id` = %s', (id,))

        if len(rows) == 0:
            return None

        sessionType = ModuleSessionType()
        sessionType.setId(rows[0]['id'])
        sessionType.setName(rows[0]['name'])
        sessionType.setDisplayName(rows[0]['display_name'])

        return sessionType

    @staticmethod
    def all():
        rows = Database.getRows('SELECT * FROM `ModuleSessionType`')
        
        out = []

        for i in rows:
            sessionType = ModuleSessionType()
            sessionType.setId(i['id'])
            sessionType.setName(i['name'])
            sessionType.setDisplayName(i['display_name'])
            out.append(sessionType)

        return out
    @staticmethod
    def findBy(field, value):
        rows = Database.getRows('SELECT * FROM `ModuleSessionType` WHERE ' + field +' = %s', (value,))

        out = []

        for i in rows:
            sessionType = ModuleSessionType()
            sessionType.setId(i['id'])
            sessionType.setName(i['name'])
            sessionType.setDisplayName(i['display_name'])
            out.append(sessionType)

        return out

    # Class Methods
    def __init__(self):
        self.id = None
        self.row = {}

        return

    def save(self):
        if self.id == None:
            # insert
            Database.execute('INSERT INTO `ModuleSessionType` (`name`, `display_name`) VALUES (%s, %s)', (self.row['name'], self.row['display_name'],))

            rows = Database.getRows('SELECT LAST_INSERT_ID() AS insert_id')
            self.id = rows[0]['insert_id']
        else:
            # update
            Database.execute('UPDATE `ModuleSessionType` SET `name` = %s, `display_name` = %s WHERE `id` = %s', (self.row['name'],self.row['display_name'],self.id))
    
    def delete(self):
        if self.id == None:
            return

        Database.execute('DELETE FROM `ModuleSessionType` WHERE `id` = %s', (self.id,))    

    # Methods for dealing with properties (setters and getters).
    
    def setId(self, id):
        self.id = id
        return self
    def getId(self):
        return self.id

    def setName(self, name):
        self.row['name'] = name
        return self
    def getName(self):
        return self.row['name']

    def setDisplayName(self, display_name):
        self.row['display_name'] = display_name
        return self
    def getDisplayName(self):
        return self.row['display_name']

    