from flask_sqlalchemy import SQLAlchemy

# Creates SQLAlchemy Object
db = SQLAlchemy()
# TODO: create bomb table to store goods(parent) to material(child)
# TODO: change string -> text in audit_log
# TODO: add remarks to -> challan, bill, returned_good, records, audit_log
# TODO: add hidden folder to store images and files that are sent to app, add delimiter to save file path in remarks
# TODO: decide cascading on update
