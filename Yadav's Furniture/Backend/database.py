from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("postgresql://postgres:Happy%404401@localhost/Furniture_Database")

Base = declarative_base()

SessionLocal=sessionmaker(bind = engine)
