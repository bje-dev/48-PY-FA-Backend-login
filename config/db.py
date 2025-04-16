from sqlalchemy import create_engine

engine = create_engine("mariadb+pymysql://cyrax:rjfwtpd7gj@localhost:3306/acceso")
conn = engine.connect()
