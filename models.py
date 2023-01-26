import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from flask_migrate import Migrate

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    # db.create_all() # auto updates database schema with changes described by models
    # NOTE: db.create_all() is an alternative approach to flask_migrate strategy
    # do not run flask_migrate with db.create_all()

"""
Actor

"""
class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    dob = Column(Date, nullable=False)

    def __init__(self, name, gender, dob):
        self.name = name
        self.gender = gender
        self.dob = dob

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'dob': self.dob
        }

"""
Movie

"""
class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(Date, nullable=False)
    cast = relationship('Actor', secondary="casts",
                           backref=db.backref('movies', lazy=True))

    def __init__(self, title, release_date, cast):
        self.title = title
        self.release_date = release_date
        self.cast = cast

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'cast': [actor.format() for actor in self.cast]
        }

"""
Cast

"""
class Cast(db.Model):
    __tablename__ = 'casts'

    movie_id = Column(Integer, ForeignKey('movies.id'), primary_key=True)
    actor_id = Column(Integer, ForeignKey('actors.id'), primary_key=True)
