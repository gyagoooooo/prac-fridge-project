from pydantic import BaseModel


class IngredientCreate(
    BaseModel
):
    name: str
    quantity: int
    storage_type: str
    quantity: int
    unit: str
    expire_date: str
    memo: str = ""
    
class IngredientResponse(
    IngredientCreate
):
    id: int
    
    class Config:
        from_attrubutes = True