from app.database import db


class Write_off(db.Model):
    __tablename__ = 'Write_off'
    id = db.Column(db.Integer, primary_key=True)
    write_offs = db.Column(db.String(100), nullable=False)
