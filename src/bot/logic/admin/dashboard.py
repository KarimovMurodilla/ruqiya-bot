import asyncio

from datetime import datetime, timedelta
from collections import defaultdict

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

    orders_by_day = await db.order.get_orders_by_day(now)
    orders_by_week = await db.order.get_orders_by_week(now - timedelta(days=datetime.now().weekday()))
    orders_by_month = await db.order.get_orders_by_month(now.year, now.month)

    orders_by_day_sum = sum([obj.total_price for obj in orders_by_day])
    orders_by_week_sum = sum([obj.total_price for obj in orders_by_week])
    orders_by_month_sum = sum([obj.total_price for obj in orders_by_month])

    formatted_price_by_day = "{:,}".format(orders_by_day_sum)
    formatted_price_by_week = "{:,}".format(orders_by_week_sum)
    formatted_price_by_month = "{:,}".format(orders_by_month_sum)

    data_by_day = defaultdict(int)
    for obj in orders_by_day:
        data_by_day[obj.product_name] += obj.total_count

    data_by_week = defaultdict(int)
    for obj in orders_by_day:
        data_by_week[obj.product_name] += obj.total_count

    data_by_month = defaultdict(int)
    for obj in orders_by_day:
        data_by_month[obj.product_name] += obj.total_count

    msg = "💸 Maxsulotlar sotuv summasi statistikasi:\n"
    msg += f"- Bugun sotilgan tovarlar summasi: {formatted_price_by_day}\n"
    msg += f"- Hafta davomida sotilgan tovarlar summasi: {formatted_price_by_week}\n"
    msg += f"- Oy davomida sotilgan tovarlar summasi: {formatted_price_by_month}\n\n"

    msg += "🧮 Maxsulotlar sotuv soni statistikasi:\n\n"
    msg += f"📅 Bugun sotilgan maxsulotlar soni:\n"
    for product, count in data_by_day.items():
        msg += f"- {product}: {count} dona\n"
    msg += "\n"

    msg += f"📅 Hafta davomida sotilgan maxsulotlar soni:\n"
    for product, count in data_by_week.items():
        msg += f"- {product}: {count} dona\n"
    msg += "\n"

    msg += f"📅 Oy davomida sotilgan maxsulotlar soni:\n"
    for product, count in data_by_month.items():
        msg += f"- {product}: {count} dona\n"
    msg += "\n\n"

    msg += f"👤 Botda {user_count}-ta foydalanuvchi mavjud"

    await message.answer(msg)


@admin_router.message(F.text=='👤 Kuryerlar statistikasi', AdminFilter())
async def process_admin_panel(
    message: Message, 
    db: Database,
):
    employee_stats = defaultdict(lambda: defaultdict(int))

    data = await db.approved_order.get_approved_order_with_joined_data()

    for obj in data:
        for item in obj.order.order_items:
            employee_stats[f"{obj.user.full_name}, {obj.user.phone_number}"][item.product_name] += item.total_count

    msg = "Kuryerlar statistikasi:\n\n"
    for employee, products in employee_stats.items():
        msg += f"{employee}:\n"
        for product, count in products.items():
            msg += f"  - {product}: {count} dona\n"
        msg += "\n"

    await message.answer(msg, reply_markup=common.set_status_checked())


@admin_router.callback_query(F.data=='set_status_checked', AdminFilter())
async def process_admin_panel(c: CallbackQuery, db: Database):
    await db.approved_order.set_status_checked()
    await c.message.edit_text("Tozalandi ✅")


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
    await message.answer("Tovar uchun minimal narxni kiriting")
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
    
    await cache.set("min_sum", int(message.text))
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


