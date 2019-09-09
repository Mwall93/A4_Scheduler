from core import Database

class Term:

    # Static methods which retrieve data from the database.
    @staticmethod
    def findById(id):
        rows = Database.getRows('SELECT * FROM `Term` WHERE `id` = %s', (id,))

        if len(rows) == 0:
            return None

        term = Term()
        term.setId(rows[0]['id'])
        term.setStartDate(rows[0]['start_date'])
        term.setEndDate(rows[0]['end_date'])
        term.setTerm(rows[0]['term'])

        return term

    @staticmethod
    def all():
        rows = Database.getRows('SELECT * FROM `Term`')

        out = []

        for i in rows:
            term = Term()
            term.setId(i['id'])
            term.setStartDate(i['start_date'])
            term.setEndDate(i['end_date'])
            term.setTerm(i['term'])
            out.append(term)

        return out

    @staticmethod
    def findBy(field, value):
        rows = Database.getRows('SELECT * FROM `Term` WHERE ' + field +' = %s', (value,))

        out = []

        for i in rows:
            term = Term()
            term.setId(i['id'])
            term.setStartDate(i['start_date'])
            term.setEndDate(i['end_date'])
            term.setTerm(i['term'])
            out.append(term)
            
        return out

    def __init__(self):
        self.id = None
        self.row = {}

        return

    def save(self):
        if self.id == None:
            # insert
            Database.execute('INSERT INTO `Term` (`start_date`, `end_date`, `term`) VALUES (%s, %s, %s)', (self.row['start_date'], self.row['end_date'], self.row['term'],))

            rows = Database.getRows('SELECT LAST_INSERT_ID() AS insert_id')
            self.id = rows[0]['insert_id']
        else:
            # update
            Database.execute('UPDATE `Term` SET `start_date` = %s, `end_date` = %s, `term` = %s WHERE `id` = %s', (self.row['start_date'], self.row['end_date'], self.row['term'], self.id))
    
    def delete(self):
        if self.id == None:
            return

        Database.execute('DELETE FROM `Term` WHERE `id` = %s', (self.id,))    

    # Methods for dealing with properties (setters and getters).
    def setId(self, id):
        self.id = id
        return self
    def getId(self):
        return self.id


    def setStartDate(self, start_date):
        self.row['start_date'] = start_date
        return self
    def getStartDate(self):
        return self.row['start_date']


    def setEndDate(self, end_date):
        self.row['end_date'] = end_date
        return self
    def getEndDate(self):
        return self.row['end_date']


    def setTerm(self, term):
        self.row['term'] = term
        return self
    def getTerm(self):
        return self.row['term']
