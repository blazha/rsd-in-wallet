from fastapi import FastAPI, Depends, Query
from typing import Annotated, Sequence
from sqlmodel import Session, select

from .database import get_session, create_db_and_tables
from .models import Wallet, WalletCreate, WalletPublic

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/health")
def read_root():
    return {"status": "ok"}


@app.post("/wallet/add", response_model=WalletPublic)
def add_wallet(wallet: WalletCreate, session: SessionDep):
    db_wallet = Wallet.model_validate(wallet)

    session.add(db_wallet)
    session.commit()
    session.refresh(db_wallet)

    return db_wallet


# TODO: add conversion currency code in query params e.g. ?conversion_currency_code=RSD
# read and cache conversion once per day
@app.get("/wallet/", response_model=list[WalletPublic])
def read_wallet(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    wallet = session.exec(select(Wallet).offset(offset).limit(limit)).all()

    return wallet
