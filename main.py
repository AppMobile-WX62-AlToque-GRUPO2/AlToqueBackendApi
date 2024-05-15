from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse

app = FastAPI(title="AlToqueAPI")
models.Base.metadata.create_all(bind=engine)

@app.get("/", include_in_schema=False)
def index():
    return RedirectResponse("/docs", status_code=300)

class UserBase(BaseModel):
    password: str
    email: str
    role: bool
    
class ContractBase(BaseModel):
    price: float
    state: int
    appointmentDate: str
    postId: int
    specialistId: int
    
class PostBase(BaseModel):
    title: str
    description: str
    address: str
    image: str
    is_publish: bool
    personaId: int
    
class PersonaBase(BaseModel):
    firstName: str
    lastName: str
    avatar: str
    phone: str
    birthdate: str
    money: float
    description: str
    rating: int
    userId: int
    ubicationId: int
        
class ProfessionBase(BaseModel):
    name: str

class SpecialistBase(BaseModel):
    workExperience: float
    Profession_idProfession: int
    personaId: int

class ProvinceBase(BaseModel):
    name: str
    
class CityBase(BaseModel):
    name: str
    provinceId: int

class DistrictBase(BaseModel):
    name: str
    cityId: int

class UbicationBase(BaseModel):
    address: str
    districtId: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

""" Users """
@app.get("/users", status_code=status.HTTP_200_OK, tags=["Users"])
async def read_users(db: db_dependency):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

@app.get("/users/{user_id}", status_code=status.HTTP_200_OK, tags=["Users"])
async def read_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users", status_code=status.HTTP_201_CREATED, tags=["Users"])
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()

@app.put("/users/{user_id}", status_code=status.HTTP_200_OK, tags=["Users"])
async def update_user(user_id: int, user: UserBase, db: db_dependency):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Actualizar los campos necesarios
    for var, value in vars(user).items():
        setattr(db_user, var, value) if value else None

    db.commit()
    return {"message": "User updated successfully"}

@app.delete("/users/{user_id}", status_code=status.HTTP_200_OK, tags=["Users"])
async def delete_user(user_id: int, db:db_dependency):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()

""" Natural People """
@app.get("/people", status_code=status.HTTP_200_OK, tags=["Natural People"])
async def read_users(db: db_dependency):
    people = db.query(models.Persona).all()
    if not people:
        raise HTTPException(status_code=404, detail="No persona found")
    return people

@app.get("/people/{persona_id}", status_code=status.HTTP_200_OK, tags=["Natural People"])
async def read_user(persona_id: int, db: db_dependency):
    persona = db.query(models.Persona).filter(models.Persona.id == persona_id).first()
    if persona is None:
        raise HTTPException(status_code=404, detail="Pesona not found")
    return persona

@app.post("/people", status_code=status.HTTP_201_CREATED, tags=["Natural People"])
async def create_persona(persona: PersonaBase, db: db_dependency):
    db_persona = models.Persona(**persona.dict())
    db.add(db_persona)
    db.commit()
    return db_persona

@app.put("/people/{persona_id}", status_code=status.HTTP_200_OK, tags=["Natural People"])
async def update_persona(persona_id: int, persona: PersonaBase, db: db_dependency):
    db_persona = db.query(models.Persona).filter(models.Persona.id == persona_id).first()
    if db_persona is None:
        raise HTTPException(status_code=404, detail="Persona not found")

    # Actualizar los campos necesarios
    for var, value in vars(persona).items():
        setattr(db_persona, var, value) if value else None

    db.commit()
    return {"message": "Persona updated successfully"}

@app.delete("/people/{persona_id}", status_code=status.HTTP_200_OK, tags=["Natural People"])
async def delete_persona(persona_id: int, db:db_dependency):
    db_persona = db.query(models.Persona).filter(models.Persona.id == persona_id).first()
    if db_persona is None:
        raise HTTPException(status_code=404, detail="Persona not found")
    db.delete(db_persona)
    db.commit()
    return {"message": "Persona deleted successfully"}




""" Professions """
@app.post("/professions", status_code=status.HTTP_201_CREATED, tags=["Professions"])
async def create_profession(profession: ProfessionBase, db: db_dependency):
    db_profession = models.Profession(**profession.dict())
    db.add(db_profession)
    db.commit()
    return db_profession

@app.get("/professions/{profession_id}", status_code=status.HTTP_200_OK, tags=["Professions"])
async def read_profession(profession_id: int, db: db_dependency):
    profession = db.query(models.Profession).filter(models.Profession.id == profession_id).first()
    if profession is None:
        raise HTTPException(status_code=404, detail="Profession not found")
    return profession

@app.put("/professions/{profession_id}", status_code=status.HTTP_200_OK, tags=["Professions"])
async def update_profession(profession_id: int, profession: ProfessionBase, db: db_dependency):
    db_profession = db.query(models.Profession).filter(models.Profession.id == profession_id).first()
    if db_profession is None:
        raise HTTPException(status_code=404, detail="Profesion not found")

    # Actualizar los campos necesarios
    for var, value in vars(profession).items():
        setattr(db_profession, var, value) if value else None

    db.commit()
    return {"message": "Profession updated successfully"}

@app.delete("/professions/{profession_id}", status_code=status.HTTP_200_OK, tags=["Professions"])
async def delete_profession(profession_id: int, db:db_dependency):
    db_profession = db.query(models.Profession).filter(models.Profession.id == profession_id).first()
    if db_profession is None:
        raise HTTPException(status_code=404, detail="Profession not found")
    db.delete(db_profession)
    db.commit()
    return {"message": "Profession deleted successfully"}


""" Specialists """
@app.post("/specialists", status_code=status.HTTP_201_CREATED, tags=["Specialists"])
async def create_specialist(specialist: SpecialistBase, db: db_dependency):
    db_specialist = models.Specialist(**specialist.dict())
    db.add(db_specialist)
    db.commit()
    return db_specialist

@app.get("/specialists/{specialist_id}", status_code=status.HTTP_200_OK, tags=["Specialists"])
async def read_specialist(specialist_id: int, db: db_dependency):
    specialist = db.query(models.Specialist).filter(models.Specialist.id == specialist_id).first()
    if specialist is None:
        raise HTTPException(status_code=404, detail="Specialist not found")
    return specialist

@app.put("/specialists/{specialist_id}", status_code=status.HTTP_200_OK, tags=["Specialists"])
async def update_specialist(specialist_id: int, specialist: SpecialistBase, db: db_dependency):
    db_specialist = db.query(models.Specialist).filter(models.Specialist.id == specialist_id).first()
    if db_specialist is None:
        raise HTTPException(status_code=404, detail="Specialist not found")

    # Actualizar los campos necesarios
    for var, value in vars(specialist).items():
        setattr(db_specialist, var, value) if value else None

    db.commit()
    return {"message": "Specialist updated successfully"}

@app.delete("/specialists/{specialist_id}", status_code=status.HTTP_200_OK, tags=["Specialists"])
async def delete_specialist(specialist_id: int, db:db_dependency):
    db_specialist = db.query(models.Specialist).filter(models.Specialist.id == specialist_id).first()
    if db_specialist is None:
        raise HTTPException(status_code=404, detail="Specialist not found")
    db.delete(db_specialist)
    db.commit()
    return {"message": "Specialist deleted successfully"}




""" Posts """
@app.post("/posts", status_code=status.HTTP_201_CREATED, tags=["Posts"])
async def create_post(post: PostBase, db: db_dependency):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    return db_post

@app.get("/posts/{post_id}", status_code=status.HTTP_200_OK, tags=["Posts"])
async def read_post(post_id: int, db: db_dependency):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.put("/posts/{post_id}", status_code=status.HTTP_200_OK, tags=["Posts"])
async def update_post(post_id: int, post: PostBase, db: db_dependency):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    # Actualizar los campos necesarios
    for var, value in vars(post).items():
        setattr(db_post, var, value) if value else None

    db.commit()
    return {"message": "Post updated successfully"}

@app.delete("/posts/{post_id}", status_code=status.HTTP_200_OK, tags=["Posts"])
async def delete_post(post_id: int, db:db_dependency):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(db_post)
    db.commit()
    return {"message": "Post deleted successfully"}


