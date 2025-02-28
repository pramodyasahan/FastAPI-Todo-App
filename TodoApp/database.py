from sqlalchemy import create_engine  # Import the create_engine function from SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Define the database URL
# 'sqlite:///' -> This specifies that we are using SQLite as the database
# './todos.db' -> This means the database file named 'todos.db' will be created in the current directory
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db'

# Create a database engine that allows our Python program to connect and interact with the database
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,  # Use the database URL we defined above
    connect_args={'check_same_thread': False}  # This allows multiple parts of the program to access the database
)

# Create a session factory for database interactions
# - autocommit=False -> Changes must be manually committed
# - autoflush=False -> Prevents automatic sending of changes before execution
# - bind=engine -> Links the session to the database engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for defining database models (tables)
Base = declarative_base()
