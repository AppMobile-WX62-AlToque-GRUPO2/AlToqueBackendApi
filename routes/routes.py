from fastapi import HTTPException, Depends, status, APIRouter, Query
from typing import Annotated, List
from sqlalchemy.orm import Session
from datetime import datetime

from config.database import get_db
import models.models as models
from schemas.schemas import UserUpdate, UserBase, NotificationBase, ContractBase, PostBase, AvailableDateBase, ClientBase, ProfessionBase, SpecialistBase, ProvinceBase, CityBase, DistrictBase, UbicationBase, ReviewBase, Review

from routes.auth import hash_password

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]

""" Users """
@router.get("/users", status_code=status.HTTP_200_OK, tags=["Users"])
async def read_users(db: db_dependency):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

@router.get("/users/{user_id}", status_code=status.HTTP_200_OK, tags=["Users"])
async def read_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/users", status_code=status.HTTP_201_CREATED, tags=["Users"])
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()

@router.put("/users/{user_id}", status_code=status.HTTP_200_OK, tags=["Users"])
async def update_user(user_id: int, user: UserUpdate, db: db_dependency):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for var, value in vars(user).items():
        # Si la variable es 'password', la hasheamos
        if var == 'password' and value:
            value = hash_password(value)
        setattr(db_user, var, value)

    db.commit()
    return {"message": "User updated successfully"}

@router.delete("/users/{user_id}", status_code=status.HTTP_200_OK, tags=["Users"])
async def delete_user(user_id: int, db:db_dependency):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()




""" Notifications """
@router.get("/notifications", status_code=status.HTTP_200_OK, tags=["Notifications"])
async def read_notifications(db: db_dependency):
    notifications = db.query(models.Notification).all()
    if not notifications:
        raise HTTPException(status_code=404, detail="No notifications found")
    return notifications

@router.get("/notifications/{notification_id}", status_code=status.HTTP_200_OK, tags=["Notifications"])
async def read_notification(notification_id: int, db: db_dependency):
    notification = db.query(models.Notification).filter(models.Notification.id == notification_id).first()
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@router.post("/notifications", status_code=status.HTTP_201_CREATED, tags=["Notifications"])
async def create_notification(notification: NotificationBase, db: db_dependency):
    db_notification = models.Notification(**notification.dict())
    db.add(db_notification)
    db.commit()

@router.put("/notifications/{notification_id}", status_code=status.HTTP_200_OK, tags=["Notifications"])
async def update_notification(notification_id: int, notification: NotificationBase, db: db_dependency):
    db_notification = db.query(models.Notification).filter(models.Notification.id == notification_id).first()
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")

    # Actualizar los campos necesarios
    for var, value in vars(notification).items():
        setattr(db_notification, var, value) if value else None

    db.commit()
    return {"message": "Notification updated successfully"}

@router.delete("/notifications/{notification_id}", status_code=status.HTTP_200_OK, tags=["Notifications"])
async def delete_notification(notification_id: int, db:db_dependency):
    db_notification = db.query(models.Notification).filter(models.Notification.id == notification_id).first()
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    db.delete(db_notification)
    db.commit()





""" Client """
@router.get("/clients", status_code=status.HTTP_200_OK, tags=["Clients"])
async def read_clients(db: db_dependency):
    clients = db.query(models.Client).all()
    if not clients:
        raise HTTPException(status_code=404, detail="No client found")
    return clients

@router.get("/clients/{client_id}", status_code=status.HTTP_200_OK, tags=["Clients"])
async def read_client(client_id: int, db: db_dependency):
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Pesona not found")
    return client

@router.post("/clients", status_code=status.HTTP_201_CREATED, tags=["Clients"])
async def create_client(client: ClientBase, db: db_dependency):
    db_client = models.Client(**client.dict())
    db.add(db_client)
    db.commit()
    return db_client

@router.put("/clients/{client_id}", status_code=status.HTTP_200_OK, tags=["Clients"])
async def update_client(client_id: int, client: ClientBase, db: db_dependency):
    db_client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")

    for var, value in vars(client).items():
        setattr(db_client, var, value) if value else None

    db.commit()
    return {"message": "Client updated successfully"}

@router.delete("/clients/{client_id}", status_code=status.HTTP_200_OK, tags=["Clients"])
async def delete_client(client_id: int, db:db_dependency):
    db_client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(db_client)
    db.commit()
    return {"message": "Client deleted successfully"}





