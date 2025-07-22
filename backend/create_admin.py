import sys
from backend.database import SessionLocal, init_db
from backend.models import Admin
from backend.auth import get_password_hash

def main():
    username = sys.argv[1] if len(sys.argv) > 1 else "admin"
    password = sys.argv[2] if len(sys.argv) > 2 else "333910Q333910"
    db = SessionLocal()
    init_db()
    if db.query(Admin).filter(Admin.username == username).first():
        print(f"管理员 {username} 已存在")
        db.close()
        return
    admin = Admin(username=username, password_hash=get_password_hash(password))
    db.add(admin)
    db.commit()
    db.close()
    print(f"管理员账号创建成功！用户名: {username}  密码: {password}")

if __name__ == "__main__":
    main() 