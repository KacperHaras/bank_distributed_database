from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

engineMain = create_engine('mssql+pyodbc://Main:Main!23@DESKTOP-26ORVSE\SQLEXPRESS/Main?driver=ODBC+Driver+17+for+SQL+Server')
engine1 = create_engine('mssql+pyodbc://Node1:Node1!23@DESKTOP-26ORVSE\SQLEXPRESS/Branch1?driver=ODBC+Driver+17+for+SQL+Server')
engine2 = create_engine('mssql+pyodbc://Node2:Node2!23@DESKTOP-26ORVSE\SQLEXPRESS/Branch2?driver=ODBC+Driver+17+for+SQL+Server')

SessionMain = sessionmaker(bind=engineMain)
Session1 = sessionmaker(bind=engine1)
Session2 = sessionmaker(bind=engine2)

session_table = [SessionMain, Session1, Session2]

def init_db(app):
    db.init_app(app)