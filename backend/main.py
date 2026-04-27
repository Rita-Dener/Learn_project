from fastapi import FastAPI, HTTPException
from . import crud
from .database import init_db
from .schemas import MaterialsCreate, MaterialUpdate, MaterialPatch, MaterialResponse

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def root():
    return {"message": "FastAPI работает!!!"}

@app.get("/materials", response_model=list[MaterialResponse], tags=["Materials"])
def get_materials():
    return crud.get_all()

@app.get("/materials/{material_id}", response_model=MaterialResponse, tags=["Materials"])
def read_material_by_id(material_id: int):
    material = crud.get_by_id(material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Материал не найден")
    return material

@app.post("/materials", response_model=MaterialResponse, tags=["Materials"])
def create_materials(materials: MaterialsCreate):
    return crud.create_material(materials.model_dump())

@app.put("/materials/{material_id}", response_model=MaterialResponse, tags=["Materials"])
def update_material_by_id(material_id: int, material: MaterialUpdate):
    updated_material = crud.update_material(material_id, material.model_dump())
    if not updated_material:
        raise HTTPException(status_code=404, detail="Материал не найден")
    return updated_material

@app.patch("/materials/{material_id}", response_model=MaterialResponse, tags=["Materials"])
def patch_material_by_id(material_id: int, material: MaterialPatch):
    updated_material = crud.patch_material(material_id, material.model_dump())
    if not updated_material:
        raise HTTPException(status_code=404, detail="Материал не найден")
    return updated_material

@app.delete("/materials/{material_id}", response_model=MaterialResponse, tags=["Materials"])
def delete_material_by_id(material_id: int):
    deleted_material = crud.delete_material(material_id)
    if not deleted_material:
        raise HTTPException(status_code=404, detail="Материал не найден")
    return {"message": "Материал успешно удалён"}