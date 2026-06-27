import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import Base, engine, SessionLocal
from app.core.elastic import es
from app.core.elastic import create_index_if_not_exists

@pytest.fixture(scope="session")
def client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def clean_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    if es.indices.exists(index="documents"):
        es.indices.delete(index="documents")
    create_index_if_not_exists()
    yield