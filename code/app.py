from flask import Flask, render_template
from application.database import db
import os

cwd=os.getcwd()
db_path=os.path.join(cwd, "instance","database.sqlite3")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///"+db_path
db.init_app(app)

app.app_context().push()
import application.config as config
from application.controller.admin import *
from application.controller.user import *
import application.models as models
with app.app_context():
    db.create_all()

from application.api import *

if __name__=='__main__':
    app.run(debug=True)