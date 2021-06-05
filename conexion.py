import os
import flask
from flask.app import Flask
from flaskext.mysql import MySQL

class conexion():
    app= Flask(__name__)
    app.secret_key="develoteca"

    mysql = MySQL()
    app.config['MYSQL_DATABASE_HOST']='localhost'
    app.config['MYSQL_DATABASE_USER']='root'
    app.config['MYSQL_DATABASE_PASSWORD']=''
    app.config['MYSQL_DATABASE_DB']='sistema'
    mysql.init_app(app)

    carpeta=os.path.join('uploads')
    app.config['carpeta'] = carpeta

   



