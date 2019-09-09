from core import Database

class StaffRole:
    # Static methods which retrieve data from the database.
    @staticmethod
    def findById(id):
        rows = Database.getRows('SELECT * FROM `StaffRole` WHERE `id` = %s', (id,))

        if len(rows) == 0:
            return None

        staffRole = StaffRole()
        staffRole.setId(rows[0]['id'])
        staffRole.setName(rows[0]['name'])
        staffRole.setDisplayName(rows[0]['display_name'])

        return staffRole

    @staticmethod
    def all():
        rows = Database.getRows('SELECT * FROM `StaffRole`')

        out = []

        for i in rows:
            staffRole = StaffRole()
            staffRole.setId(i['id'])
            staffRole.setName(i['name'])
            staffRole.setDisplayName(i['display_name'])
            out.append(staffRole)

        return out
    @staticmethod
    def findBy(field, value):
        rows = Database.getRows('SELECT * FROM `StaffRole` WHERE ' + field +' = %s', (value,))

        out = []

        for i in rows:
            staffRole = StaffRole()
            staffRole.setId(i['id'])
            staffRole.setName(i['name'])
            staffRole.setDisplayName(i['display_name'])
            out.append(staffRole)

        return out

    # Class Methods
    def __init__(self):
        self.id = None
        self.row = {}

        return

    def save(self):
        if self.id == None:
            # insert
            Database.execute('INSERT INTO `StaffRole` (`name`, `display_name`) VALUES (%s, %s)', (self.row['name'], self.row['display_name'],))

            rows = Database.getRows('SELECT LAST_INSERT_ID() AS insert_id')
            self.id = rows[0]['insert_id']
        else:
            # update
            Database.execute('UPDATE `StaffRole` SET `name` = %s, `display_name` = %s WHERE `id` = %s', (self.row['name'],self.row['display_name'],self.id))
    
    def delete(self):
        if self.id == None:
            return

        Database.execute('DELETE FROM `StaffRole` WHERE `id` = %s', (self.id,))    

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

    