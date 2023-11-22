from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#sqlite3 데이터베이스의 파일을 의미하며 프로젝트 루트 디렉터리에 저장
SQLALCHEMY_DATABASE_URL = "sqlite:///./Verfit.db" 

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

#autocommit=False이므로, commit이 없으면 저장되지 않음.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()