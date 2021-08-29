from datetime import timedelta

from flask import Flask, session
settings = 'U0cuNk9QMVk3RE1SdWljbGhhcTRKeFRHQS5WeTg2ZjRXRkJVa28xRzVGT2lwLVkzSjNnMnV1LUdNZWVPT2xZSzY4S1JF'
from src.database.db import init_db
from src.api import shopkeepers_api

app = Flask(__name__, instance_relative_config=True,static_folder="static/dist",template_folder="static")
app.config.from_mapping(
    SECRET_KEY = 'DEV')

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=10)

app.register_blueprint(shopkeepers_api.shopkeeper_bp)

if __name__ == "__main__":
    init_db()
    app.run("192.168.1.15", debug = True)

