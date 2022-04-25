"""
@Author Marco A. Gallegos
@Date   2020/10/09
@Update 2020/10/09
@Description
    Main Api file
"""
from config.config import APP_CONFIG
from flask import Flask
from flask_cors import CORS
from config.routes import setup_routes
from flask_jwt_extended import (JWTManager)


app = Flask(APP_CONFIG['APP_NAME'])
CORS(app, resources={r"/*": {"origins": "*"}})

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = APP_CONFIG["APP_KEY"]
jwt = JWTManager(app)

# set up default routes
setup_routes(app, APP_CONFIG)


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5001 # diferent port than users
    app.run(debug=True, host=host, port=port)
