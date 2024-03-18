from app import db


class User(db.Model):
    __tablename__ = 'User'
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(50), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'user_type': self.user_type
        }
