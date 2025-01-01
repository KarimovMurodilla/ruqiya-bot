from typing import List, Tuple

from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, 
    KeyboardButton, KeyboardButtonRequestUsers
)
from src.bot.utils.messages import default_languages, regions, translate_region
from src.bot.utils.transliterate import transliterate


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


def get_admin_menu(user_lang: str = 'LATIN'):
    admin_menu_keyboard = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text="👤 Statistika"),
            KeyboardButton(text="✍️ Habar yuborish")
        ],
        [
            KeyboardButton(text="➕ Mahsulot qo'shish"),
            KeyboardButton(text="➖ Mahsulot o'chirish")
        ],
        [
            KeyboardButton(text="💸 Min Summa"),
            KeyboardButton(text="🚫 Foydalanuvchini bloklash", request_users=KeyboardButtonRequestUsers(
                    request_id=1, user_is_bot=False, request_username=True, request_name=True, max_quantity=10
                )
            )
        ],
        [
            KeyboardButton(text="👤 Kuryerlar statistikasi"),
        ],
        [
            KeyboardButton(text="🚫 Foydalanuvchini blokdan ochish", request_users=KeyboardButtonRequestUsers(
                    request_id=2, user_is_bot=False, request_username=True, request_name=True, max_quantity=10
                )
            )
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
            KeyboardButton(text=transliterate("Lokatsiyani jo'natish", user_lang), request_location=True)
        ]
    ], resize_keyboard=True )
    return main_menu_keyboard

def show_products(data: List[Tuple], user_lang: str):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=transliterate(data[i][0], user_lang), callback_data=str(data[i][1])) 
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


def show_regions(user_lang: str):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=translate_region(region, user_lang), callback_data=region)
            for region in regions
        ][n:n+3]
        for n in range(0, len(regions), 3)
    ])
    return keyboard


def show_distincts(region: str, user_lang: str):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=translate_region(district, user_lang), callback_data=district)
            for district in regions[region]
        ][n:n+3]
        for n in range(0, len(regions), 3)
    ])
    return keyboard


def show_settings(user_lang: str):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=transliterate("Tilni o'zgartirish", user_lang), callback_data="change_lang"),
        ],
        [
            InlineKeyboardButton(text=transliterate("Telefon raqamini o'zgartirish", user_lang), callback_data="change_phone_number"),
        ],
        [
            InlineKeyboardButton(text=transliterate("To'liq ismni o'zgartirish", user_lang), callback_data="change_name"),
        ]
    ])

    return keyboard


def get_order(order_id: int):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📥 Buyurtmani olish", callback_data=f"get_order {order_id}"),
        ]
    ])

    return keyboard


def order_complete(user_id: int, order_id: int):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Yetkazib berdim", callback_data=f"order_complete {user_id} {order_id}"),
        ]
    ])

    return keyboard


def make_order(user_lang: str):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=transliterate("Buyurtma berish", user_lang), callback_data="make_order"),
        ]
    ])

    return keyboard


def set_status_checked():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Tozalash", callback_data="set_status_checked") 
        ]
    ])
    return keyboard

