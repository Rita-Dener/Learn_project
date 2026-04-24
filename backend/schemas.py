from typing import Optional
from pydantic import BaseModel, Field

class Material(BaseModel):
    title: str = Field(..., min_length=2, max_length=50, description='Название материала')
    description: Optional[str] = Field(..., min_length=2, max_length=100, description='Описание материала')
    link: str = Field(..., min_length=2, description='Ссылка на материал')

class MaterialsCreate(Material):
    pass

class MaterialUpdate(Material):
    pass

class MaterialPatch(BaseModel):
    title: Optional[str] = Field(default=None, min_length=2, max_length=50)
    description: Optional[str] = Field(default=None, min_length=2, max_length=100)
    link: Optional[str] = Field(default=None, min_length=2)

class MaterialResponse(Material):
    id: int