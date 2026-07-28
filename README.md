## Flask Inventory Manager

A flask based inventory manager project made by me and my friends >-<. You can check out the images or read the configuration setup used by my us to keep each other in sync with backend.

### Images
| | |
|---|---|
| ![Login Page](images/login.png) | ![Inventory Goods Page](images/invGoods.png) 
| ![Challan Page](images/challan.png) | ![Challan Info](images/challanInfo.png) 
| ![New Sales Form](images/sale.png) | ![Product Table Page](images/product.png) 

## Local Database Setup

###### Create Database in MySQL

Create a database in mysql. You already know how but still here's the
code

MySQL command line:

```mysql
CREATE DATABASE database_name;
```

---

###### Create Database URI

Use the database information like the username, password, host_name to
create a database_uri. It is a path for your local database.

```text
mysql://username:password@host/database_name
```

host
: It is generally localhost untill you make it something else

database_name
: When using testing database use <font color="yellow">mock</font> as the name
(Recommended)

---

###### Create config.py

Create a config.py file in the app package. The file would look like
this:

```python
SQLALCHEMY_DATABASE_URI = 'your_database_uri'
SQLALCHEMY_TRACK_MODIFICATIONS = True
```

<font color="green">*Note: config.py is not tracked in git to avoid conflict with local
username, password and database name*</font>

For using the free online database the URI is given below. Please test the
connection first using the <font color="lighblue">test_database_connection</font> path in route.

<font color="green">*Note: the database URI may change in future depending*</font>

```python
SQLALCHEMY_DATABASE_URI = 'mysql://sql6687728:iCUBYbhW74@sql6.freemysqlhosting.net:3306/sql6687728'
```

---

###### Create database.py

Create the database.py file in app package that will have the
SQLAlchemy object. It look like this:

```python
from flask_sqlalchemy import SQLAlchemy

# Creates SQLAlchemy Object
db = SQLAlchemy()
```

---

###### Modify init.py

Add the following import to your init.py.

```python
from .database import db
```

Add the following code to your create_app in init.py.

```python
def create_app():
    # Load local configurations from config.py
    app.config.from_pyfile()

    # Initialize database
    db.init_app(app)
```

---

###### Test Database Connection

Add the following code to your routes.py to test if database connected
or not. If the output is <font color="lighblue">Database connected successfully!</font> then it
is working else get it fixed.

```python
from .database import db


@main_routes.route('/test_database_connection')
def test_database_connection():
    try:
        # Execute a simple query to test the connection
        db.session.execute(text('SELECT 1'))
        return 'Database connected successfully!'
    except Exception as e:
        return f'Database connection error: {str(e)}'
```

## Database Tool Migration

###### Install Flask-Migrate

`pip install flask-migrate`

---

###### Modify init.py

Modify the init.py file to use flask-migrate in terminal. Add the
following import.

```python
from flask_migrate import Migrate
```

Add the following code in create_app in init.py.

```python
# Initialize database migration tool
migrate = Migrate(app, db)
```

---

###### Add migration directory

`flask db init`

This command initialises the migration directory automatically in the
project folder

---

###### Add revision

When you do any change to the database add a revision. Revision keep
database version history and help in getting older version and get
latest version.

<font color="green">*Note: before making any changes to database keep your version update*</font>

`flask db revision -m "revision_name"`

revision_name
: Typically what you added or modified in database to
help in keeping track of

---

###### Migrate database

After revision migrate the database

`flask db migrate -m "migration_name"`

migration_name
: Whatever changes you made to the database

---

###### Update Database

After migrating always update the database. Update the database
whenever new change is made to the versions in migration directory.

`flask db upgrade`

###### Add Dummy Data to Database

Run the `seed.py` file to add dummy data to the database automatically

## Git Branch Rules

###### Branch Naming Convention

When creating a new feature or working on a bug fix create new branch
under a category that is appropriate for the branch. Use the naming
convention below when creating new branch.

<font color="green">*Note: use dash (-) rather space in branch or category name*</font>

`category-name/branch-name`

###### Git Commands

Create new branch from terminal

`git checkout -b <category-name>/<branch-name>`

Push the new branch on GitHub

`git push -u origin <category-name>/<branch-name>`

# Flask Test

###### Setup Test Database

To do testing for this app we need `config_test.py` file which should contain the configurations for testing database.
Create a new ***test*** database for testing purpose.
In the `config_test.py` add the configurations

```python
SQLALCHEMY_DATABASE_URI = 'test_database_uri'
SQLALCHEMY_TRACK_MODIFICATIONS = False
```

<font color="green">*Tip: create database with name *test*, and copy the main config Database URI
and replace database name with *test* '*</font>

###### Run Tests

We need `pytest` package for testing app. Pytest will create the database automatically and delete it after tests.
To run test just type `pytest` in the terminal and run. Pytest will run the created tests automatically.
