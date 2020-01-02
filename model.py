import sqlalchemy

db = sqlalchemy()

class Users(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user = db.Column(db.String, nullable=False)
        email = db.Column(db.String, unique=True, nullable=False)
    
        def __repr__(self):
            return '<Users {} {}>'.format(self.user, self.email)