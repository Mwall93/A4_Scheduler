from core import Database

class CampusBuildingRoom:
    # Static methods which retrieve data from the database.
    @staticmethod
    def findById(id):
        rows = Database.getRows('SELECT * FROM `Room` WHERE `id` = %s', (id,))

        if len(rows) == 0:
            return None
        
        room = CampusBuildingRoom()
        room.setId(rows[0]['id'])
        room.setIdentifier(rows[0]['identifier'])
        room.setBuildingFloor(rows[0]['building_floor'])
        room.setBuilding(rows[0]['building'])
        room.setCapacity(rows[0]['capacity'])

        return room

    @staticmethod
    def all():
        rows = Database.getRows('SELECT * FROM `Room`')

        out = []

        for i in rows:
            room = CampusBuildingRoom()
            room.setId(i['id'])
            room.setIdentifier(i['identifier'])
            room.setBuildingFloor(i['building_floor'])
            room.setBuilding(i['building'])
            room.setCapacity(i['capacity'])
            out.append(room)

        return out
    
    @staticmethod
    def findBy(field, value):
        rows = Database.getRows('SELECT * FROM `Room` WHERE ' + field +' = %s', (value,))

        out = []

        for i in rows:
            room = CampusBuildingRoom()
            room.setId(i['id'])
            room.setIdentifier(i['identifier'])
            room.setBuildingFloor(i['building_floor'])
            room.setBuilding(i['building'])
            room.setCapacity(i['capacity'])
            out.append(room)

        return out


    def __init__(self):
        self.id = None
        self.row = {}

        return

    def save(self):
        if self.id == None:
            # insert
            Database.execute('INSERT INTO `Room` (`identifier`, `building_floor`, `building`, `capacity`) VALUES (%s, %s, %s, %s)', (self.row['identifier'], self.row['building_floor'], self.row['building'], self.row['capacity']))

            rows = Database.getRows('SELECT LAST_INSERT_ID() AS insert_id')
            self.id = rows[0]['insert_id']
        else:
            # update
            Database.execute('UPDATE `Room` SET `identifier` = %s, `building_floor` = %s, `building` = %s, `capacity` = %s WHERE `id` = %s', (self.row['identifier'],self.row['building_floor'],self.row['building'], self.row['capacity'], self.id))

    def delete(self):
        if self.id == None:
            return

        Database.execute('DELETE FROM `Room` WHERE `id` = %s', (self.id,))    

    # Methods for dealing with properties (setters and getters).

    def setId(self, id):
        self.id = id
        return self
    def getId(self):
        return self.id

    def setIdentifier(self, identifier):
        self.row['identifier'] = identifier
        return self
    def getIdentifier(self):
        return self.row['identifier']

    def setBuildingFloor(self, building_floor):
        self.row['building_floor'] = building_floor
        return self
    def getBuildingFloor(self):
        return self.row['building_floor']

    def setBuilding(self, building):
        self.row['building'] = building  
        return self
    def getBuilding(self):
        return self.row['building']
    
    def setCapacity(self, capacity):
        self.row['capacity'] = capacity
        return self
    def getCapacity(self):
        return self.row['capacity']