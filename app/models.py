from sqlmodel import Field, SQLModel


class WalletBase(SQLModel):
    currency_code: str = Field(index=True)
    amount: int | None = Field(default=0, index=False)


class Wallet(WalletBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class WalletCreate(WalletBase):
    pass


class WalletPublic(WalletBase):
    id: int


class WalletRead(WalletBase):
    converted_currency_code: str
    amount: int