""" Professions """
@router.post("/professions", status_code=status.HTTP_201_CREATED, tags=["Professions"])
async def create_profession(profession: ProfessionBase, db: db_dependency):
    db_profession = models.Profession(**profession.dict())
    db.add(db_profession)
    db.commit()
    return db_profession

@router.get("/professions/{profession_id}", status_code=status.HTTP_200_OK, tags=["Professions"])
async def read_profession(profession_id: int, db: db_dependency):
    profession = db.query(models.Profession).filter(models.Profession.id == profession_id).first()
    if profession is None:
        raise HTTPException(status_code=404, detail="Profession not found")
    return profession

@router.put("/professions/{profession_id}", status_code=status.HTTP_200_OK, tags=["Professions"])
async def update_profession(profession_id: int, profession: ProfessionBase, db: db_dependency):
    db_profession = db.query(models.Profession).filter(models.Profession.id == profession_id).first()
    if db_profession is None:
        raise HTTPException(status_code=404, detail="Profesion not found")

    # Actualizar los campos necesarios
    for var, value in vars(profession).items():
        setattr(db_profession, var, value) if value else None

    db.commit()
    return {"message": "Profession updated successfully"}

@router.delete("/professions/{profession_id}", status_code=status.HTTP_200_OK, tags=["Professions"])
async def delete_profession(profession_id: int, db:db_dependency):
    db_profession = db.query(models.Profession).filter(models.Profession.id == profession_id).first()
    if db_profession is None:
        raise HTTPException(status_code=404, detail="Profession not found")
    db.delete(db_profession)
    db.commit()
    return {"message": "Profession deleted successfully"}


""" Specialists """
@router.post("/specialists", status_code=status.HTTP_201_CREATED, tags=["Specialists"])
async def create_specialist(specialist: SpecialistBase, db: db_dependency):
    db_specialist = models.Specialist(**specialist.dict())
    db.add(db_specialist)
    db.commit()
    return db_specialist

@router.get("/specialists/{specialist_id}", status_code=status.HTTP_200_OK, tags=["Specialists"])
async def read_specialist(specialist_id: int, db: db_dependency):
    specialist = db.query(models.Specialist).filter(models.Specialist.id == specialist_id).first()
    if specialist is None:
        raise HTTPException(status_code=404, detail="Specialist not found")
    return specialist

@router.put("/specialists/{specialist_id}", status_code=status.HTTP_200_OK, tags=["Specialists"])
async def update_specialist(specialist_id: int, specialist: SpecialistBase, db: db_dependency):
    db_specialist = db.query(models.Specialist).filter(models.Specialist.id == specialist_id).first()
    if db_specialist is None:
        raise HTTPException(status_code=404, detail="Specialist not found")

    # Actualizar los campos necesarios
    for var, value in vars(specialist).items():
        setattr(db_specialist, var, value) if value else None

    db.commit()
    return {"message": "Specialist updated successfully"}

@router.delete("/specialists/{specialist_id}", status_code=status.HTTP_200_OK, tags=["Specialists"])
async def delete_specialist(specialist_id: int, db:db_dependency):
    db_specialist = db.query(models.Specialist).filter(models.Specialist.id == specialist_id).first()
    if db_specialist is None:
        raise HTTPException(status_code=404, detail="Specialist not found")
    db.delete(db_specialist)
    db.commit()
    return {"message": "Specialist deleted successfully"}




""" Posts """
@router.get("/posts", status_code=status.HTTP_200_OK, tags=["Posts"])
async def read_posts(db: db_dependency, clientId: int = Query(None)):
    if clientId is not None:
        posts = db.query(models.Post).filter(models.Post.clientId == clientId).all()
        if not posts:
            raise HTTPException(status_code=404, detail=f"No posts found for client ID {clientId}")
    else:
        posts = db.query(models.Post).all()
        if not posts:
            raise HTTPException(status_code=404, detail="No posts found")
    return posts

@router.post("/posts", status_code=status.HTTP_201_CREATED, tags=["Posts"])
async def create_post(post: PostBase, db: db_dependency):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    return db_post

