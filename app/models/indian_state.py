from app.extensions import db


# Note: This is a Static Model and all values should be predefined.
#       This is available in readonly access to user.
class IndianState(db.Model):
    __tablename__ = 'indian_state'
    id = db.Column(db.Integer, primary_key=True)  # use as state code
    name = db.Column(db.String(80), unique=True, nullable=False)
    abbreviation = db.Column(db.String(10), unique=True, nullable=False)

    @staticmethod
    def load_state():
        data = [
            {"id": 1, "name": "Jammu and Kashmir", "abbreviation": "JK"},
            {"id": 2, "name": "Himachal Pradesh", "abbreviation": "HP"},
            {"id": 3, "name": "Punjab", "abbreviation": "PB"},
            {"id": 4, "name": "Chandigarh", "abbreviation": "CH"},
            {"id": 5, "name": "Uttarakhand", "abbreviation": "UK"},
            {"id": 6, "name": "Haryana", "abbreviation": "HR"},
            {"id": 7, "name": "Delhi", "abbreviation": "DL"},
            {"id": 8, "name": "Rajasthan", "abbreviation": "RJ"},
            {"id": 9, "name": "Uttar Pradesh", "abbreviation": "UP"},
            {"id": 10, "name": "Bihar", "abbreviation": "BR"},
            {"id": 11, "name": "Sikkim", "abbreviation": "SK"},
            {"id": 12, "name": "Arunachal Pradesh", "abbreviation": "AR"},
            {"id": 13, "name": "Nagaland", "abbreviation": "NL"},
            {"id": 14, "name": "Manipur", "abbreviation": "MN"},
            {"id": 15, "name": "Mizoram", "abbreviation": "MZ"},
            {"id": 16, "name": "Tripura", "abbreviation": "TR"},
            {"id": 17, "name": "Meghalaya", "abbreviation": "ML"},
            {"id": 18, "name": "Assam", "abbreviation": "AS"},
            {"id": 19, "name": "West Bengal", "abbreviation": "WB"},
            {"id": 20, "name": "Jharkhand", "abbreviation": "JH"},
            {"id": 21, "name": "Odisha", "abbreviation": "OR"},
            {"id": 22, "name": "Chhattisgarh", "abbreviation": "CG"},
            {"id": 23, "name": "Madhya Pradesh", "abbreviation": "MP"},
            {"id": 24, "name": "Gujarat", "abbreviation": "GJ"},
            {"id": 25, "name": "Daman and Diu", "abbreviation": "DD"},
            {"id": 26, "name": "Dadra and Nagar Haveli", "abbreviation": "DN"},
            {"id": 27, "name": "Maharashtra", "abbreviation": "MH"},
            {"id": 28, "name": "Karnataka", "abbreviation": "KA"},
            {"id": 29, "name": "Goa", "abbreviation": "GA"},
            {"id": 30, "name": "Lakshadweep", "abbreviation": "LD"},
            {"id": 31, "name": "Kerala", "abbreviation": "KL"},
            {"id": 32, "name": "Tamil Nadu", "abbreviation": "TN"},
            {"id": 33, "name": "Puducherry", "abbreviation": "PY"},
            {"id": 34, "name": "Andaman and Nicobar Islands", "abbreviation": "AN"},
            {"id": 35, "name": "Telangana", "abbreviation": "TS"},
            {"id": 36, "name": "Andhra Pradesh", "abbreviation": "AP"},
            {"id": 37, "name": "Ladakh", "abbreviation": "LA"}
        ]
        for item in data:
            state = IndianState(id=item['id'], name=item['name'], abbreviation=item['abbreviation'])
            db.session.add(state)
        db.session.commit()
