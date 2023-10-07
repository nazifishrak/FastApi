# Import necessary modules from the SQLAlchemy library
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DATABASE URL format: 
# 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
# The following is an example URL for a local PostgreSQL server:
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password@localhost/postgres'

# The 'create_engine' function initializes a connection to the database.
# The engine serves as the source of connectivity to our database.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# To interact with the database, rather than using the engine directly,
# we use a 'Session'. The 'sessionmaker' function creates a factory for sessions.
# 'autocommit' being False means data won't be saved unless we explicitly call commit.
# 'autoflush' being False means SQLAlchemy won't automatically flush (i.e., write/sync) changes to the database unless explicitly asked.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# The 'declarative_base' function creates a base class for our models.
# This base class will contain metadata about our tables and columns and provide the ability to generate SQL queries.
# All the ORM classes/models we define will inherit from this base class, ensuring they are mapped to the right tables.
Base = declarative_base()
