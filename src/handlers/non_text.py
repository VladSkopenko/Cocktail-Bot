from random import choice

from aiogram import F
from aiogram import Router
from aiogram import types

from src.common.sticks_id import STICKERS
from src.utils.save_contact import save_contact

non_text_router = Router()


@non_text_router.message(F.photo)
async def photo_cmd(message: types.Message):
    await message.answer("Фото чудове, поділись ще одним будь ласка")


@non_text_router.message(F.sticker)
async def sticker_cmd(message: types.Message):
    await message.answer_sticker(sticker=choice(STICKERS))


@non_text_router.message(F.location)
async def location_cmd(message: types.Message):
    await message.answer("Неймовірно, це тайм-сквер?")


@non_text_router.message(F.contact)
async def contact_cmd(message: types.Message):
    contact = message.contact
    save_contact(contact.user_id,
                 contact.first_name,
                 contact.phone_number
                 )

    await message.answer("Дякую що поділились контактом ")



@non_text_router.message(F.voice)
async def voice_cmd(message: types.Message):
    await message.answer("У вас дуже приємний голос")


@non_text_router.message(F.video_note)
async def video_cmd(message: types.Message):
    await message.answer("Вау, Ви режисер? ?")
