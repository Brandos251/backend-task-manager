import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

load_dotenv()

database_url = (
    f'postgresql+psycopg://'
    f'{os.getenv('DB_USER')}:'
    f'{os.getenv('DB_PASSWORD')}@'
    f'{os.getenv('DB_HOST')}:'
    f'{os.getenv('DB_PORT')}/'
    f'{os.getenv('DB_NAME')}'
)

engine = create_engine(database_url)

def get_session():
    with Session(engine) as session:
        yield session

