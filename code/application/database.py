from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

engine=None
engine = None
Base = declarative_base()

db =SQLAlchemy()