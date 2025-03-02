from sqlalchemy.engine import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..database import Base
from ..app import app
from ..routers.todos import get_db, get_current_user
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from ..models import Todos


SQLALCHEMY_DATABASE_URI = 'sqlite:///./test.db'
engine = create_engine(SQLALCHEMY_DATABASE_URI,
                       poolclass=StaticPool,
                       connect_args={"check_same_thread": False})

TestLocalSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base.metadata.create_all(engine)


def override_get_db():
    db = TestLocalSession()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {'username': 'pramodyasahan', 'id': 1, 'user_role': 'admin'}


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user
client = TestClient(app)


@pytest.fixture
def test_todo():
    todo = Todos(
        title='Test title',
        description='Test description',
        priority=4,
        complete=False,
        owner_id=1
    )

    db = TestLocalSession()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as conn:
        conn.execute()



def test_read_all_authenticated():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []