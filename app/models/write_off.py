from app.database import db


class WriteOff(db.Model):
    """
    Represents a write-off record within the application, useful for managing and tracking items that are written off.

    Attributes:
        __tablename__ (str): Defines the table name in the database for the Write_off model.
        id (db.Column): A unique integer identifier for each write-off record. It is the primary key.
        write_offs (db.Column): Stores the description or details of the write-off. It is a string of maximum length
        100 characters and cannot be null.

    The model includes a method `to_dict` for converting write-off entity attributes into a dictionary, which is
    suitable for JSON serialization or similar use cases.

    Methods:
        to_dict(self): Converts the Write_off instance into a dictionary containing 'id' and 'write_offs' as keys.
    """

    __tablename__ = 'write_off'
    id = db.Column(db.Integer, primary_key=True)
    write_offs = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        """
        Creates a dictionary representation of the Write_off instance, including the id and write-offs description.

        Returns:
            dict: A dictionary containing the 'id' and 'write_offs' of the write-off record.
        """
        return {
            'id': self.id,
            'write_offs': self.write_offs
        }