@router.get("/posts/{post_id}", status_code=status.HTTP_200_OK, tags=["Posts"])
async def read_post(post_id: int, db: db_dependency):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/posts/{post_id}", status_code=status.HTTP_200_OK, tags=["Posts"])
async def update_post(post_id: int, post: PostBase, db: db_dependency):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    # Actualizar los campos necesarios
    for var, value in vars(post).items():
        setattr(db_post, var, value) if value else None

    db.commit()
    return {"message": "Post updated successfully"}

@router.delete("/posts/{post_id}", status_code=status.HTTP_200_OK, tags=["Posts"])
async def delete_post(post_id: int, db:db_dependency):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(db_post)
    db.commit()
    return {"message": "Post deleted successfully"}


""" Contracts """
@router.post("/contracts", status_code=status.HTTP_201_CREATED, tags=["Contracts"])
async def create_contract(contract: ContractBase, db: db_dependency):
    db_contract = models.Contract(**contract.dict())
    db.add(db_contract)
    db.commit()
    return db_contract

@router.get("/contracts/{contract_id}", status_code=status.HTTP_200_OK, tags=["Contracts"])
async def read_contract(contract_id: int, db: db_dependency):
    contract = db.query(models.Contract).filter(models.Contract.id == contract_id).first()
    if contract is None:
        raise HTTPException(status_code=404, detail="Contract not found")
    return contract

@router.put("/contracts/{contract_id}", status_code=status.HTTP_200_OK, tags=["Contracts"])
async def update_contract(contract_id: int, contract: ContractBase, db: db_dependency):
    db_contract = db.query(models.Contract).filter(models.Contract.id == contract_id).first()
    if db_contract is None:
        raise HTTPException(status_code=404, detail="Contract not found")

    # Actualizar los campos necesarios
    for var, value in vars(contract).items():
        setattr(db_contract, var, value) if value else None

    db.commit()
    return {"message": "Contract updated successfully"}

@router.delete("/contracts/{contract_id}", status_code=status.HTTP_200_OK, tags=["Contracts"])
async def delete_contract(contract_id: int, db:db_dependency):
    db_contract = db.query(models.Contract).filter(models.Contract.id == contract_id).first()
    if db_contract is None:
        raise HTTPException(status_code=404, detail="Contract not found")
    db.delete(db_contract)
    db.commit()
    return {"message": "Contract deleted successfully"}





""" AvailableDate """
@router.post("/availableDates", status_code=status.HTTP_201_CREATED, tags=["AvailableDates"])
async def create_availableDate(availableDate: AvailableDateBase, db: db_dependency):
    db_dates = models.AvailableDate(**availableDate.dict())
    db.add(db_dates)
    db.commit()
    return db_dates

@router.get("/availableDates/{availableDate_id}", status_code=status.HTTP_200_OK, tags=["AvailableDates"])
async def read_availableDates(availableDate_id: int, db: db_dependency):
    availableDate = db.query(models.AvailableDate).filter(models.AvailableDate.id == availableDate_id).first()
    if availableDate is None:
        raise HTTPException(status_code=404, detail="available date not found")
    return availableDate

@router.put("/availableDates/{availableDate_id}", status_code=status.HTTP_200_OK, tags=["AvailableDates"])
async def update_availableDate(availableDate_id: int, availableDate: PostBase, db: db_dependency):
    db_dates = db.query(models.AvailableDate).filter(models.AvailableDate.id == availableDate_id).first()
    if db_dates is None:
        raise HTTPException(status_code=404, detail="available date not found")

    for var, value in vars(availableDate).items():
        setattr(db_dates, var, value) if value else None

    db.commit()
    return {"message": "available date updated successfully"}

@router.delete("/availableDates/{availableDate_id}", status_code=status.HTTP_200_OK, tags=["AvailableDates"])
async def delete_availableDate(availableDate_id: int, db:db_dependency):
    db_dates = db.query(models.AvailableDate).filter(models.AvailableDate.id == availableDate_id).first()
    if db_dates is None:
        raise HTTPException(status_code=404, detail="available date not found")
    db.delete(db_dates)
    db.commit()
    return {"message": "available date deleted successfully"}



""" Review """
@router.post("/reviews", status_code=status.HTTP_201_CREATED, tags=["Reviews"])
async def create_review(review: ReviewBase, db: db_dependency):
    db_review = models.Review(**review.dict())
    db.add(db_review)
    db.commit()
    return db_review

