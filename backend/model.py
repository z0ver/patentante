from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, userInfo):
        self.id = userInfo['id']
        self.name = userInfo['name']

    def __repr__(self):
        return str(self.id)

    def is_authenticated(self):
        return self.authenticated