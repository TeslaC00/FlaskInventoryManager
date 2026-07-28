import os
import subprocess
import gzip
from flask import Blueprint, jsonify, request, current_app
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename
from itsdangerous import URLSafeSerializer

# Create Blueprint for the Backup and Recovery module
backup_bp = Blueprint('backup', __name__)

# Define a backup directory
BACKUP_DIR = "database_backups"
os.makedirs(BACKUP_DIR, exist_ok=True)

# Create a secret key-based serializer for secure file naming
serializer = URLSafeSerializer(current_app.config.get('SECRET_KEY', 'default-secret-key'))

def parse_mysql_uri(database_uri):
    """
    Parse MySQL Database URI into components.
    Example DB URI: mysql+pymysql://username:password@host/database
    """
    from urllib.parse import urlparse

    # Remove scheme and parse MySQL URI
    uri = urlparse(database_uri.replace("mysql+pymysql://", ""))

    return {
        "host": uri.hostname,
        "user": uri.username,
        "password": uri.password,
        "database": uri.path.lstrip("/")
    }

@backup_bp.route('/backup', methods=['GET'])
def backup_database():
    """
    Endpoint to create a backup of the database with compression.
    """
    try:
        # Fetch database URL from Flask config
        db_uri = current_app.config['SQLALCHEMY_DATABASE_URI']
        backup_file = os.path.join(BACKUP_DIR, 'backup.sql')
        compressed_backup_file = f"{backup_file}.gz"

        # Logic for SQLite Backup
        if "sqlite" in db_uri:
            from sqlite3 import connect

            conn = connect(db_uri.replace("sqlite:///", ""))
            backup_conn = connect(backup_file)
            with backup_conn:
                conn.backup(backup_conn)
            backup_conn.close()
            conn.close()

        # Logic for MySQL Backup
        elif "mysql" in db_uri:
            db_config = parse_mysql_uri(db_uri)
            with open(backup_file, "w") as outfile:
                subprocess.run(
                    [
                        "mysqldump",
                        "-h", db_config["host"],
                        "-u", db_config["user"],
                        f"-p{db_config['password']}",
                        db_config["database"]
                    ],
                    stdout=outfile,
                    check=True
                )
        else:
            return jsonify({"error": "Unsupported database type."}), 501

        # Compress the backup file
        with open(backup_file, 'rb') as f_in, gzip.open(compressed_backup_file, 'wb') as f_out:
            f_out.writelines(f_in)
        os.remove(backup_file)  # Remove uncompressed file

        # Secure the filename for download
        secure_filename = serializer.dumps(os.path.basename(compressed_backup_file))

        return jsonify({"message": "Backup created successfully.", "backup_file": secure_filename})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Database backup failed.", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@backup_bp.route('/restore', methods=['POST'])
def restore_database():
    """
    Endpoint to restore the database from a compressed backup file.
    """
    try:
        # Check if backup file is provided
        if 'backup_file' not in request.files:
            return jsonify({"error": "No backup file provided."}), 400

        file = request.files['backup_file']

        # Save the uploaded backup file temporarily
        filename = secure_filename(file.filename)
        compressed_backup_path = os.path.join(BACKUP_DIR, filename)
        file.save(compressed_backup_path)

        # Decompress the backup file
        backup_path = compressed_backup_path.rstrip('.gz')
        with gzip.open(compressed_backup_path, 'rb') as f_in, open(backup_path, 'wb') as f_out:
            f_out.writelines(f_in)
        os.remove(compressed_backup_path)  # Remove compressed file

        # Fetch database URI from Flask config
        db_uri = current_app.config['SQLALCHEMY_DATABASE_URI']

        # Logic for SQLite Restore
        if "sqlite" in db_uri:
            from sqlite3 import connect

            conn = connect(db_uri.replace("sqlite:///", ""))
            backup_conn = connect(backup_path)
            with conn:
                backup_conn.backup(conn)
            backup_conn.close()
            conn.close()

        # Logic for MySQL Restore
        elif "mysql" in db_uri:
            db_config = parse_mysql_uri(db_uri)
            with open(backup_path, "r") as infile:
                subprocess.run(
                    [
                        "mysql",
                        "-h", db_config["host"],
                        "-u", db_config["user"],
                        f"-p{db_config['password']}",
                        db_config["database"]
                    ],
                    stdin=infile,
                    check=True
                )
        else:
            return jsonify({"error": "Unsupported database type."}), 501

        os.remove(backup_path)  # Clean up decompressed file

        return jsonify({"message": "Database restored successfully."})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Database restore failed.", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
