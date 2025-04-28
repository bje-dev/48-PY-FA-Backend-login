from sqlalchemy import Table, Column, Integer, String, MetaData, Boolean
from config.db import engine

metadata = MetaData()

users = Table("users", metadata,
    Column("id", Integer, primary_key=True),
              Column("name", String(255)),
              Column("surname", String(255)),
              Column("email", String(255)),
              Column("alias", String(255)),
              Column("password", String(255)),
              Column("agree", Boolean))

metadata.create_all(engine)