@router.get("/reviews/{review_id}", status_code=status.HTTP_200_OK, tags=["Reviews"])
async def read_review(review_id: int, db: db_dependency):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.put("/reviews/{review_id}", status_code=status.HTTP_200_OK, tags=["Reviews"])
async def update_review(review_id: int, review: ReviewBase, db: db_dependency):
    db_review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")

    # Actualizar los campos necesarios
    for var, value in vars(review).items():
        setattr(db_review, var, value) if value else None

    db.commit()
    return {"message": "Review updated successfully"}

@router.delete("/reviews/{review_id}", status_code=status.HTTP_200_OK, tags=["Reviews"])
async def delete_review(review_id: int, db:db_dependency):
    db_review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(db_review)
    db.commit()
    return {"message": "Review deleted successfully"}

@router.get("/reviews/client/{id_user}", status_code=status.HTTP_200_OK, response_model=List[Review], tags=["Reviews"])
async def get_reviews_of_client_by_userId(id_user: int, db: Session = Depends(get_db)):
    
    reviews = (
        db.query(models.Review)
        .filter(models.Review.asignedTo == True)
        .filter(models.Review.idUserAsigned == id_user)
        .all()
    )

    return reviews

@router.get("/reviews/specialist/{id_user}", status_code=status.HTTP_200_OK, response_model=List[Review], tags=["Reviews"])
async def get_reviews_of_specialist_by_userId(id_user: int, db: Session = Depends(get_db)):
    reviews = (
        db.query(models.Review)
        .filter(models.Review.asignedTo == False)
        .filter(models.Review.idUserAsigned == id_user)
        .all()
    )

    return reviews


""" Provinces """
@router.get("/provinces", status_code=status.HTTP_200_OK, tags=["Provinces"])
async def read_provinces(db: db_dependency):
    provinces = db.query(models.Province).all()
    if not provinces:
        raise HTTPException(status_code=404, detail="No provinces found")
    return provinces

@router.get("/provinces/{province_id}", status_code=status.HTTP_200_OK, tags=["Provinces"])
async def read_province(province_id: int, db: db_dependency):
    province = db.query(models.Province).filter(models.Province.id == province_id).first()
    if province is None:
        raise HTTPException(status_code=404, detail="Province not found")
    return province

@router.post("/provinces", status_code=status.HTTP_201_CREATED, tags=["Provinces"])
async def create_province(province: ProvinceBase, db: db_dependency):
    db_province = models.Province(**province.dict())
    db.add(db_province)
    db.commit()
    return db_province

@router.put("/provinces/{province_id}", status_code=status.HTTP_200_OK, tags=["Provinces"])
async def update_province(province_id: int, province: ProvinceBase, db: db_dependency):
    db_province = db.query(models.Province).filter(models.Province.id == province_id).first()
    if db_province is None:
        raise HTTPException(status_code=404, detail="Province not found")

    # Actualizar los campos necesarios
    for var, value in vars(province).items():
        setattr(db_province, var, value) if value else None

    db.commit()
    return {"message": "Province updated successfully"}

@router.delete("/provinces/{province_id}", status_code=status.HTTP_200_OK, tags=["Provinces"])
async def delete_province(province_id: int, db:db_dependency):
    db_province = db.query(models.Province).filter(models.Province.id == province_id).first()
    if db_province is None:
        raise HTTPException(status_code=404, detail="Province not found")
    db.delete(db_province)
    db.commit()
    return {"message": "Province eliminated successfully"}




""" Cities """
@router.get("/cities", status_code=status.HTTP_200_OK, tags=["Cities"])
async def read_cities(db: db_dependency):
    cities = db.query(models.City).all()
    if not cities:
        raise HTTPException(status_code=404, detail="No cities found")
    return cities

@router.get("/cities/{city_id}", status_code=status.HTTP_200_OK, tags=["Cities"])
async def read_city(city_id: int, db: db_dependency):
    city = db.query(models.City).filter(models.City.id == city_id).first()
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city

@router.post("/cities", status_code=status.HTTP_201_CREATED, tags=["Cities"])
async def create_city(city: CityBase, db: db_dependency):
    db_city = models.City(**city.dict())
    db.add(db_city)
    db.commit()
    return db_city

