from aiogram import Router
from .main import router as main_router
from .order import router as order_router
from .catalog import router as catalog_router
from .basket import router as basket_router

user_router = Router()


user_router.include_router(main_router)
user_router.include_router(order_router)
user_router.include_router(catalog_router)
user_router.include_router(basket_router)

