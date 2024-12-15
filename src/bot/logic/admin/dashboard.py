import asyncio

from datetime import datetime, timedelta

from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.cache import Cache
from src.db.database import Database
from src.bot.filters.admin_filter import AdminFilter
from src.bot.structures.keyboards import common
from src.bot.structures.fsm.admin import AdminGroup
from .router import admin_router


@admin_router.message(F.text=='/admin', AdminFilter())
async def process_admin_panel(
    message: Message, 
    state: FSMContext, 
    db: Database,
    cache: Cache
):
    await state.clear()
    await message.answer(
        "Admin panelga hush kelibsiz", 
        reply_markup=common.get_admin_menu()
    )


@admin_router.message(F.text=='👤 Statistika', AdminFilter())
async def process_admin_panel(
    message: Message, 
    state: FSMContext, 
    db: Database,
    cache: Cache
):
    now = datetime.now()
    user_count = len(await db.user.get_many())
    orders_by_day = len(await db.order.get_orders_by_day(now))
    orders_by_week = len(await db.order.get_orders_by_week(now - timedelta(days=datetime.now().weekday())))
    orders_by_month = len(await db.order.get_orders_by_month(now.year, now.month))

    msg = "Maxsulotlar sotuvi statistikasi:\n"
    msg += f"- Bugun sotilgan tovarlar soni: {orders_by_day}\n"
    msg += f"- Hafta davomida sotilgan tovarlar soni: {orders_by_week}\n"
    msg += f"- Oy davomida sotilgan tovarlar soni: {orders_by_month}\n\n"
    msg += f"Botda {user_count}-ta foydalanuvchi mavjud"

    await message.answer(msg)

@admin_router.message(F.text=='✍️ Habar yuborish', AdminFilter())
async def process_admin_panel(
    message: Message, 
    state: FSMContext, 
    db: Database,
    cache: Cache
):
    await message.answer("Habaringizni yuboring", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AdminGroup.broadcast)


@admin_router.message(AdminGroup.broadcast, AdminFilter())
async def process_admin_panel(
    message: Message, 
    state: FSMContext, 
    db: Database,
    cache: Cache
):
    users = await db.user.get_many()
    count = 0

    for user in users:
        try:
            await message.bot.send_message(
                chat_id=user.user_id,
                text = message.text
            )
            count += 1
        except Exception as e:
            print(e)
        
        await asyncio.sleep(0.5)
    
    await message.answer(f"Habar {count}-ta odamga jo'natildi", reply_markup=common.get_admin_menu())
    await state.clear()


@admin_router.message(F.text=="➕ Mahsulot qo'shish", AdminFilter())
async def process_admin_panel(
    message: Message, 
    state: FSMContext, 
    db: Database,
    cache: Cache
):
    await message.answer("Mahsulotni nomini kiriting", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AdminGroup.add_product)


@admin_router.message(AdminGroup.add_product, AdminFilter())
async def process_admin_panel(
    message: Message, 
    state: FSMContext, 
    db: Database,
    cache: Cache
):
    await state.set_data(dict(product_name=message.text))
    await message.answer("Mahsulotni narxini kiriting")
    await state.set_state(AdminGroup.add_price)


@admin_router.message(AdminGroup.add_price, AdminFilter())
async def process_admin_panel(
    message: Message, 
    state: FSMContext, 
    db: Database,
    cache: Cache
):
    if not message.text.isdigit():
        return message.answer("Iltimos faqat son ishlatgan holda mahsulotni narxini kiriting!")
    
    data = await state.get_data()
    product_name = data['product_name']
    product_price = int(message.text)

    await db.product.new(
        product_name=product_name,
        price=product_price
    )
    await message.answer("Maxsulot saqlandi ✅", reply_markup=common.get_admin_menu())
    await state.clear()


@admin_router.message(F.text=="➖ Mahsulot o'chirish", AdminFilter())
async def process_admin_panel(
    message: Message, 
    state: FSMContext, 
    db: Database,
    cache: Cache
):
    await message.answer("Maxsulotni nomini kiriting", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AdminGroup.delete_product)


@admin_router.message(AdminGroup.delete_product, AdminFilter())
async def process_admin_panel(
    message: Message, 
    state: FSMContext, 
    db: Database,
    cache: Cache
):
    product = await db.product.get_product(product_name=message.text)
    if not product:
        return await message.answer("Bunday maxsulot mavjud emas")
    
    await db.product.delete(product_id=product.id)
    await message.answer("Maxsulot o'chirildi ✅", reply_markup=common.get_admin_menu())
    await state.clear()


@admin_router.message(F.text=="💸 Min Summa", AdminFilter())
async def process_admin_panel(
    message: Message, 
    state: FSMContext, 
    db: Database,
    cache: Cache
):
    await message.answer("Tovar uchun minimal sonni kiriting")
    await state.set_state(AdminGroup.set_min_sum)


@admin_router.message(AdminGroup.set_min_sum, AdminFilter())
async def process_admin_panel(
    message: Message, 
    state: FSMContext, 
    db: Database,
    cache: Cache
):
    if not message.text.isdigit():
        return await message.answer("Iltimos son kiriting!")
    
    await cache.set("min_count", int(message.text))
    await message.answer("Yangilandi ✅", reply_markup=common.get_admin_menu())
    await state.clear()


@admin_router.message(F.users_shared, AdminFilter())
async def process_admin_panel(
    message: Message, 
    state: FSMContext, 
    db: Database,
    cache: Cache
):
    request_id = message.users_shared.request_id

    for user in message.users_shared.users:
        user_db = await db.user.get_me(user.user_id)
        if user_db:
            if request_id == 1:
                await db.user.update_user(user_db.user_id, is_blocked=True)
            elif request_id == 2:
                await db.user.update_user(user_db.user_id, is_blocked=False)
    
    banned_msg = "Foydalanuvchilar bloklandi!"
    unbanned_msg = "Foydalanuvchilar blokdan chiqarildi!"
    msg = banned_msg if request_id == 1 else unbanned_msg
    await message.answer(msg)