""" Contracts """
@app.post("/contracts", status_code=status.HTTP_201_CREATED, tags=["Contracts"])
async def create_contract(contract: ContractBase, db: db_dependency):
    db_contract = models.Contract(**contract.dict())
    db.add(db_contract)
    db.commit()
    return db_contract

@app.get("/contracts/{contract_id}", status_code=status.HTTP_200_OK, tags=["Contracts"])
async def read_contract(contract_id: int, db: db_dependency):
    contract = db.query(models.Contract).filter(models.Contract.id == contract_id).first()
    if contract is None:
        raise HTTPException(status_code=404, detail="Contract not found")
    return contract

@app.put("/contracts/{contract_id}", status_code=status.HTTP_200_OK, tags=["Contracts"])
async def update_contract(contract_id: int, contract: ContractBase, db: db_dependency):
    db_contract = db.query(models.Contract).filter(models.Contract.id == contract_id).first()
    if db_contract is None:
        raise HTTPException(status_code=404, detail="Contract not found")

    # Actualizar los campos necesarios
    for var, value in vars(contract).items():
        setattr(db_contract, var, value) if value else None

    db.commit()
    return {"message": "Contract updated successfully"}

@app.delete("/contracts/{contract_id}", status_code=status.HTTP_200_OK, tags=["Contracts"])
async def delete_contract(contract_id: int, db:db_dependency):
    db_contract = db.query(models.Contract).filter(models.Contract.id == contract_id).first()
    if db_contract is None:
        raise HTTPException(status_code=404, detail="Contract not found")
    db.delete(db_contract)
    db.commit()
    return {"message": "Contract deleted successfully"}




""" Provinces """
@app.get("/provinces", status_code=status.HTTP_200_OK, tags=["Provinces"])
async def read_provinces(db: db_dependency):
    provinces = db.query(models.Province).all()
    if not provinces:
        raise HTTPException(status_code=404, detail="No users found")
    return provinces

@app.get("/provinces/{province_id}", status_code=status.HTTP_200_OK, tags=["Provinces"])
async def read_province(province_id: int, db: db_dependency):
    province = db.query(models.Province).filter(models.Province.id == province_id).first()
    if province is None:
        raise HTTPException(status_code=404, detail="Province not found")
    return province

@app.post("/provinces", status_code=status.HTTP_201_CREATED, tags=["Provinces"])
async def create_province(province: ProvinceBase, db: db_dependency):
    db_province = models.Province(**province.dict())
    db.add(db_province)
    db.commit()
    return db_province

@app.put("/provinces/{province_id}", status_code=status.HTTP_200_OK, tags=["Provinces"])
async def update_province(province_id: int, province: ProvinceBase, db: db_dependency):
    db_province = db.query(models.Province).filter(models.Province.id == province_id).first()
    if db_province is None:
        raise HTTPException(status_code=404, detail="Province not found")

    # Actualizar los campos necesarios
    for var, value in vars(province).items():
        setattr(db_province, var, value) if value else None

    db.commit()
    return {"message": "Province updated successfully"}

@app.delete("/provinces/{province_id}", status_code=status.HTTP_200_OK, tags=["Provinces"])
async def delete_province(province_id: int, db:db_dependency):
    db_province = db.query(models.Province).filter(models.Province.id == province_id).first()
    if db_province is None:
        raise HTTPException(status_code=404, detail="Province not found")
    db.delete(db_province)
    db.commit()
    return {"message": "Province eliminated successfully"}




""" Cities """
@app.get("/cities", status_code=status.HTTP_200_OK, tags=["Cities"])
async def read_cities(db: db_dependency):
    cities = db.query(models.City).all()
    if not cities:
        raise HTTPException(status_code=404, detail="No cities found")
    return cities

@app.get("/cities/{city_id}", status_code=status.HTTP_200_OK, tags=["Cities"])
async def read_city(city_id: int, db: db_dependency):
    city = db.query(models.City).filter(models.City.id == city_id).first()
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city

@app.post("/cities", status_code=status.HTTP_201_CREATED, tags=["Cities"])
async def create_city(city: CityBase, db: db_dependency):
    db_city = models.City(**city.dict())
    db.add(db_city)
    db.commit()
    return db_city

