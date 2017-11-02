# Seamless Note

## Installation Instructions
- Install [MySQL Community Server](https://dev.mysql.com/downloads/mysql/).
- Install [MySQL Workbench](https://dev.mysql.com/downloads/workbench/).
- Follow MySQL Set Up Instructions.
- Install [Git](https://git-scm.com/) and set it up. Instructions are [here](https://help.github.com/articles/set-up-git/).
- Install [Python](https://www.python.org/) >= 2.7 and make sure you have pip installed.
- Install all Python modules (see Python Modules).
- Clone this repository, run `git clone https://github.com/CS196Illinois/SeamlessNote.git`
- Fill in the above values with what you specified when you created your connection/schema in MySQL workbench.

## MySQL Set Up
- Once you have MySQL Community Server and Workbench installed, open Workbench.
- Go to MySQL connections and create a new connection.
- Once in the connection create a new schema using the schemas tab on the left.
- Refresh your schemas and double click on your new schema to set it as default.
- Create and fill out secrets.py in the seamless note folder. It should have the following format
- Create a file in the repository called secrets.py and give it the following format. Fill out the fields with the values you used in Workbench.
```python
DB_USERNAME = ''
DB_PASSWORD = ''
DB_NAME = ''
```
- Go to your terminal and navigate to the Seamless Note folder.
- Enter the python shell by typing python2
- Enter the following commands in order
```python
from app import db
from app import User
db.create_all()
user = User('username', 'email@example.com', 'password')
db.session.add(user)
db.session.commit()
print User.query.all()
```
- Your output should look like [User: username]

## Python Modules
- Flask `pip install Flask`
- Flask-SQLAlchemy `pip install Flask-SQLAlchemy`
- MySQL-python `pip install MySQL-python`

## Running
- Make sure that your MySQL local server is running (using System Preferences or Workbench).
- Navigate to the seamlessnote repository folder on your computer.
- Run `python app.py`.
- Open your favorite browser and go to localhost:5000.
