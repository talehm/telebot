from sqlalchemy.orm import sessionmaker, Session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta, datetime
from flask import current_app

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
        # self.session.rollback()
        session = db.session
        try:
            return session.query(model).filter_by(**kwargs).first()
        except Exception as e:
            print(f"Errors: {e}")
            return None

    def get_many(self, model, older_than=None, **kwargs):
        try:
            status = kwargs.get("status")  # Extract the statuses from kwargs
            query = self.session.query(model)
            if isinstance(status, list):
                kwargs.pop("status", None)
                query = query.filter(model.status.in_(status))

            query = query.filter_by(**kwargs)

            if older_than is not None:
                interval = datetime.utcnow() - older_than
                query = query.filter(model.created_at <= interval)
            return query.all()
        except Exception as e:
            print(f"Error: {e}")
            return None

    def update(self, model_instance, **kwargs):
        """Updates an existing record"""
        for key, value in kwargs.items():
            setattr(model_instance, key, value)
        # if kwargs.items() == 0:
        #     self.session.add(model_instance)
        self.session.commit()
        self.session.refresh(model_instance)
        # self.session.close()
        return model_instance

    def delete(self, model_instance):
        """Deletes a record from the database"""
        self.session.delete(model_instance)
        self.session.commit()
        # self.session.close()
