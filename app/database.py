from app.extensions import db
from app.logger import logger
from sqlalchemy import inspect
from app.seed import seed


def tables_changed():
    inspector = inspect(db.engine)
    existing_tables = inspector.get_table_names()
    all_tables = db.metadata.tables.keys()

    new_tables = set(all_tables) - set(existing_tables)
    return new_tables


def fill_tables():
    try:
        seed(db)
        db.session.commit()
        logger.info("Filled tables with seed data")
    except Exception as e:
        db.session.rollback()
        logger.error("Error while filling tables with seed", e)


def check_and_create_and_fill_tables(app):
    with app.app_context():
        if tables_changed():
            try:
                logger.info("Detected changes in tables")
                db.drop_all()
                logger.debug("Dropped all tables")
                db.create_all()
                logger.debug("Recreated all tables")
                fill_tables()
            except Exception as e:
                db.session.rollback()
                logger.error("Error while creating tables", e)
