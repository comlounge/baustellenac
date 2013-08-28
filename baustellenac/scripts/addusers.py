from starflyer.scripts import ScriptBase
from baustellenac import db


class AddUsers(ScriptBase):
    """script to sync the userids with entries which have a profile set"""

    def __call__(self):
        self.app.module_map['userbase'].register({
            'email' : 'cr@comlounge.net',
            'fullname' : 'Carsten Rebbien',
            'password' : 'admin'
        }, force = True, create_pw = False)
        self.app.module_map['userbase'].register({
            'email' : 'cs@comlounge.net',
            'fullname' : 'Christian Scholz',
            'password' : 'admin'
        }, force = True, create_pw = False)
        self.app.module_map['userbase'].register({
            'email' : 'klaus.dosch',
            'fullname' : 'Klaus Dosch',
            'password' : 'kdadmin'
        }, force = True, create_pw = False)



def addusers():
    f = AddUsers()
    f()

if __name__=="__main__":
    addusers()
