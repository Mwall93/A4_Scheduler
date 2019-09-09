from core import Database

class PasswordReset:

    # Static methods which retrieve data from the database.
    @staticmethod
    def findById(id):
        rows = Database.getRows('SELECT * FROM `PasswordReset` WHERE `id` = %s', (id,))

        if len(rows) == 0:
            return None

        reset = PasswordReset()
        reset.setId(rows[0]['id'])
        reset.setToken(rows[0]['token'])
        reset.setUserId(rows[0]['user_id'])
        reset.setUserType(rows[0]['user_type'])
        reset.setExpires(rows[0]['expires'])
        
        return reset

    @staticmethod
    def all():
        rows = Database.getRows('SELECT * FROM `PasswordReset`')

        out = []

        for i in rows:
            reset = PasswordReset()
            reset.setId(i['id'])
            reset.setToken(i['token'])
            reset.setUserId(i['user_id'])
            reset.setUserType(i['user_type'])
            reset.setExpires(i['expires'])
            out.append(reset)
        
        return out

    # Class Methods
    def __init__(self):
        self.id = None
        self.row = {}

        return
    
    def save(self):
        if self.id == None:
            # insert
            Database.execute('INSERT INTO `PasswordReset` (`token`, `user_id`, `user_type`,`expires`) VALUES (%s, %s, %s, %s)', (self.row['token'], self.row['user_id'], self.row['user_type'], self.row['expires'],))

            rows = Database.getRows('SELECT LAST_INSERT_ID() AS insert_id')
            self.id = rows[0]['insert_id']
        else:
            # update
            Database.execute('UPDATE `PasswordReset` SET `token` = %s, `user_id` = %s, `user_type` = %s , `expires` = %s WHERE `id` = %s', (self.row['token'],self.row['user_id'],self.row['user_type'], self.row['expires'], self.id))
    
    def delete(self):
        if self.id == None:
            return

        Database.execute('DELETE FROM `PasswordReset` WHERE `id` = %s', (self.id,))    

    # Methods for dealing with properties (setters and getters).
    
    def setId(self, id):
        self.id = id
        return self
    def getId(self):
        return self.id
        
    def setToken(self, token):
        self.row['token'] = token
        return self
    def getToken(self):
        return self.row['token']

    def setUserId(self, user_id):
        self.row['user_id'] = user_id
        return self
    def getUserId(self):
        return self.row['user_id']

    def setUserType(self, user_type):
        self.row['user_type'] = user_type
        return self
    def getUserType(self):
        return self.row['user_type']

    def setExpires(self, expires):
        self.row['expires'] = expires
        return self
    def getExpires(self):
        return self.row['expires']