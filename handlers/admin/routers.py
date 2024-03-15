from aiogram import Router

from .catalog import router as catalog_router
from .main import router as main_router
from .product import router as product_router

admin_router = Router()

admin_router.include_router(main_router)
admin_router.include_router(catalog_router)
admin_router.include_router(product_router)

