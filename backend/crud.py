from sqlalchemy.orm import Session
from . import models, schemas
from .auth import get_password_hash

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    if user_update.email is not None:
        db_user.email = user_update.email
    if user_update.usage_count is not None:
        db_user.usage_count = user_update.usage_count
    if user_update.password is not None:
        db_user.password_hash = get_password_hash(user_update.password)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_orders_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Order).filter(models.Order.user_id == user_id).order_by(models.Order.created_at.desc()).offset(skip).limit(limit).all()

def create_order(db: Session, order: schemas.OrderBase, user_id: int):
    db_order = models.Order(
        user_id=user_id,
        out_trade_no=order.out_trade_no,
        amount=order.amount,
        remark=order.remark
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_admin_by_username(db: Session, username: str):
    return db.query(models.Admin).filter(models.Admin.username == username).first()

def create_admin(db: Session, username: str, password: str):
    db_admin = models.Admin(
        username=username,
        password_hash=get_password_hash(password)
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin 