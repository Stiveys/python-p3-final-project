from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create a SQLite database engine
# This will store all our recipe data in a local file called culinary_compass.db
engine = create_engine('sqlite:///culinary_compass.db')

# Create a session factory bound to our engine
# Sessions are used to interact with the database
Session = sessionmaker(bind=engine)

# Create a base class for our models
# All our model classes will inherit from this base
Base = declarative_base()