from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from api.control.settings.settings import Settings

engine = create_engine(Settings().DATABASE_URL)

# Fecha a session corretamente
def get_session():  # pragma: no cover
    with Session(engine) as session:
        yield session
