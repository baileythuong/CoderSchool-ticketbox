import os
from dotenv import load_dotenv
load_dotenv()

class Config(object):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL')
    SECRET_KEY='this is a super duper secret key'
    FLASK_ADMIN_SWATCH = 'cerulean'
    EMAIL_API_KEY="aa5945215cd9444b1c0fad8ce0a169fd-09001d55-7c06bbfb"