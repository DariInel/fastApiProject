from typing import Optional, List

from pydantic import BaseModel, ConfigDict
from datetime import datetime


class PurchaseBase(BaseModel):
    sum: int


class PurchaseCreate(PurchaseBase):
    pass


class PurchaseUpdate(PurchaseBase):
    sum: Optional[int] = None


class Purchase(PurchaseBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    buyer_id: int
    created_at: datetime


class BuyerBase(BaseModel):
    name: str
    surname: str
    number: str


class BuyerCreate(BuyerBase):
    pass


class BuyerUpdate(BaseModel):
    number: Optional[str] = None


class Buyer(BuyerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    purchases: list[PurchaseBase] = []


