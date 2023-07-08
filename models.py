from pydantic import BaseModel, Field

class Customer(BaseModel):
    id: int = Field(description="Unique ID of the customer.")
    first_name: str = Field(description="Customer's first name.")
    last_name: str = Field(description="Customer's last name.")
    email: str = Field(description="Email address of the customer.")
    is_verified: bool = Field(description="Information if the customer has verified his account")

class Item(BaseModel):
    serial_id: int = Field(description="Unique ID of the item.")
    name: str = Field(description="Name of the item.")
    price: float = Field(description="Price of the item in USD.")
    stock: int = Field(description="Amount of the pieces currently in stock.")
    added: str = Field(description="Date when was the item added to store")
