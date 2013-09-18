# coding=utf-8

from starflyer.scripts import ScriptBase
from baustellenac import db


USERNAMES = [
    #'dosch@aachener-stiftung.de',
    'render@aachener-stiftung.de',
    'vallee@aachener-stiftung.de',
    'simon@aachener-stiftung.de',
    'tappesser@aachener-stiftung.de',
    'schiffler@aachener-stiftung.de',
    'sachsen@aachener-stiftung.de',
    'baldin@aachener-stiftung.de',
]

MAIL_TEMPLATE = u"""
Hallo %(un)s,

Ihr Passwort für das Baustellenprojekt lautet: %(pw)s
"""

class AddUsers(ScriptBase):
    """script to sync the userids with entries which have a profile set"""

    def __call__(self, reset_db=False, send_mail=False):
        if reset_db:
            pass
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
            'email' : 'dosch@aachener-stiftung.de',
            'fullname' : 'Klaus Dosch',
            'password' : 'kdadmin'
        }, force = True, create_pw = False)

        for username in USERNAMES:
            u = self.app.module_map['userbase'].register({
                'email' : username,
                'fullname' : username,
                'password' : ''
            }, force = True, create_pw = False)
            pw = u.create_pw()
            u.save()

            print '%s %s' % (username, pw)

            #txt = MAIL_TEMPLATE % {'un':username, 'pw':pw}
            #mailer = self.app.module_map['mail']
            #mailer.mail(username, 'Ihr Zugang zum Baustellen-Projekt', txt)

    def extend_parser(self):
        """add the location of the file to the parser"""
        self.parser.add_argument('-R', '--reset-db', help='reset user db', action="store_true")
        self.parser.add_argument('-s', '--send-mail', help='send the password to each user', action="store_true")

def addusers():
    f = AddUsers()
    args = f.parser.parse_args()
    f(args.reset_db, args.send_mail)

if __name__=="__main__":
    addusers()
