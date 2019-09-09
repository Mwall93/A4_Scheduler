from core import Database

class Teacher:

    # Static methods which retrieve data from the database.
    @staticmethod
    def findById(id):
        rows = Database.getRows('SELECT * FROM `Teacher` WHERE `id` = %s', (id,))

        if len(rows) == 0:
            return None
        
        teacher = Teacher()
        teacher.setId(rows[0]['id'])
        teacher.setFirstName(rows[0]['first_name'])
        teacher.setLastName(rows[0]['last_name'])
        teacher.setEmail(rows[0]['email'])
        teacher.setMobile(rows[0]['mobile'])
        teacher.setSalt(rows[0]['salt'])
        teacher.setPassword(rows[0]['password'])

        return teacher

    @staticmethod
    def all():
        rows = Database.getRows('SELECT * FROM  `Teacher`')

        out = []

        for i in rows:
            teacher = Teacher()
            teacher.setId(i['id'])
            teacher.setFirstName(i['first_name'])
            teacher.setLastName(i['last_name'])
            teacher.setEmail(i['email'])
            teacher.setMobile(i['mobile'])
            teacher.setSalt(i['salt'])
            teacher.setPassword(i['password'])
            out.append(teacher)

        return out
    @staticmethod
    def findBy(field, value):

        rows = Database.getRows('SELECT * FROM `Teacher` WHERE ' + field +' = %s', (value,))

        out = []

        for i in rows:
            teacher = Teacher()
            teacher.setId(i['id'])
            teacher.setFirstName(i['first_name'])
            teacher.setLastName(i['last_name'])
            teacher.setEmail(i['email'])
            teacher.setMobile(i['mobile'])
            teacher.setSalt(i['salt'])
            teacher.setPassword(i['password'])
            out.append(teacher)

        return out

    def __init__(self):
        self.id = None
        self.row = {}

        return


    def save(self):
        if self.id == None:
            # insert
            Database.execute('INSERT INTO `Teacher` (`first_name`, `last_name`, `email`, `mobile`, `salt`, `password`) VALUES (%s, %s, %s, %s, %s, %s)', (self.row['first_name'], self.row['last_name'], self.row['email'], self.row['mobile'], self.row['salt'], self.row['password'],))

            rows = Database.getRows('SELECT LAST_INSERT_ID() AS insert_id')
            self.id = rows[0]['insert_id']
        else:
            # update
            Database.execute('UPDATE `Teacher` SET `first_name` = %s, `last_name` = %s, `email` = %s, `mobile` = %s, `salt` = %s, `password` = %s WHERE `id` = %s', (self.row['first_name'], self.row['last_name'], self.row['email'], self.row['mobile'], self.row['salt'], self.row['password'], self.id))


    def delete(self):
        if self.id == None:
            return

        Database.execute('DELETE FROM `Teacher` WHERE `id` = %s', (self.id,))    

    # Methods for dealing with properties (setters and getters).
    def setId(self, id):
        self.id = id
        return self
    def getId(self):
        return self.id

    def setFirstName(self, first_name):
        self.row['first_name'] = first_name
        return self
    def getFirstName(self):
        return self.row['first_name']
        
    def setLastName(self, last_name):
        self.row['last_name'] = last_name
        return self
    def getLastName(self):
        return self.row['last_name']
        
    def setEmail(self, email):
        self.row['email'] = email
        return self
    def getEmail(self):
        return self.row['email']
        
    def setMobile(self, mobile):
        self.row['mobile'] = mobile
        return self
    def getMobile(self):
        return self.row['mobile']
        
    def setSalt(self, salt):
        self.row['salt'] = salt
        return self
    def getSalt(self):
        return self.row['salt']
        
    def setPassword(self, password):
        self.row['password'] = password
        return self
    def getPassword(self):
        return self.row['password']
        