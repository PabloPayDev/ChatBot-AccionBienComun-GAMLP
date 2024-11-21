from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from pymongo import MongoClient
import logging
import os

from .routes import routes_bp
from .helpers import cleanup_expired_sessions
from .config import init_app_config

def create_app():
    app = Flask(__name__)

    # ======= ====== ======= HOST/DB ENV VARS SECTION ======= ======= =======
    serverHost = os.getenv('SERVER_HOST')
    serverPort = os.getenv('SERVER_PORT')

    mongoDBDomain = os.getenv('MONGODB_DOMAIN')
    mongoDBPath = os.getenv('MONGODB_PATH')
    # ======= ====== ======= ======= ======= ======= =======
    # ======= ====== ======= DB INIT SECTION ======= ======= =======
    client = MongoClient(mongoDBDomain)
    db = client[mongoDBPath]
    # ======= ====== ======= ======= ======= ======= =======
    # ======= ====== ======= BG TASKS INIT SECTION ======= ======= =======
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=cleanup_expired_sessions, trigger="interval", minutes=1)
    scheduler.start()
    # ======= ====== ======= ======= ======= ======= =======
    # ======= ====== ======= LOGGING CONFIG SECTION ======= ======= =======
    logging.basicConfig(level=logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)
    logging.getLogger("pymongo").setLevel(logging.WARNING)
    # ======= ====== ======= ======= ======= ======= =======
    # ======= ====== ======= APP CONFIG SECTION ======= ======= =======
    app.config['SERVER_HOST'] = serverHost
    app.config['SERVER_PORT'] = serverPort

    app.config['MONGO_DB'] = db

    init_app_config(app)
    app.register_blueprint(routes_bp, url_prefix='/api')
    # ======= ====== ======= ======= ======= =======

    return app
