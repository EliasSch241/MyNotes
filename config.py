import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'yolo'
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://dbadmin:Pa55wort@dbflaskesc.mysql.database.azure.com:3306/notes'
#   SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
#       'mysql+pymysql://dbadmin:Pa55wort@dbflaskesc.mysql.database.azure.com:3306/notes'
    SQLALCHEMY_TRACK_MODIFICATIONS = False