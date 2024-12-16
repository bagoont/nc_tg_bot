from aiogram import Router, filters, types

router = Router(name="common")


@router.message(filters.CommandStart())
async def start(message: types.Message) -> None:
    await message.answer("Welcome!")
