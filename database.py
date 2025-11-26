from sqlalchemy import Column,Integer,ForeignKey,DECIMAL,String,create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'sqlite:///.base.db'
engine = create_engine(DATABASE_URL)
Session_local = sessionmaker(autoflush=True,autocommit=False,bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,index=True,nullable=False)
    email = Column(String,unique=True,index=True,nullable=False)
    age = Column(Integer,nullable=False)

class Class(Base):
    __tablename__ = 'classes'
    id = Column(Integer,primary_key=True,index=True)
    teacher = Column(String,nullable=False,index=True)

Base.metadata.create_all(bind=engine)
