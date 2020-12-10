from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t

from . import models, schemas
from app.core.security import get_password_hash


def get_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_user_by_email(db: Session, email: str) -> schemas.UserBase:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(
    db: Session, skip: int = 0, limit: int = 100
) -> t.List[schemas.UserOut]:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return user


def edit_user(
    db: Session,
    user_id: int,
    user: t.Union[schemas.UserEdit, schemas.UserAdmin],
) -> schemas.User:
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    update_data = user.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(user.password)
        del update_data["password"]

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_item(db: Session, item_id: int):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


def get_items(db: Session, skip: int = 0, limit: int = 100
              ) -> list[schemas.Item]:
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(
        name=item.name,
        description=item.description,
        volume=item.volume,
        price=item.price,
        local_id=item.local_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int):
    item = get_item(db, item_id)
    db.delete(item)
    db.commit()
    return item


def edit_item(db: Session, item_id: int, item: schemas.ItemCreate
              ) -> schemas.Item:
    db_item = get_item(db, item_id)
    update_data = item.dict(exclude_unset=True)

    for k, v in update_data.items():
        setattr(db_item, k, v)

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_local(db: Session, local_id: int):
    local = db.query(models.Local).filter(models.Local.id == local_id).first()
    if not local:
        raise HTTPException(status_code=404, detail="Item not found")
    return local


def get_locals(db: Session, skip: int = 0, limit: int = 100
               ) -> list[schemas.Local]:
    return db.query(models.Local).offset(skip).limit(limit).all()


def create_local(db: Session, local: schemas.LocalCreate):
    db_local = models.Local(
        volume=local.volume,
        coordinate=local.coordinate
    )
    db.add(db_local)
    db.commit()
    db.refresh(db_local)
    return db_local


def delete_local(db: Session, local_id: int):
    local = get_local(db, local_id)
    db.delete(local)
    db.commit()
    return local


def edit_local(db: Session, local_id: int, local: schemas.LocalCreate
               ) -> schemas.Local:
    db_local = get_local(db, local_id)
    update_data = local.dict(exclude_unset=True)

    for k, v in update_data.items():
        setattr(db_local, k, v)

    db.add(db_local)
    db.commit()
    db.refresh(db_local)
    return db_local
