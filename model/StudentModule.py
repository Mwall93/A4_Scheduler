from core import Database

class StudentModule:

    # Static methods which retrieve data from the database.
    @staticmethod
    def findById(id):
        rows = Database.getRows('SELECT * FROM `StudentModule` WHERE `id` = %s', (id,))

        if len(rows) == 0:
            return None
        
        studentModule = StudentModule()
        studentModule.setId(rows[0]['id'])
        studentModule.setModule(rows[0]['module'])
        studentModule.setStudent(rows[0]['student'])
        studentModule.setEnrolmentDate(rows[0]['enrolment_date'])

        return studentModule
    
    @staticmethod
    def all():
        rows = Database.getRows('SELECT * FROM `StudentModule`')

        out = []

        for i in rows:
            studentModule = StudentModule()
            studentModule.setId(i['id'])
            studentModule.setModule(i['module'])
            studentModule.setStudent(i['student'])
            studentModule.setEnrolmentDate(i['enrolment_date'])
            out.append(studentModule)

        return out

    @staticmethod
    def findBy(field, value):
        rows = Database.getRows('SELECT * FROM `StudentModule` WHERE ' + field +' = %s', (value,))

        out = []

        for i in rows:
            studentModule = StudentModule()
            studentModule.setId(i['id'])
            studentModule.setModule(i['module'])
            studentModule.setStudent(i['student'])
            studentModule.setEnrolmentDate(i['enrolment_date'])
            out.append(studentModule)

        return out

    # Class Methods
    def __init__(self):
        self.id = None
        self.row = {}

        return
    
    def save(self):
        if self.id == None:
            # insert
            Database.execute('INSERT INTO `StudentModule` (`module`,`student`, `enrolment_date`) VALUES (%s, %s, %s)', (self.row['module'],self.row['student'], self.row['enrolment_date']))

            rows = Database.getRows('SELECT LAST_INSERT_ID() AS insert_id')
            self.id = rows[0]['insert_id']
        else:
            # update
            Database.execute('UPDATE `StudentModule` SET `module` = %s ,`student` = %s, `enrolment_date` = %s WHERE `id` = %s', (self.row['module'],self.row['student'], self.row['enrolment_date'], self.id))
    
    def delete(self):
        if self.id == None:
            return

        Database.execute('DELETE FROM `StudentModule` WHERE `id` = %s', (self.id,))    

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


    def setStudent(self, student):
        self.row['student'] = student
        return self
    def getStudent(self):
        return self.row['student']

    def setEnrolmentDate(self, enrolment_date):
        self.row['enrolment_date'] = enrolment_date
        return self
    def getEnrolmentDate(self):
        return self.row['enrolment_date']