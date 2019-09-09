from core import Database

class CampusBuilding:
    # Static methods which retrieve data from the database.
    @staticmethod
    def findById(id):
        rows = Database.getRows('SELECT * FROM `Building` WHERE `id` = %s', (id,))

        if len(rows) == 0:
            return None

        building = CampusBuilding()
        building.setId(rows[0]['id'])
        building.setName(rows[0]['name'])
        building.setFloorCount(rows[0]['floor_count'])
        building.setCampus(rows[0]['campus'])

        return building

    @staticmethod
    def all():
        rows = Database.getRows('SELECT * FROM  `Building`')

        out = []

        for i in rows:
            building = CampusBuilding()
            building.setId(i['id'])
            building.setName(i['name'])
            building.setFloorCount(i['floor_count'])
            building.setCampus(i['campus'])
            out.append(building)

        return out
    @staticmethod
    def findBy(field, value):
        rows = Database.getRows('SELECT * FROM `Building` WHERE ' + field +' = %s', (value,))

        out = []

        for i in rows:
            building = CampusBuilding()
            building.setId(i['id'])
            building.setName(i['name'])
            building.setFloorCount(i['floor_count'])
            building.setCampus(i['campus'])
            out.append(building)

        return out

    def __init__(self):
        self.id = None
        self.row = {}

        return

    def save(self):
        if self.id == None:
            # insert
            Database.execute('INSERT INTO `Building` (`name`, `floor_count`, `campus`) VALUES (%s, %s, %s)', (self.row['name'], self.row['floor_count'], self.row['campus'],))

            rows = Database.getRows('SELECT LAST_INSERT_ID() AS insert_id')
            self.id = rows[0]['insert_id']
        else:
            # update
            Database.execute('UPDATE `Building` SET `name` = %s, `floor_count` = %s, `campus` = %s WHERE `id` = %s', (self.row['name'],self.row['floor_count'],self.row['campus'], self.id))


    def delete(self):
        if self.id == None:
            return

        Database.execute('DELETE FROM `Building` WHERE `id` = %s', (self.id,))    

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

    def setFloorCount(self, floor_count):
        self.row['floor_count'] = floor_count
        return self

    def getFloorCount(self):
        return self.row['floor_count']

    def setCampus(self, campus):
        self.row['campus'] = campus
        return self

    def getCampus(self):
        return self.row['campus']
