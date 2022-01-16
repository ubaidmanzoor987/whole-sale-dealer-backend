from flask import Flask
from src.database.db import Session
from src.api import user_api, brands_api, products_api, orders_api
from dotenv import dotenv_values
config = dotenv_values(".env")

app = Flask(__name__, instance_relative_config=True, static_folder="static", template_folder="static")

app.config['SECRET_KEY'] = config['SECRET_KEY']
app.register_blueprint(user_api.user_bp)
app.register_blueprint(brands_api.brands_bp)
app.register_blueprint(products_api.products_pp)
app.register_blueprint(orders_api.orders_pp)

if __name__ == "__main__":
    Session.session.init_db()
    app.run(host='0.0.0.0', debug = True, port=5000)

