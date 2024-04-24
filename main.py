from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class UserBase(BaseModel):
    password: str
    email: str
    
class ContractBase(BaseModel):
    price: float
    state: int
    appointmentDate: str
    publicationId: int
    specialistId: int
    
class PublicationBase(BaseModel):
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
    role: bool
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

class CityBase(BaseModel):
    id: int
    name: str

class DistrictBase(BaseModel):
    id: int
    name: str
    cityId: int

class UbicationBase(BaseModel):
    id: int
    address: str
    districtId: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    
@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/personas", status_code=status.HTTP_201_CREATED)
async def create_persona(persona: PersonaBase, db: db_dependency):
    db_persona = models.Persona(**persona.dict())
    db.add(db_persona)
    db.commit()
    return db_persona

@app.post("/professions", status_code=status.HTTP_201_CREATED)
async def create_profession(profession: ProfessionBase, db: db_dependency):
    db_profession = models.Profession(**profession.dict())
    db.add(db_profession)
    db.commit()
    return db_profession

@app.get("/professions/{profession_id}", status_code=status.HTTP_200_OK)
async def read_profession(profession_id: int, db: db_dependency):
    profession = db.query(models.Profession).filter(models.Profession.id == profession_id).first()
    if profession is None:
        raise HTTPException(status_code=404, detail="Profession not found")
    return profession

@app.post("/specialists", status_code=status.HTTP_201_CREATED)
async def create_specialist(specialist: SpecialistBase, db: db_dependency):
    db_specialist = models.Specialist(**specialist.dict())
    db.add(db_specialist)
    db.commit()
    return db_specialist

@app.get("/specialists/{specialist_id}", status_code=status.HTTP_200_OK)
async def read_specialist(specialist_id: int, db: db_dependency):
    specialist = db.query(models.Specialist).filter(models.Specialist.id == specialist_id).first()
    if specialist is None:
        raise HTTPException(status_code=404, detail="Specialist not found")
    return specialist

@app.post("/publications", status_code=status.HTTP_201_CREATED)
async def create_publication(publication: PublicationBase, db: db_dependency):
    db_publication = models.Publication(**publication.dict())
    db.add(db_publication)
    db.commit()
    return db_publication

@app.get("/publications/{publication_id}", status_code=status.HTTP_200_OK)
async def read_publication(publication_id: int, db: db_dependency):
    publication = db.query(models.Publication).filter(models.Publication.id == publication_id).first()
    if publication is None:
        raise HTTPException(status_code=404, detail="Publication not found")
    return publication

@app.post("/contracts", status_code=status.HTTP_201_CREATED)
async def create_contract(contract: ContractBase, db: db_dependency):
    db_contract = models.Contract(**contract.dict())
    db.add(db_contract)
    db.commit()
    return db_contract

@app.get("/contracts/{contract_id}", status_code=status.HTTP_200_OK)
async def read_contract(contract_id: int, db: db_dependency):
    contract = db.query(models.Contract).filter(models.Contract.id == contract_id).first()
    if contract is None:
        raise HTTPException(status_code=404, detail="Contract not found")
    return contract

@app.post("/cities", status_code=status.HTTP_201_CREATED)
async def create_city(city: CityBase, db: db_dependency):
    db_city = models.City(**city.dict())
    db.add(db_city)
    db.commit()
    return db_city

@app.get("/cities/{city_id}", status_code=status.HTTP_200_OK)
async def read_city(city_id: int, db: db_dependency):
    city = db.query(models.City).filter(models.City.id == city_id).first()
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city

@app.post("/districts", status_code=status.HTTP_201_CREATED)
async def create_district(district: DistrictBase, db: db_dependency):
    db_district = models.District(**district.dict())
    db.add(db_district)
    db.commit()
    return db_district

@app.get("/districts/{district_id}", status_code=status.HTTP_200_OK)
async def read_district(district_id: int, db: db_dependency):
    district = db.query(models.District).filter(models.District.id == district_id).first()
    if district is None:
        raise HTTPException(status_code=404, detail="District not found")
    return district

@app.post("/ubications", status_code=status.HTTP_201_CREATED)
async def create_ubication(ubication: UbicationBase, db: db_dependency):
    db_ubication = models.Ubication(**ubication.dict())
    db.add(db_ubication)
    db.commit()
    return db_ubication

@app.get("/ubications/{ubication_id}", status_code=status.HTTP_200_OK)
async def read_ubication(ubication_id: int, db: db_dependency):
    ubication = db.query(models.Ubication).filter(models.Ubication.id == ubication_id).first()
    if ubication is None:
        raise HTTPException(status_code=404, detail="Ubication not found")
    return ubication