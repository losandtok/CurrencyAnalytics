from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



SQLALCHEMY_DATABASE_URL  = 'postgresql+psycopg2://yafcbxezfzlemw:872753ef79dce9b5268371000800cc6a12605c23349dd6c3153d088310f65df1@ec2-34-252-216-149.eu-west-1.compute.amazonaws.com:5432/d7ngenunpf9h3k'
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

