from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, text
from .database import Base


class Post(Base):
    #what do we wanna call this table in postgres? We have a class name called Post that only python knows but we can specify a specific name in postgres
    __tablename__ = "posts"
    #to create a column we have to import Column from SQLAlchemy
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


 