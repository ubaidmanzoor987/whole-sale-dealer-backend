from flask import Flask
from src.database.db import Session
from src.api import shopkeepers_api
from dotenv import dotenv_values
config = dotenv_values(".env")

app = Flask(__name__, instance_relative_config=True,static_folder="static/dist",template_folder="static")

app.config['SECRET_KEY'] = config['SECRET_KEY']
app.register_blueprint(shopkeepers_api.shopkeeper_bp)


if __name__ == "__main__":
    Session.session.init_db()
    app.run(host='0.0.0.0', debug = True, port=5000)

