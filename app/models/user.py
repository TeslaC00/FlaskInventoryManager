from app.database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    flag = db.Column(db.String(120))

    def __repr__(self):
        return '<User %r>' % self.username
