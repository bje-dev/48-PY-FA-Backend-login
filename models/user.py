from sqlalchemy import Table, Column, Integer, String, MetaData
from config.db import engine

metadata = MetaData()

users = Table("users", metadata,
    Column("id", Integer, primary_key=True),
              Column("name", String(255)),
              Column("email", String(255)),
              Column("password", String(255)))

metadata.create_all(engine)
