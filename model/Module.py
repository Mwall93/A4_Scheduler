from core import Database

class Module:
    # Static methods which retrieve data from the database.
    @staticmethod
    def findById(id):
        rows = Database.getRows('SELECT * FROM `Module` WHERE `id` = %s', (id,))

        if len(rows) == 0:
            return None
        
        module = Module()
        module.setId(rows[0]['id'])
        module.setName(rows[0]['name'])
        module.setLeader(rows[0]['leader'])

        return module

    @staticmethod
    def all():
        rows = Database.getRows('SELECT * FROM `Module`')

        out = []

        for i in rows:
            module = Module()
            module.setId(i['id'])
            module.setName(i['name'])
            module.setLeader(i['leader'])
            out.append(module)

        return out
    
    @staticmethod
    def findBy(field, value):
        rows = Database.getRows('SELECT * FROM `Module` WHERE ' + field +' = %s', (value,))

        out = []

        for i in rows:
            module = Module()
            module.setId(i['id'])
            module.setName(i['name'])
            module.setLeader(i['leader'])
            out.append(module)


        return out



    def __init__(self):
        self.id = None
        self.row = {}

        return

    def save(self):
        if self.id == None:
            # insert
            Database.execute('INSERT INTO `Module` (`name`, `leader`) VALUES (%s, %s)', (self.row['name'], self.row['leader'],))

            rows = Database.getRows('SELECT LAST_INSERT_ID() AS insert_id')
            self.id = rows[0]['insert_id']
        else:
            # update
            Database.execute('UPDATE `Module` SET `name` = %s, `leader` = %s WHERE `id` = %s', (self.row['name'],self.row['leader'], self.id))
    
    def delete(self):
        if self.id == None:
            return

        Database.execute('DELETE FROM `Module` WHERE `id` = %s', (self.id,))    

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

    def setLeader(self, leader):
        self.row['leader'] = leader
        return self
    def getLeader(self):
        return self.row['leader']