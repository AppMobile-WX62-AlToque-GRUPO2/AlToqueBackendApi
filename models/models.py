from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Date, Float, Time, DateTime
from config.database import Base

class Province(Base):
    __tablename__ = "province"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    
class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    provinceId = Column(Integer, ForeignKey('province.id'), nullable=False)


class District(Base):
    __tablename__ = "district"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    cityId = Column(Integer, ForeignKey('city.id'), nullable=False)


class Ubication(Base):
    __tablename__ = "ubication"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(200), nullable=False)
    districtId = Column(Integer, ForeignKey('district.id'), nullable=False)

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    password = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    role = Column(Boolean, nullable=False)
    firstName = Column(String(50), nullable=False)
    lastName = Column(String(50), nullable=False)
    phone = Column(String(15), nullable=False)
    birthdate = Column(Date, nullable=False)
    avatar = Column(String(500))
    rating = Column(Integer)  
    description = Column(String(50)) 
    ubicationId = Column(Integer, ForeignKey('ubication.id'), nullable=False)

class Notification(Base):
    __tablename__ = "notification"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(200), nullable=False)
    date = Column(DateTime, nullable=False)
    userId = Column(Integer, ForeignKey('user.id'), nullable=False)
    
class Client(Base):
    __tablename__ = "client"
    
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey('user.id'), nullable=False)

class Profession(Base):
    __tablename__ = "profession"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)

class Specialist(Base):
    __tablename__ = "specialist"

    id = Column(Integer, primary_key=True, index=True)
    workExperience = Column(Float(5, 2), nullable=False)
    consultationPrice = Column(Float, nullable=True)
    userId = Column(Integer, ForeignKey('user.id'), nullable=False)
    professionId = Column(Integer, ForeignKey('profession.id'), nullable=False)

class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String(200), nullable=False)
    address = Column(String(200), nullable=False)
    image = Column(String(500), nullable=False)
    is_publish = Column(Boolean, nullable=False)
    clientId = Column(Integer, ForeignKey('client.id'), nullable=False)

class AvailableDate(Base):
    __tablename__ = "availableDate"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    day = Column(String(10), nullable=False)
    postId = Column(Integer, ForeignKey('post.id'), nullable=False)

class Contract(Base):
    __tablename__ = "contract"

    id = Column(Integer, primary_key=True, index=True)
    state = Column(Integer, nullable=False)
    availableDateId = Column(Integer, ForeignKey('availableDate.id'), nullable=False)
    specialistId = Column(Integer, ForeignKey('specialist.id'), nullable=False)

class Review(Base):
    __tablename__ = "review"

    id = Column(Integer, primary_key=True, index=True)
    contractId = Column(Integer, ForeignKey('contract.id'), nullable=False)
    comment = Column(String(200), nullable=False)
    rating = Column(Integer, nullable=False)
    asignedTo = Column(Boolean, nullable=False)
    idUserAsigned = Column(Integer, nullable=False)
