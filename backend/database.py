from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# 環境変数や設定ファイルからDATABASE_URLを取得するのが理想ですが、まずは直書きでOK
DATABASE_URL = "postgresql://postgres:Supabase_1412.Kid@db.yfslwlwhnmkvkcuapqvs.supabase.co:5432/postgres" 

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 