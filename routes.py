from typing import List

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

import schemas
from controllers import get_purchases, get_purchase, add_purchase, get_buyers, get_buyer, add_buyer, \
    update_buyer_number, delete_buyer, update_purchase_sum, delete_purchase
from database import get_db

router_purchase = APIRouter(prefix='/purchase', tags=['item'])
router_buyer = APIRouter(prefix='/buyer', tags=['buyer'])
router_websocket = APIRouter()


connected_clients = set()


async def send_notify(notify: str):
    for client in connected_clients:
        await client.send_text(notify)


@router_websocket.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    await send_notify("New client")
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        await websocket.close()


@router_purchase.get("/",  response_model=List[schemas.Purchase])
async def get_purchases_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    purchases = get_purchases(db, skip=skip, limit=limit)
    await send_notify(f"All purchases")
    return purchases


@router_purchase.get("/{id}", response_model=schemas.Purchase)
async def get_purchase_id(id: int, db: Session = Depends(get_db)):
    await send_notify(f"Purchase with id: {id}")
    return get_purchase(db, id)


@router_purchase.post("/{buyer_id}/add")
async def add_purchase_id(buyer_id: int, purchase: schemas.PurchaseBase, db: Session = Depends(get_db)):
    flag = add_purchase(db, purchase, buyer_id)
    if flag:
        await send_notify(f"New purchase add with sum: {purchase.sum}")
        return "Successfully"
    return "No successfully :("


@router_purchase.put("/{purchase_id}/update")
async def update_purchase_sum_(purchase_id: int, purchase: schemas.PurchaseUpdate, db: Session = Depends(get_db)):
    flag = update_purchase_sum(db, purchase, purchase_id)
    if flag:
        await send_notify(f"Sum of purchase update: {purchase.sum}")
        return "Successfully"
    return "No successfully :("


@router_purchase.delete("/{purchase_id}/delete")
async def delete_purchase_id(purchase_id: int, db: Session = Depends(get_db)):
    flag = delete_purchase(db, purchase_id)
    if flag:
        await send_notify(f"Delete purchase with id: {id}")
        return "Successfully"
    return "No successfully :("


@router_buyer.get("/",  response_model=List[schemas.Buyer])
async def get_buyers_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    buyers = get_buyers(db, skip=skip, limit=limit)
    await send_notify(f"All buyers")
    return buyers


@router_buyer.get("/{id}", response_model=schemas.Buyer)
async def get_buyer_id(id: int, db: Session = Depends(get_db)):
    await send_notify(f"Buyer with id: {id}")
    return get_buyer(db, id)


@router_buyer.post("/add")
async def add_buyer_(buyer: schemas.BuyerBase, db: Session = Depends(get_db)):
    flag = add_buyer(db, buyer)
    if flag:
        await send_notify(f"New buyer add")
        return "Successfully"
    return "No successfully :("


@router_buyer.put("/{buyer_id}/update")
async def update_buyer_number_(buyer_id: int, buyer: schemas.BuyerUpdate, db: Session = Depends(get_db)):
    flag = update_buyer_number(db, buyer, buyer_id)
    if flag:
        await send_notify(f"Number of buyer update: {buyer.number}")
        return "Successfully"
    return "No successfully :("


@router_buyer.delete("/{buyer_id}/delete")
async def delete_buyer_id(buyer_id: int, db: Session = Depends(get_db)):
    flag = delete_buyer(db, buyer_id)
    if flag:
        await send_notify(f"Delete buyer with id: {id}")
        return "Successfully"
    return "No successfully :("