@app.put("/cities/{city_id}", status_code=status.HTTP_200_OK, tags=["Cities"])
async def update_city(city_id: int, city: CityBase, db: db_dependency):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    # Actualizar los campos necesarios
    for var, value in vars(city).items():
        setattr(db_city, var, value) if value else None

    db.commit()
    return {"message": "Province updated successfully"}

@app.delete("/cities/{city_id}", status_code=status.HTTP_200_OK, tags=["Cities"])
async def delete_city(city_id: int, db:db_dependency):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    db.delete(db_city)
    db.commit()
    return {"message": "City eliminated successfully"}



""" Districts """
@app.get("/districts", status_code=status.HTTP_200_OK, tags=["Districts"])
async def read_districts(db: db_dependency):
    districts = db.query(models.District).all()
    if not districts:
        raise HTTPException(status_code=404, detail="No District found")
    return districts

@app.get("/districts/{district_id}", status_code=status.HTTP_200_OK, tags=["Districts"])
async def read_district(district_id: int, db: db_dependency):
    district = db.query(models.District).filter(models.District.id == district_id).first()
    if district is None:
        raise HTTPException(status_code=404, detail="District not found")
    return district

@app.post("/districts", status_code=status.HTTP_201_CREATED, tags=["Districts"])
async def create_district(district: DistrictBase, db: db_dependency):
    db_district = models.District(**district.dict())
    db.add(db_district)
    db.commit()
    return db_district

@app.put("/districts/{district_id}", status_code=status.HTTP_200_OK, tags=["Districts"])
async def update_district(district_id: int, district: DistrictBase, db: db_dependency):
    db_district = db.query(models.District).filter(models.District.id == district_id).first()
    if db_district is None:
        raise HTTPException(status_code=404, detail="City not found")

    # Actualizar los campos necesarios
    for var, value in vars(district).items():
        setattr(db_district, var, value) if value else None

    db.commit()
    return {"message": "District updated successfully"}

@app.delete("/districts/{district_id}", status_code=status.HTTP_200_OK, tags=["Districts"])
async def delete_district(district_id: int, db:db_dependency):
    db_district = db.query(models.District).filter(models.District.id == district_id).first()
    if db_district is None:
        raise HTTPException(status_code=404, detail="District not found")
    db.delete(db_district)
    db.commit()
    return {"message": "District eliminated successfully"}




""" Ubications """
@app.get("/ubications", status_code=status.HTTP_200_OK, tags=["Ubications"])
async def read_ubications(db: db_dependency):
    ubications = db.query(models.Ubication).all()
    if not ubications:
        raise HTTPException(status_code=404, detail="No Ubication found")
    return ubications

@app.get("/ubications/{ubication_id}", status_code=status.HTTP_200_OK, tags=["Ubications"])
async def read_ubication(ubication_id: int, db: db_dependency):
    ubication = db.query(models.Ubication).filter(models.Ubication.id == ubication_id).first()
    if ubication is None:
        raise HTTPException(status_code=404, detail="Ubication not found")
    return ubication

@app.post("/ubications", status_code=status.HTTP_201_CREATED, tags=["Ubications"])
async def create_ubication(ubication: UbicationBase, db: db_dependency):
    db_ubication = models.Ubication(**ubication.dict())
    db.add(db_ubication)
    db.commit()
    return db_ubication

@app.put("/ubications/{ubication_id}", status_code=status.HTTP_200_OK, tags=["Ubications"])
async def update_ubication(ubication_id: int, ubication: UbicationBase, db: db_dependency):
    db_ubication = db.query(models.Ubication).filter(models.Ubication.id == ubication_id).first()
    if db_ubication is None:
        raise HTTPException(status_code=404, detail="City not found")

    # Actualizar los campos necesarios
    for var, value in vars(ubication).items():
        setattr(db_ubication, var, value) if value else None

    db.commit()
    return {"message": "Ubication updated successfully"}

@app.delete("/ubications/{ubication_id}", status_code=status.HTTP_200_OK, tags=["Ubications"])
async def delete_ubication(ubication_id: int, db:db_dependency):
    db_ubication = db.query(models.Ubication).filter(models.Ubication.id == ubication_id).first()
    if db_ubication is None:
        raise HTTPException(status_code=404, detail="Ubication not found")
    db.delete(db_ubication)
    db.commit()
    return {"message": "Ubication eliminated successfully"}
