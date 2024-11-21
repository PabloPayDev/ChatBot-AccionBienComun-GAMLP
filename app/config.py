from dotenv import load_dotenv
import os

load_dotenv(override=True)

def init_app_config(app):
    app.config['IMAGE_DIR_PATH'] = os.getenv('IMAGE_DIR_PATH')

    app.config['META_TOKEN'] = os.getenv('META_TOKEN')
    app.config['WEBHOOK_TOKEN'] = os.getenv('WEBHOOK_TOKEN')
    
    app.config['META_DOMAIN'] = os.getenv('META_DOMAIN')
    app.config['META_VERSION'] = os.getenv('META_VERSION')
    app.config['META_USER_ID'] = os.getenv('META_USER_ID')
    app.config['META_MESSAGES_PATH'] = f"/{app.config['META_VERSION']}/{app.config['META_USER_ID']}/messages"
    
    app.config['BLOG_DOMAIN'] = os.getenv('BLOG_DOMAIN')
    app.config['BLOG_PATH'] = os.getenv('BLOG_PATH')

    app.config['GAMLP_DOMAIN'] = os.getenv('GAMLP_DOMAIN')
    app.config['GAMLP_PORT'] = os.getenv('GAMLP_PORT')
    app.config['GAMLP_PATH_GET_TOKEN'] = os.getenv('GAMLP_PATH_GET_TOKEN')
    app.config['GAMLP_PATH_GET_CIUDADANO'] = os.getenv('GAMLP_PATH_GET_CIUDADANO')
    app.config['GAMLP_PATH_CREATE_CIUDADANO'] = os.getenv('GAMLP_PATH_CREATE_CIUDADANO')
    app.config['GAMLP_USER'] = os.getenv('GAMLP_USER')
    app.config['GAMLP_PASS'] = os.getenv('GAMLP_PASS')

    app.config['SESSIONS_STORE'] = {}


