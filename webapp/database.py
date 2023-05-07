from sqlalchemy.orm import sessionmaker, Session
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class DBHelper:
    def __init__(self):
        self.session = db.session

    def add(self, model_instance):
        """Adds a new record to the database"""
        self.session.add(model_instance)
        self.session.commit()
        self.session.refresh(model_instance)
        return model_instance

    def get_one(self, model, **kwargs):
        return self.session.query(model).filter_by(**kwargs).first()
    
    def get_many(self, model, **kwargs):
        return self.session.query(model).filter_by(**kwargs)
    
    def update(self, model_instance, **kwargs):
        """Updates an existing record"""
        for key, value in kwargs.items():
            setattr(model_instance, key, value)
        self.session.commit()
        self.session.refresh(model_instance)
        return model_instance

    def delete(self, model_instance):
        """Deletes a record from the database"""
        self.session.delete(model_instance)
        self.session.commit()
