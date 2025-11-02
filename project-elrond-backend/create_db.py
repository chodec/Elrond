import os
import sys
from sqlalchemy.dialects import postgresql

#Add new tables
#1. run .venv
#2. run create_db.py

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))

import app.db.models 

from app.db.database import engine, Base
from app.db.models import Role, request_status_enum


print("Clear tables")

Base.metadata.drop_all(bind=engine) 

enum_type = postgresql.ENUM(Role, name='role_enum')

with engine.begin() as conn:
    print("Creating enums")
    enum_type.create(conn, checkfirst=True) 
    request_status_enum.create(conn, checkfirst=True)

print("Creating tables")
Base.metadata.create_all(bind=engine) 

print("Tables created")
