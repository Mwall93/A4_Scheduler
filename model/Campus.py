from core import Database

class Campus:

    # Static methods which retrieve data from the database.
    @staticmethod
    def findById(id):
        rows = Database.getRows('SELECT * FROM `Campus` WHERE `id` = %s', (id,))

        if len(rows) == 0:
            return None
        
        campus = Campus()
        campus.setId(rows[0]['id'])
        campus.setName(rows[0]['name'])

        return campus
    
    @staticmethod
    def all():
        rows = Database.getRows('SELECT * FROM `Campus`')

        out = []

        for i in rows:
            campus = Campus()
            campus.setId(i['id'])
            campus.setName(i['name'])
            out.append(campus)

        return out

    @staticmethod
    def findBy(field, value):
        rows = Database.getRows('SELECT * FROM `Campus` WHERE ' + field +' = %s', (value,))

        out = []

        for i in rows:
            campus = Campus()
            campus.setId(i['id'])
            campus.setName(i['name'])
            out.append(campus)

        return out

    # Class Methods
    def __init__(self):
        self.id = None
        self.row = {}

        return
    
    def save(self):
        if self.id == None:
            # insert
            Database.execute('INSERT INTO `Campus` (`name`) VALUES (%s)', (self.row['name'],))

            rows = Database.getRows('SELECT LAST_INSERT_ID() AS insert_id')
            self.id = rows[0]['insert_id']
        else:
            # update
            Database.execute('UPDATE `Campus` SET `name` = %s WHERE `id` = %s', (self.row['name'], self.id))
    
    def delete(self):
        if self.id == None:
            return

        Database.execute('DELETE FROM `Campus` WHERE `id` = %s', (self.id,))    

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