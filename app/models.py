from sqlalchemy import Boolean, Column, Integer, String
from .database import Base


class Post(Base):
    #what do we wanna call this table in postgres? We have a class name called Post that only python knows but we can specify a specific name in postgres
    __tablename__ = "posts"
    #to create a column we have to import Column from SQLAlchemy
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True)


#Now we will create the models in our mainfile
