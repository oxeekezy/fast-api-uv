from web.database import Base
from sqlalchemy import Column, Integer, String, DateTime


class Users(Base):
    __tablename__="users"
    
    id = Column(Integer, primary_key=True)
    
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    middlename = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    birthday = Column(DateTime, nullable=True)
    
    login = Column(String, nullable=False)
    email = Column(String, nullable=True)
    tel = Column(String, nullable=True)
    reg_date = Column(DateTime, nullable=True)
    
