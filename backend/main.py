from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
import os

from . import models, schemas, crud, auth, database

app = FastAPI()

# 初始化数据库
@app.on_event("startup")
def on_startup():
    database.init_db()

# 静态文件（管理前端）
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

@app.get("/admin", response_class=HTMLResponse)
def admin_page():
    return FileResponse(os.path.join(os.path.dirname(__file__), "static", "admin.html"))

# 管理员登录
@app.post("/admin/login")
def admin_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(auth.get_db)):
    admin = crud.get_admin_by_username(db, form_data.username)
    if not admin or not auth.verify_password(form_data.password, admin.password_hash):
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    access_token = auth.create_access_token(data={"sub": admin.username})
    return {"access_token": access_token, "token_type": "bearer"}

# 用户管理接口
@app.get("/admin/users", response_model=List[schemas.UserOut])
def list_users(skip: int = 0, limit: int = 100, current_admin: models.Admin = Depends(auth.get_current_admin), db: Session = Depends(auth.get_db)):
    return crud.get_users(db, skip=skip, limit=limit)

@app.get("/admin/user/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, current_admin: models.Admin = Depends(auth.get_current_admin), db: Session = Depends(auth.get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user

@app.put("/admin/user/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: int, user_update: schemas.UserUpdate, current_admin: models.Admin = Depends(auth.get_current_admin), db: Session = Depends(auth.get_db)):
    user = crud.update_user(db, user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user

# 用户订单管理
@app.get("/admin/user/{user_id}/orders", response_model=List[schemas.OrderOut])
def get_user_orders(user_id: int, skip: int = 0, limit: int = 100, current_admin: models.Admin = Depends(auth.get_current_admin), db: Session = Depends(auth.get_db)):
    return crud.get_orders_by_user(db, user_id, skip=skip, limit=limit) 