from model.Staff import Staff as StaffModel
from model.StaffRole import StaffRole as StaffRoleModel

def canAccess(user_id, roles):
    #return True

    if not user_id:
        return False

    user = StaffModel.findById(user_id)

    if not user:
        return False

    role = StaffRoleModel.findById(user.getRole())

    if role.getName() == 'admin':
        return True

    if role.getName() in roles:
        return True

    return False

def isLoggedIn(user_id):
    if not user_id:
        return False
    
    user = StaffModel.findById(user_id)

    if not user:
        return False

    return True