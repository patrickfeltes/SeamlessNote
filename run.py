from app import app

# register authentication endpoints
from auth import authentication
app.register_blueprint(authentication)

# register file endpoints
from files import file_routes
app.register_blueprint(file_routes)

# will run twice if debug is set to True
if __name__ == '__main__':
    app.run(debug = False)