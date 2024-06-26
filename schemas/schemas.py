from pydantic import BaseModel, Field, EmailStr

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




#User
class UserAuth(BaseModel):
    email: EmailStr
    password: str
    role: bool

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: bool
    firstName: str
    lastName: str
    phone: str
    birthdate: str = Field(default="2002-03-21")
    avatar: str = Field(default="https://as1.ftcdn.net/v2/jpg/03/39/45/96/1000_F_339459697_XAFacNQmwnvJRqe1Fe9VOptPWMUxlZP8.jpg")
    description: str = Field(default="")
    rating: int = Field(default=1)
    ubicationId: int

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    firstName: str
    lastName: str
    phone: str
    birthdate: str
    avatar: str
    description: str
    rating: int
    ubicationId: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    password: str
    email: str
    role: bool
    firstName: str
    lastName: str
    phone: str
    birthdate: str = Field(default="2002-03-21")
    avatar: str = Field(default="https://as1.ftcdn.net/v2/jpg/03/39/45/96/1000_F_339459697_XAFacNQmwnvJRqe1Fe9VOptPWMUxlZP8.jpg")
    description: str = Field(default="")
    rating: int = Field(default=1)
    ubicationId: int

class UserUpdate(BaseModel):
    email: str
    role: bool
    firstName: str
    lastName: str
    phone: str
    birthdate: str = Field(default="2002-03-21")
    avatar: str = Field(default="https://as1.ftcdn.net/v2/jpg/03/39/45/96/1000_F_339459697_XAFacNQmwnvJRqe1Fe9VOptPWMUxlZP8.jpg")
    description: str = Field(default="")
    ubicationId: int





class NotificationBase(BaseModel):
    text: str
    date: str
    userId: str

class ClientBase(BaseModel):
    userId: int

class ProfessionBase(BaseModel):
    name: str

class SpecialistBase(BaseModel):
    workExperience: float
    consultationPrice: float
    professionId: int
    userId: int

class PostBase(BaseModel):
    title: str
    description: str
    address: str
    image: str
    is_publish: bool
    clientId: int

class AvailableDateBase(BaseModel):
    start_time: str
    end_time: str
    day: str
    postId: int

class ContractBase(BaseModel):
    state: int
    availableDateId: int
    specialistId: int

class ReviewBase(BaseModel):
    comment: str
    rating: int
    contractId: int
    asignedTo: bool
    idUserAsigned: int

class Review(ReviewBase):
    id: int

    class Config:
        from_attributes = True