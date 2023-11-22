from passlib.context import CryptContext
from sqlalchemy.orm import Session
from domain.accounts.accounts_schema import UserCreate, AdminCreate
from models import User, Admin


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#user
def create_user(db: Session, user_create: UserCreate):
    db_user = User(username=user_create.username,
                   password=pwd_context.hash(user_create.password1),
                   email=user_create.useremail)
    db.add(db_user)
    db.commit()

def get_existing_user(db: Session, user_create: UserCreate):
    return db.query(User).filter(
        (User.email == user_create.useremail)
    ).first()

def get_user(db: Session, email: str):
    return db.query(User).filter(User.email== email).first()

#admin
def create_admin(db: Session, admin_create: AdminCreate):
    db_admin = Admin(password=pwd_context.hash(admin_create.password1),
                   email=admin_create.adminemail)
    db.add(db_admin)
    db.commit()

def get_existing_admin(db: Session, admin_create: AdminCreate):
    return db.query(Admin).filter(
        (Admin.email == admin_create.adminemail)
    ).first()

def get_admin(db: Session, email: str):
    return db.query(Admin).filter(Admin.email== email).first()