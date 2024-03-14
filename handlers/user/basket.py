from aiogram import types, F, Router


router = Router()


@router.message(F.text == 'Корзина')
async def basket(message: types.Message):
    pass

