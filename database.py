from sqlalchemy import Column,Integer,ForeignKey,Boolean,String,create_engine,CheckConstraint
from sqlalchemy.orm import sessionmaker,DeclarativeBase

DATABASE_URL = 'sqlite:///.base.db'
engine = create_engine(DATABASE_URL)
Session_local = sessionmaker(autoflush=True,autocommit=False,bind=engine)

class Base(DeclarativeBase):
    pass

class Soldier(Base):
    __tablename__ = "soldiers"
    id = Column(Integer,primary_key=True)
    privet_number = Column(Integer,index=True)
    first_name = Column(String,index=True,nullable=False)
    last_name = Column(String,index=True,nullable=False)
    gender = Column(String,nullable=False,index=True)
    city = Column(String,nullable=False,index=True)
    distance = Column(Integer,nullable=False,index=True)
    is_assign = Column(Boolean,nullable=True,index=True)

class Dorm(Base):
    __tablename__ = 'dorm-a'
    id = Column(Integer,primary_key=True,index=True)
    dormid = Column(Integer,nullable=False)
    soldier_1 = Column(Integer,nullable=False,index=True,unique=True)
    soldier_2 = Column(Integer,nullable=False,index=True,unique=True)
    soldier_3 = Column(Integer,nullable=False,index=True,unique=True)
    soldier_4 = Column(Integer,nullable=False,index=True,unique=True)
    soldier_5 = Column(Integer,nullable=False,index=True,unique=True)
    soldier_6 = Column(Integer,nullable=False,index=True,unique=True)
    soldier_7 = Column(Integer,nullable=False,index=True,unique=True)
    soldier_8 = Column(Integer,nullable=False,index=True,unique=True)


# Base.metadata.create_all(bind=engine)
