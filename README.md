# Seamless Note

## Getting Started

###
- [Git](https://git-scm.com/)
- [Python](https://www.python.org/) >= 2.7
- [MySQL Community Server](https://dev.mysql.com/downloads/mysql/)
- [MySQL Workbench](https://dev.mysql.com/downloads/workbench/)
- [Flask](http://flask.pocoo.org/)(`pip install Flask`)

## Installation Instructions
- Install MySQL.
- Install Git and set it up. Instructions are [here](https://help.github.com/articles/set-up-git/).
- Install Python and make sure you have pip installed.
- Install flask, run `pip install Flask`
- Clone this repository, run `git clone https://github.com/pj6444/seamlessnote.git`
- Create a file in the seamless note repo called secrets.py and give it the following format. Be sure to replace the empty strings with the correct values for your system
```python
DB_USERNAME = ''
DB_PASSWORD = ''
DB_NAME = ''
```


## Running
- Navigate to the seamlessnote repository folder on your computer
- Run `python app.py`
- Open your favorite browser and go to localhost:5000.
