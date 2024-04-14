from random import choice

from aiogram import Router
import os
from aiogram import types
from aiogram import F
from src.common.sticks_id import STICKERS
non_text_router = Router()


@non_text_router.message(F.photo)
async def photo_cmd(message: types.Message):
    await message.answer("Фото чудове, поділись ще одним будь ласка")


@non_text_router.message(F.sticker)
async def sticker_cmd(message: types.Message):
    await message.answer_sticker(sticker=choice(STICKERS))


@non_text_router.message(F.location)
async def location_cmd(message: types.Message):
    await message.answer("Реакція на повідомлення з локацією")


@non_text_router.message(F.contact)
async def contact_cmd(message: types.Message):
    await message.answer("Спасибі за контакт")


@non_text_router.message(F.photo)
async def photo_cmd(message: types.Message):
    await message.answer("Фото чудове, поділись ще одним будь ласка")


@non_text_router.message(F.sticker)
async def sticker_cmd(message: types.Message):
    await message.answer("Стікер у відповідь")


@non_text_router.message(F.voice)
async def voice_cmd(message: types.Message):
    await message.answer("Реакція на голосове повідомлення")


@non_text_router.message(F.video_note)
async def video_cmd(message: types.Message):
    await message.answer("Спасибі за контакт")
