from typing import Optional

from pydantic import BaseModel, Field


class LoginData(BaseModel):
    id: int
    username: str
    email: str
    firstName: str
    lastName: str
    gender: str
    image: str
    accessToken: str
    refreshToken: str


class UserData(BaseModel):
    id: int
    username: str
    email: str
    firstName: str
    lastName: str
    gender: str
    image: str

class CartsData(BaseModel):
    carts: list[CartData]
    total: int
    skip: int
    limit: int

class CartData(BaseModel):
    id: int
    products: list[ProductsData]
    total: float
    discountedTotal: float
    userId: int
    totalProducts: int
    totalQuantity: int

class CartDeletedData(BaseModel):
    id: int
    products: list[ProductsData]
    total: float
    discountedTotal: float
    userId: int
    totalProducts: int
    totalQuantity: int
    isDeleted: bool = True
    deletedOn: str = Field(pattern=r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$')

class ProductsData(BaseModel):
    id: int
    title: str
    price: float
    quantity: int
    total: float
    discountPercentage: float
    discountedPrice: Optional[float] = None
    discountedTotal: Optional[float] = None
    thumbnail: str
