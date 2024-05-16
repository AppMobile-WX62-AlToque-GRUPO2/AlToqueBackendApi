from pydantic import BaseModel

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

class UserBase(BaseModel):
    password: str
    email: str
    role: bool

class PersonaBase(BaseModel):
    firstName: str
    lastName: str
    avatar: str
    phone: str
    birthdate: str
    description: str
    rating: int
    userId: int
    ubicationId: int

class ProfessionBase(BaseModel):
    name: str

class SpecialistBase(BaseModel):
    workExperience: float
    consultationPrice: float
    Profession_idProfession: int
    personaId: int

class PostBase(BaseModel):
    title: str
    description: str
    address: str
    image: str
    is_publish: bool
    personaId: int

class AvailableDateBase(BaseModel):
    start_time: str
    end_time: str
    day: str
    postId: int

class ContractBase(BaseModel):
    state: int
    availableDateId: int
    specialistId: int