from fastapi import FastAPI

from .database import SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def read_root():
    return {"status": "ok"}
