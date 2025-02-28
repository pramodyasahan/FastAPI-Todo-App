from database import Base
from sqlalchemy import Column, String, Integer, Boolean


class Todos(Base):  # Inherit from 'base' to define a table
    __tablename__ = "todos"  # Table name in the database

    # This creates a table with columns id, title, description, priority, and complete in the database
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
