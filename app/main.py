from fastapi import FastAPI, Depends, Query, HTTPException
from typing import Annotated
from sqlmodel import Session, select

from .currency_converter import get_cached_calculation, get_cache_key
from .database import get_session, create_db_and_tables
from .models import Wallet, WalletCreate, WalletPublic, WalletRead, WalletResponse

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

SUPPORTED_CURRENCIES = ["RSD"]


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/health")
def read_root():
    return {"status": "ok"}


@app.post("/wallet/add", response_model=WalletPublic)
def add_wallet(wallet: WalletCreate, session: SessionDep):
    db_wallet = session.exec(select(Wallet).where(Wallet.currency_code == wallet.currency_code)).first()

    if db_wallet:
        db_wallet.amount += wallet.amount
    else:
        db_wallet = Wallet.model_validate(wallet)

    session.add(db_wallet)
    session.commit()
    session.refresh(db_wallet)

    return db_wallet


@app.post("/wallet/remove", response_model=WalletPublic)
def add_wallet(wallet: WalletCreate, session: SessionDep):
    db_wallet = session.exec(select(Wallet).where(Wallet.currency_code == wallet.currency_code)).first()

    if db_wallet:
        db_wallet.amount -= wallet.amount
        if db_wallet.amount < 0:
            raise HTTPException(status_code=400,
                                detail="Cannot remove from your wallet more than you have!")
    else:
        raise HTTPException(status_code=400, detail=f"Currency code '{wallet.currency_code}' not exists, add it first")

    session.add(db_wallet)
    session.commit()
    session.refresh(db_wallet)

    return db_wallet


@app.get("/wallet/", response_model=WalletResponse)
def read_wallet(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
    conversion_currency_code: str = "RSD",
):
    if conversion_currency_code not in SUPPORTED_CURRENCIES:
        raise HTTPException(status_code=400, detail=f"Currency code '{conversion_currency_code}' not supported")

    db_wallets = session.exec(select(Wallet).offset(offset).limit(limit)).all()

    conversion_rate = get_cached_calculation(get_cache_key())

    wallets = [
        WalletRead(
            **wallet.dict(),
            converted_currency_code=conversion_currency_code,
            converted_amount=wallet.amount * conversion_rate if wallet.amount else 0
        )
        for wallet in db_wallets
    ]

    total_converted_amount = sum(wallet.converted_amount for wallet in wallets)

    return WalletResponse(wallets=wallets, total_converted_amount=total_converted_amount)
