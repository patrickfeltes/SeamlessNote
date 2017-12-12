# Seamless Note
## Overview
Seamless Note is a note taking website with a tag-based organizational system. Our system seamlessly recommends tags for your notes based on their contents.

## Team Members
- Manuel A Hernandez-Estrada Jr(manuelh3)
- Rahul Miriyala(rmiriya2)
- Abhay Varmaraja(abhaymv2)
- Patrick Feltes(pfeltes2)
- PM: Aria Malkani

## Installation Instructions
- Install [Git](https://git-scm.com/) and set it up. Instructions are [here](https://help.github.com/articles/set-up-git/).
- Install [Python](https://www.python.org/) >= 2.7 and make sure you have pip installed.
- Clone this repository, run `git clone https://github.com/CS196Illinois/SeamlessNote.git`
- Install all Python modules: run `pip2 install -r requirements.txt` when in the SeamlessNote directory.
- Install [MySQL Community Server](https://dev.mysql.com/downloads/mysql/).
- Install [MySQL Workbench](https://dev.mysql.com/downloads/workbench/).
- Follow MySQL set up instructions (see below).
- Create a file in the repository called secrets.py and give it the following format.
```python
DB_USERNAME = ''
DB_PASSWORD = ''
DB_NAME = ''
```
- Fill in the above values with what you specified when you created your connection/schema in MySQL workbench.
- Navigate to the Seamless Note folder and open the python shell by typing `python` or `python2` in terminal/command prompt.
- To create all of the database tables, run the following commands.
```python
>>> import database
>>> from app import db
>>> db.create_all()
```
- Follow the running instructions to run the Flask app. On your first run, make sure you go to https://localhost:5000/register and create a username and password so you can login when necessary.

## MySQL Set Up
- Once you have MySQL Community Server and Workbench installed, open Workbench.
- Go to MySQL connections and create a new connection.
- Once in the connection create a new schema using the schemas tab on the left.
- Refresh your schemas and double click on your new schema to set it as default.

## Running
- Make sure that your MySQL local server is running (using System Preferences or Workbench).
- Navigate to the seamlessnote repository folder on your computer.
- Run `python run.py`.
- Open your favorite browser and go to localhost:5000.
