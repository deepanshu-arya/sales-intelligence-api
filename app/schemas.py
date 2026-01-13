from datetime import date
from pydantic import BaseModel


class SaleBase(BaseModel):
    date: date
    product_name: str
    quantity: int
    price: float


class SaleCreate(SaleBase):
    pass


class SaleResponse(SaleBase):
    id: int
    total_amount: float

    class Config:
        from_attributes = True
