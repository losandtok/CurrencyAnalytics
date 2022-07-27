from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URI = 'postgres://yxjakgazhvvxvb:aac65fdcf984547be34bcb4df35456b752b01fc050fb2cf9a4bbd6178bcf4171@ec2-176-34-215-248.eu-west-1.compute.amazonaws.com:5432/dbadgq9revtsgg'

engine = create_engine(
    SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
