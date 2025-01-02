"""This file represents a start logic."""

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart

from src.cache import Cache
from src.db.database import Database
from src.bot.structures.keyboards import common
from src.bot.structures.fsm.registration import RegisterGroup
from src.language.translator import LocalizedTranslator
from src.bot.utils.messages import default_languages, introduction_template, check_phone, fix_phone
from src.bot.filters.user_filter import UserFilter

start_router = Router(name='start')
start_router.message.filter(UserFilter())


@start_router.message(CommandStart())
async def start_handler(message: types.Message, db: Database, state: FSMContext):
    """Start command handler."""
    await state.clear()

    user = await db.user.get_me(message.from_user.id)

    if not user:
        await message.answer_photo(
            "AgACAgIAAxkBAAIS-GddHv939Sv1blKDHWMjtn57WHL_AAKp7DEbPPIwSkjvRmUFSUNcAQADAgADeQADNgQ",
            caption=default_languages['welcome_message'],
            reply_markup=common.get_languages()
        )
        await state.set_state(RegisterGroup.lang) 
    else:
        # await message.answer_photo(
        #     "AgACAgIAAxkBAAITF2ddPJ7fa2j3Du7Ny7WR-TsgxzT_AAJD7DEbPPIwSqi6-T75nSkRAQADAgADeQADNgQ",
        #     caption=introduction_template[user.language_code.value.upper()],
        #     reply_markup=common.get_main_menu(user.language_code.value.upper())
        # )
        await message.answer("Assalomu aleykum")

@start_router.callback_query(RegisterGroup.lang)
async def get_lang(c: types.CallbackQuery, state: FSMContext):
    await c.answer()

    match c.data:
        case 'lang_uz': await state.set_data(dict(language='LATIN'))
        case 'lang_ru': await state.set_data(dict(language='CYRILLIC'))
    
    data = await state.get_data()
    lang = data.get('language')
    await c.message.answer(default_languages[lang]['full_name'])

    await state.set_state(RegisterGroup.fullname)

@start_router.message(RegisterGroup.fullname)
async def get_fullname(message: types.Message, state: FSMContext):
    await state.update_data(dict(fullname=message.text))

    data = await state.get_data()
    lang = data.get('language')
    await message.answer(
        default_languages[lang]['contact'], 
        reply_markup=common.get_phone_number(user_lang=lang)
    )
    await state.set_state(RegisterGroup.phone_number)

@start_router.message(F.contact | F.text, RegisterGroup.phone_number)
async def get_phone_number(message: types.Message, db: Database, cache: Cache, state: FSMContext):
    data = await state.get_data()
    lang = data.get('language')
    fullname = data.get('fullname')

    if message.contact:
        phone_number = message.contact.phone_number

    elif message.text:
        if check_phone(message.text):
            phone_number = message.text
        else:
            return await message.answer(default_languages[lang]['sorry'])

    await db.user.new(
        user_id=message.from_user.id,
        user_name=message.from_user.username,
        full_name=fullname,
        phone_number=fix_phone(phone_number),
        language=lang
    )
    
    await message.answer(
        default_languages[lang]['successful_registration'],
        reply_markup=common.get_main_menu(user_lang=lang)
    )

    k = f'lang_{message.from_user.id}'
    await cache.set(k, lang)
    
    await state.clear()

@start_router.message(F.photo)
async def receive_photo(message: types.Message, db: Database, translator: LocalizedTranslator, state: FSMContext):
    print(message.photo[-1].file_id)
