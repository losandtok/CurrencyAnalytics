from sqlalchemy.orm import Session
from sqlalchemy import desc
import hashlib

import os

from . import models

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, email, password):

    hashed_password = password
    db_user = models.User(email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Timeseries).offset(skip).limit(limit).all()


def get_last_timeseries(db: Session, user_id):
    return db.query(models.Timeseries.start_to_end_time).filter(models.Timeseries.owner_id == user_id).order_by(desc(models.Timeseries.query_date)).first()

def create_user_timeseries(db: Session, timeseries, user_id: int):
    db_timeseries = models.Timeseries(start_to_end_time=timeseries, owner_id=user_id)
    db.add(db_timeseries)
    db.commit()
    db.refresh(db_timeseries)
    return db_timeseries
