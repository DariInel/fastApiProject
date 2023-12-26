from typing import List

from sqlalchemy.orm import Session

import schemas
from models import Purchase, Buyer


def create_purchase(db: Session, schema: schemas.PurchaseCreate):
    db_purchase = Purchase(**schema.model_dump())
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase


def get_purchases(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Purchase).offset(skip).limit(limit).all()


def get_purchase(db: Session, id: int):
    return db.query(Purchase).filter_by(id=id).first()


def update_purchase_sum(db: Session, data: schemas.PurchaseUpdate | dict, id: int):
    purchase = db.query(Purchase).filter_by(id=id).first()

    if purchase:
        purchase.sum = data.sum
        db.commit()
        db.refresh(purchase)
        return True

    return False


def delete_purchase(db: Session, id: int):
    purchase = db.query(Purchase).filter_by(id=id).first()
    if purchase:
        db.delete(purchase)
        db.commit()
        return True
    return False


def add_purchase(db: Session, data: schemas.PurchaseBase | dict, data_buyer_id: int):
    purchase = Purchase(sum=data.sum, buyer_id=data_buyer_id)
    db.add(purchase)
    db.commit()
    db.refresh(purchase)
    return True


def get_buyers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Buyer).offset(skip).limit(limit).all()


def get_buyer(db: Session, id: int):
    return db.query(Buyer).filter_by(id=id).first()


def update_buyer_number(db: Session, data: schemas.BuyerUpdate, id: int):
    buyer = db.query(Buyer).filter_by(id=id).first()

    if buyer:
        buyer.number = data.number
        db.commit()
        db.refresh(buyer)

        return True

    return False


def delete_buyer(db: Session, id: int):
    buyer = db.query(Buyer).filter_by(id=id).first()
    if buyer:
        db.delete(buyer)
        db.commit()
        return True
    return False


def add_buyer(db: Session, data: schemas.BuyerBase | dict):
    buyer = Buyer(name=data.name, surname=data.surname, number=data.number)
    db.add(buyer)
    db.commit()
    db.refresh(buyer)
    return True