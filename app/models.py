from sqlmodel import Field, SQLModel
from pydantic import BaseModel


class WalletBase(SQLModel):
    currency_code: str = Field(index=True)
    amount: float | None = Field(default=0, index=False)


class Wallet(WalletBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class WalletCreate(WalletBase):
    pass


class WalletPublic(WalletBase):
    id: int


class WalletRead(WalletBase):
    converted_currency_code: str
    converted_amount: float


class WalletResponse(SQLModel):
    wallets: list[WalletRead]
    total_converted_amount: float


class Token(BaseModel):
    access_token: str
    token_type: str


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    full_name: str
    role: str
    hashed_password: str
