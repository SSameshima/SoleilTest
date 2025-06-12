from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime

# データベースURLの設定
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/location_db')

# エンジンの作成
engine = create_engine(DATABASE_URL)

# セッションの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ベースクラスの作成
Base = declarative_base()

class Location(Base):
    __tablename__ = "locations"

    place_pos = Column(String, primary_key=True)
    count_person = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'place_pos': self.place_pos,
            'count_person': self.count_person,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }

# データベースの初期化
def init_db():
    Base.metadata.create_all(bind=engine)

# データベースセッションの取得
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 