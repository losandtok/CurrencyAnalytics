from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



SQLALCHEMY_DATABASE_URL  = 'postgresql+psycopg2://gxzwnrrlprhgrm:d988195cb445d139128ad103b1722ab0bae6e082cc2fc2986f546523495b771c@ec2-54-76-43-89.eu-west-1.compute.amazonaws.com:5432/dfa8h8agc5p6gi'
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