@router.put("/cities/{city_id}", status_code=status.HTTP_200_OK, tags=["Cities"])
async def update_city(city_id: int, city: CityBase, db: db_dependency):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    # Actualizar los campos necesarios
    for var, value in vars(city).items():
        setattr(db_city, var, value) if value else None

    db.commit()
    return {"message": "Province updated successfully"}

@router.delete("/cities/{city_id}", status_code=status.HTTP_200_OK, tags=["Cities"])
async def delete_city(city_id: int, db:db_dependency):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    db.delete(db_city)
    db.commit()
    return {"message": "City eliminated successfully"}



""" Districts """
@router.get("/districts", status_code=status.HTTP_200_OK, tags=["Districts"])
async def read_districts(db: db_dependency):
    districts = db.query(models.District).all()
    if not districts:
        raise HTTPException(status_code=404, detail="No District found")
    return districts

@router.get("/districts/{district_id}", status_code=status.HTTP_200_OK, tags=["Districts"])
async def read_district(district_id: int, db: db_dependency):
    district = db.query(models.District).filter(models.District.id == district_id).first()
    if district is None:
        raise HTTPException(status_code=404, detail="District not found")
    return district

@router.post("/districts", status_code=status.HTTP_201_CREATED, tags=["Districts"])
async def create_district(district: DistrictBase, db: db_dependency):
    db_district = models.District(**district.dict())
    db.add(db_district)
    db.commit()
    return db_district

@router.put("/districts/{district_id}", status_code=status.HTTP_200_OK, tags=["Districts"])
async def update_district(district_id: int, district: DistrictBase, db: db_dependency):
    db_district = db.query(models.District).filter(models.District.id == district_id).first()
    if db_district is None:
        raise HTTPException(status_code=404, detail="City not found")

    # Actualizar los campos necesarios
    for var, value in vars(district).items():
        setattr(db_district, var, value) if value else None

    db.commit()
    return {"message": "District updated successfully"}

@router.delete("/districts/{district_id}", status_code=status.HTTP_200_OK, tags=["Districts"])
async def delete_district(district_id: int, db:db_dependency):
    db_district = db.query(models.District).filter(models.District.id == district_id).first()
    if db_district is None:
        raise HTTPException(status_code=404, detail="District not found")
    db.delete(db_district)
    db.commit()
    return {"message": "District eliminated successfully"}




""" Ubications """
@router.get("/ubications", status_code=status.HTTP_200_OK, tags=["Ubications"])
async def read_ubications(db: db_dependency):
    ubications = db.query(models.Ubication).all()
    if not ubications:
        raise HTTPException(status_code=404, detail="No Ubication found")
    return ubications

@router.get("/ubications/{ubication_id}", status_code=status.HTTP_200_OK, tags=["Ubications"])
async def read_ubication(ubication_id: int, db: db_dependency):
    ubication = db.query(models.Ubication).filter(models.Ubication.id == ubication_id).first()
    if ubication is None:
        raise HTTPException(status_code=404, detail="Ubication not found")
    return ubication

@router.post("/ubications", status_code=status.HTTP_201_CREATED, tags=["Ubications"])
async def create_ubication(ubication: UbicationBase, db: db_dependency):
    db_ubication = models.Ubication(**ubication.dict())
    db.add(db_ubication)
    db.commit()
    return db_ubication

@router.put("/ubications/{ubication_id}", status_code=status.HTTP_200_OK, tags=["Ubications"])
async def update_ubication(ubication_id: int, ubication: UbicationBase, db: db_dependency):
    db_ubication = db.query(models.Ubication).filter(models.Ubication.id == ubication_id).first()
    if db_ubication is None:
        raise HTTPException(status_code=404, detail="City not found")

    # Actualizar los campos necesarios
    for var, value in vars(ubication).items():
        setattr(db_ubication, var, value) if value else None

    db.commit()
    return {"message": "Ubication updated successfully"}

@router.delete("/ubications/{ubication_id}", status_code=status.HTTP_200_OK, tags=["Ubications"])
async def delete_ubication(ubication_id: int, db:db_dependency):
    db_ubication = db.query(models.Ubication).filter(models.Ubication.id == ubication_id).first()
    if db_ubication is None:
        raise HTTPException(status_code=404, detail="Ubication not found")
    db.delete(db_ubication)
    db.commit()
    return {"message": "Ubication eliminated successfully"}
