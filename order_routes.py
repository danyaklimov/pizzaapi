from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT

from database import engine, Session
from models import User, Order
from schemas import OrderModel, OrderStatusModel

session = Session(bind=engine)

order_router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)

@order_router.get('/')
async def hello(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    return {"message": "Hello world"}

@order_router.post('/order', status_code=status.HTTP_201_CREATED)
async def place_an_order(order: OrderModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    new_order = Order(
        pizza_size=order.pizza_size,
        quantity=order.quantity,
        flavour=order.flavour,
        order_status=order.order_status
    )
    new_order.user = user

    session.add(new_order)
    session.commit()

    response = {
        "pizza_size": new_order.pizza_size,
        "flavour": new_order.flavour,
        "quantity": new_order.quantity,
        "id": new_order.id,
        "user": new_order.user
    }

    return jsonable_encoder(response)

@order_router.get('/orders')
async def list_all_orders(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()

    if user.is_staff:
        orders = session.query(Order).all()
        return jsonable_encoder(orders)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not a superuser")

@order_router.get('/orders/{order_id}')
async def get_order_by_id(order_id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()

    if user.is_staff:
        order = session.query(Order).filter(Order.id == order_id).first()
        return jsonable_encoder(order)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not a superuser")

@order_router.get('/user/orders')
async def get_current_user_orders(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    orders = session.query(Order).filter(Order.user_id == user.id).all()

    return jsonable_encoder(orders)

@order_router.get('/user/order/{order_id}')
async def get_current_user_specific_order(order_id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    order = session.query(Order).filter(Order.id == order_id, Order.user_id == user.id).first()

    response = {
        "id": order.id,
        "order_status": order.order_status,
        "quantity": order.quantity,
        "flavour": order.flavour,
        "user_id": order.user_id
    }

    return jsonable_encoder(order)

@order_router.put('/order/update/{order_id}')
async def update_order(order_id: int, order: OrderModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    order_to_update = session.query(Order).filter(Order.id == order_id).first()
    order_to_update.quantity = order.quantity
    order_to_update.pizza_size = order.pizza_size
    order_to_update.flavour = order.flavour

    session.commit()

    result = session.query(Order).filter(Order.id == order_id).first()
    response = {
        "id": result.id,
        "order_status": result.order_status,
        "quantity": result.quantity,
        "flavour": result.flavour,
        "user_id": result.user_id
    }

    return jsonable_encoder(response)

@order_router.patch('/order/status/{order_id}')
async def update_order_status(order_id: int, order: OrderStatusModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    username = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == username).first()
    if not current_user.is_staff:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not a superuser")

    order_to_update = session.query(Order).filter(Order.id == order_id).first()
    order_to_update.order_status = order.order_status

    session.commit()

    result = session.query(Order).filter(Order.id == order_id).first()
    response = {
        "id": result.id,
        "order_status": result.order_status,
        "quantity": result.quantity,
        "flavour": result.flavour,
        "user_id": result.user_id
    }
    return jsonable_encoder(response)

@order_router.delete('/order/delete/{order_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_an_order(order_id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    order_to_delete = session.query(Order).filter(Order.id == order_id).first()
    session.delete(order_to_delete)
    session.commit()

    return order_to_delete
