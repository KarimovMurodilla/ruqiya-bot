from typing import List, Tuple

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from src.bot.utils.messages import default_languages, regions


def get_languages(flag="lang"):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="O‘zbek 🇺🇿", callback_data=f"{flag}_uz"),
         InlineKeyboardButton(text="Кирилл 🇺🇿", callback_data=f"{flag}_ru")],
    ])
    return keyboard


def get_main_menu(user_lang: str):
    main_menu_keyboard = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text=default_languages[user_lang]['categories']),
            KeyboardButton(text=default_languages[user_lang]['contact_us'])
        ],
        [
            KeyboardButton(text=default_languages[user_lang]['my_orders']),
            KeyboardButton(text=default_languages[user_lang]['settings'])
        ],
        [
            KeyboardButton(text=default_languages[user_lang]['cart'])
        ]

    ], resize_keyboard=True)
    return main_menu_keyboard


def get_admin_menu(user_lang):
    admin_menu_keyboard = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text="👤Statistika"),
            KeyboardButton(text="✍️ Habar yuborish")
        ],
        [
            KeyboardButton(text="➕ Mahsulot qo'shish"),
            KeyboardButton(text="➖ Mahsulot o'chirish")
        ],
        [
            KeyboardButton(text="💸 Min Summa"),
            KeyboardButton(text="🚫 Foydalanuvchini bloklash")
        ],
        [
            KeyboardButton(text="🚫 Foydalanuvchini blokdan ochish")
        ]
    ], resize_keyboard=True)
    return admin_menu_keyboard


def get_phone_number(user_lang: str):
    main_menu_keyboard = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text=default_languages[user_lang]['send_number'], request_contact=True)
        ]
    ], resize_keyboard=True )
    return main_menu_keyboard


def get_location(user_lang: str = None):
    main_menu_keyboard = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text="Lokatsiyani jo'natish", request_location=True)
        ]
    ], resize_keyboard=True )
    return main_menu_keyboard

def show_products(data: List[Tuple]):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=data[i][0], callback_data=str(data[i][1])) 
        ]
        for i in range(len(data))
    ])
    return keyboard


def make_order_or_back(user_lang: str):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=default_languages[user_lang]["place_order"], callback_data="place_order") 
        ],
        [
            InlineKeyboardButton(text=default_languages[user_lang]["back"], callback_data="back") 
        ],  
    ])
    return keyboard


def show_regions():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=region, callback_data=region)
        ]
        for region in regions 
    ])
    return keyboard


def show_distincts(region: str):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=district, callback_data=district) 
        ]
        for district in regions[region]
    ])
    return keyboard


def show_settings():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Tilni o'zgartirish", callback_data="change_lang"),
        ],
        [
            InlineKeyboardButton(text="Telefon raqamini o'zgartirish", callback_data="change_phone_number"),
        ],
        [
            InlineKeyboardButton(text="To'liq ismni o'zgartirish", callback_data="change_name"),
        ]
    ])

    return keyboard
