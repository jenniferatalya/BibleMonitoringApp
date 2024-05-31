from sqlalchemy import create_engine, text

engine = create_engine('mysql+mysqlconnector://root@localhost/monitoring_app')

connection = engine.connect()