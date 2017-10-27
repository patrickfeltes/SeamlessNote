# Seamless Note

## Installation Instructions
- Install [MySQL Community Server](https://dev.mysql.com/downloads/mysql/).
- Install [MySQL Workbench](https://dev.mysql.com/downloads/workbench/).
- Follow MySQL Set Up Instructions.
- Install [Git](https://git-scm.com/) and set it up. Instructions are [here](https://help.github.com/articles/set-up-git/).
- Install [Python](https://www.python.org/) >= 2.7 and make sure you have pip installed.
- Install all Python modules (see Python Modules).
- Clone this repository, run `git clone https://github.com/CS196Illinois/SeamlessNote.git`
- Create a file in the repository called secrets.py and give it the following format.
```python
DB_USERNAME = ''
DB_PASSWORD = ''
DB_NAME = ''
```
- Fill in the above values with what you specified when you created your connection/schema in MySQL workbench.

## MySQL Set Up
- Once you have MySQL Community Server and Workbench installed, open Workbench.
- Go to MySQL connections and create a new connection.
- Once in the connection create a new schema using the schemas tab on the left.
- Refresh your schemas and double click on your new schema to set it as default.
- In the Query tab, do the following in order to set up the database table structure. Pressing the lightning bolt will execute the query.
- Create the users database.
```SQL
CREATE TABLE users (
user_id INTEGER PRIMARY KEY AUTO_INCREMENT,
username varchar(100),
hashed_password varchar(100)
);
```
- Insert a sample user into the table.
```SQL
INSERT INTO users VALUES (DEFAULT, "username", "password");
```
- Create the notes table.
```SQL
CREATE TABLE notes (
file_id INTEGER PRIMARY KEY AUTO_INCREMENT,
file_name varchar(100),
file_contents varchar(20000),
user_id INTEGER
);
```

## Python Modules
- Flask `pip install Flask`
- Flask-SQLAlchemy `pip install Flask-SQLAlchemy`
- MySQL-python `pip install MySQL-python`

## Running
- Make sure that your MySQL local server is running (using System Preferences or Workbench).
- Navigate to the seamlessnote repository folder on your computer.
- Run `python app.py`.
- Open your favorite browser and go to localhost:5000.
