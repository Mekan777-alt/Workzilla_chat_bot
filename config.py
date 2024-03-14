import os
from dotenv import load_dotenv
from data.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage


load_dotenv()

bot = Bot(token=os.getenv('TOKEN'))

engine = create_engine('sqlite:///database.sqlite', echo=False)
Base.metadata.create_all(engine)
db_session = Session(bind=engine)

dp = Dispatcher(bot=bot, storage=MemoryStorage())
