from decimal import Decimal
from pydantic import BaseModel, Field, field_validator


class OperationRequest(BaseModel):
    wallet_name: str = Field(..., max_length=127)
    amount: Decimal
    descriptions: str | None = Field(None, max_length=255)


    @field_validator('amount')
    def amount_must_be_positive(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError('Amount must be positive')
        return v
    
    @field_validator('wallet_name')
    def wallet_name_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError('Wallet name not be empty')
        return v
    

class CreateWalletRequest(BaseModel):
    name: str = Field(..., max_length=127)
    initial_balance: Decimal = 0

    @field_validator('name')
    def wallet_name_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError('Wallet name not be empty')
        return v
    
    @field_validator('initial_balance')
    def amount_not_be_negative(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError('Initial balance can not negative')
        return v

