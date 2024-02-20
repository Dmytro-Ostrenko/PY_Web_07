from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///database_HW7.db")
Session = sessionmaker(bind=engine)
session = Session()