import re

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from src.cache import Cache
from src.db.database import Database
from src.bot.structures.keyboards import common
from src.bot.structures.fsm.order import OrderGroup
from src.bot.structures.fsm.registration import RegisterGroup
from src.bot.utils.messages import default_languages, check_phone, get_product_info
from src.bot.utils.transliterate import transliterate
from src.bot.filters.user_filter import UserFilter
from src.configuration import conf

commands_router = Router(name='commands')
commands_router.message.filter(UserFilter())


@commands_router.message(F.text.in_({'✅ Buyurtma berish', '✅ Буюртма бериш'}))
async def order_handler(message: types.Message, cache: Cache, db: Database, state: FSMContext):
    k = f'lang_{message.from_user.id}'
    lang = await cache.get(k)
    lang = lang.decode()

    products = await db.product.get_all_products()
    products = [(obj.product_name, obj.id) for obj in products]

    await message.answer(
        default_languages[lang]['category_select'],
        reply_markup=common.show_products(data=products, user_lang=lang)
    )

    await state.set_state(OrderGroup.get_product)


@commands_router.callback_query(OrderGroup.get_product)
async def show_product_info(c: types.CallbackQuery, cache: Cache, db: Database, state: FSMContext):
    await c.answer()

    product = await db.product.get(int(c.data))
    
    k = f'lang_{c.from_user.id}'
    lang = await cache.get(k)
    lang = lang.decode()

    number = product.price
    formatted_number = "{:,}".format(int(number))

    await state.set_data(
        dict(
            product_id=c.data,
            product_price=int(product.price)
        )
    )

    msg = get_product_info(lang, transliterate(product.product_name, lang), formatted_number)
    await c.message.edit_text(msg, reply_markup=common.make_order_or_back(lang))
    await state.set_state(OrderGroup.to_order)

@commands_router.callback_query(OrderGroup.to_order)
async def show_product_info(c: types.CallbackQuery, cache: Cache, db: Database, state: FSMContext):
    k = f'lang_{c.from_user.id}'
    lang = await cache.get(k)
    lang = lang.decode()

    await c.answer()

    if c.data == 'place_order':
        await c.message.answer(
            default_languages[lang]['products_quantity_enter'],
            reply_markup=types.ReplyKeyboardRemove()
        )
        await state.set_state(OrderGroup.get_count)
    else:
        products = await db.product.get_all_products()
        products = [(obj.product_name, obj.id) for obj in products]

        await c.message.edit_text(
            default_languages[lang]['category_select'],
            reply_markup=common.show_products(data=products, user_lang=lang)
        )

        await state.set_state(OrderGroup.get_product)

@commands_router.message(OrderGroup.get_count)
async def get_count_handler(message: types.Message, cache: Cache, db: Database, state: FSMContext):
    data = await state.get_data()
    product_id = int(data.get('product_id'))
    product_price = int(data.get('product_price'))
    # min_count = await cache.get("min_count")
    match = re.search(r'\d+', message.text)

    # if min_count:
    #     product_min_count = int(min_count.decode())
    # else:
    #     product_min_count = 2

    k = f'lang_{message.from_user.id}'
    lang = await cache.get(k)
    lang = lang.decode()

    if match:
        count = int(match.group())
        # if count >= product_min_count:
        await db.cart.new(
            user_id=message.from_user.id,
            product_id=product_id,
            total_price=product_price * count,
            total_count=count
        )
        await message.answer(
            default_languages[lang]['product_add_cart'],
            reply_markup=common.get_main_menu(lang)
        )
        await state.clear()
        # else:
        #     await message.answer(default_languages[lang]["min_count_product"].format(product_min_count))
    else:
        await message.answer(default_languages[lang]['invalid_quantity'])

@commands_router.message(F.text.in_({'📦 Mening buyurtmalarim', '📦 Менинг буюртмаларим'}))
async def my_orders_handler(message: types.Message, cache: Cache, db: Database, state: FSMContext):
    orders = await db.order.get_all_by_user_id(message.from_user.id)
    k = f'lang_{message.from_user.id}'
    lang = await cache.get(k)
    lang = lang.decode()

    lat_longs = []

    if orders:
        msg = default_languages[lang]["order"] + '\n\n'
        for order in orders:
            msg += f"Buyurtma #{order.id}\n"
            msg += "Holati: TO'LANGAN\n"
            msg += "Manzil: {}\n"
            formatted_price = "{:,}".format(int(order.total_price)) 
            msg += f"Jami narx: {formatted_price}\n"
            msg += f"Buyurtma berilgan sana: {order.created_at}\n\n"
            lat_longs.append(f"https://www.google.com/maps?q={order.lat_long}")
        
        result = transliterate(msg, lang)
        await message.answer(result.format(*lat_longs))
    else:
        await message.answer(default_languages[lang]["order_not_found"])
    
@commands_router.message(F.text.in_({'📲 Biz bilan bog‘lanish', '📲 Биз билан боғланиш'}))
async def contact_handler(message: types.Message, state: FSMContext):
    await message.answer("📞 +998916694474\n📩 @Ruqiyasuv")

@commands_router.message(F.text.in_({'⚙️ Sozlamalar', '⚙️ Созламалар'}))
async def settings_handler(message: types.Message, cache: Cache, state: FSMContext):
    k = f'lang_{message.from_user.id}'
    lang = await cache.get(k)
    lang = lang.decode()

    await message.answer(
        transliterate("Kerakli sozlamalarni tanlang:", lang), 
        reply_markup=common.show_settings(lang)
    )
    await state.set_state(RegisterGroup.choose_option)


@commands_router.callback_query(RegisterGroup.choose_option)
async def choose_option_handler(c: types.CallbackQuery, cache: Cache, db: Database, state: FSMContext):
    k = f'lang_{c.from_user.id}'
    lang = await cache.get(k)
    lang = lang.decode()

    await c.answer()

    if c.data == 'change_lang':
        await c.message.answer(transliterate("Kerakli tilni tanlang:", lang), reply_markup=common.get_languages())
        await state.set_state(RegisterGroup.change_lang)
    
    elif c.data == 'change_phone_number':
        await c.message.answer(
            default_languages[lang]['contact'], 
            reply_markup=common.get_phone_number(lang)
        )
        await state.set_state(RegisterGroup.change_phone_number)
    
    elif c.data == 'change_name':
        await c.message.answer(default_languages[lang]['full_name'])
        await state.set_state(RegisterGroup.change_fullname)

@commands_router.callback_query(RegisterGroup.change_lang)
async def change_lang_handler(c: types.CallbackQuery, cache: Cache, db: Database, state: FSMContext):
    k = f'lang_{c.from_user.id}'
    # lang = await cache.get(k)
    # lang = lang.decode()

    await c.answer()

    match c.data:
        case 'lang_uz': lang = 'LATIN'
        case 'lang_ru': lang = 'CYRILLIC'

    await cache.set(k, lang)
    await db.user.update_user(
        user_id=c.from_user.id,
        language_code=lang
    )

    await c.message.answer(transliterate("Muvaqqiyatli o'zgardi", lang), reply_markup=common.get_main_menu(lang))
    await state.clear()

@commands_router.message(F.contact | F.text, RegisterGroup.change_phone_number)
async def change_contact_handler(message: types.Message, cache: Cache, db: Database, state: FSMContext):
    k = f'lang_{message.from_user.id}'
    lang = await cache.get(k)
    lang = lang.decode()

    if message.contact:
        await message.answer(transliterate("Muvafaqiyatli o'zgardi", lang))
        phone_number = message.contact.phone_number
    elif message.text:
        if check_phone(message.text):
            await message.answer(transliterate("Muvafaqiyatli o'zgardi", lang), reply_markup=common.get_main_menu(lang))
            phone_number = message.text
        else:
            return await message.answer(default_languages[lang]['sorry'])
    
    await db.user.update_user(
        user_id=message.from_user.id,
        phone_number=phone_number
    )
    await state.clear()

@commands_router.message(RegisterGroup.change_fullname)
async def change_fullname_handler(message: types.Message, cache: Cache, db: Database, state: FSMContext):
    k = f'lang_{message.from_user.id}'
    lang = await cache.get(k)
    lang = lang.decode()

    await db.user.update_user(
        user_id=message.from_user.id,
        full_name=message.text
    )
    await message.answer(default_languages[lang]["full_name_update"])
    await state.clear()

@commands_router.message(F.text.in_({'🛒 Savatcha', '🛒 Cаватча'}))
async def cart_handler(message: types.Message, cache: Cache, db: Database, state: FSMContext):
    cart_products = await db.cart.get_cart_products(user_id=message.from_user.id)

    k = f'lang_{message.from_user.id}'
    lang = await cache.get(k)
    lang = lang.decode()

    if cart_products:
        result = "Sizning savatchangiz:\n"
        for cart_product in cart_products:
            product = await db.product.get(cart_product.product_id)
            result += f"Tovar nomi: {product.product_name}\n"
            result += f"Tovar soni: {cart_product.total_count}\n"
            formatted_cart_price = "{:,}".format(int(cart_product.total_price)) 
            result += f"Umumiy summa: {formatted_cart_price}\n\n"
        
        await message.answer(transliterate(result, lang), reply_markup=common.make_order(lang))
        await state.set_state(OrderGroup.show_regions)
    else:
        await message.answer(default_languages[lang]['product_not_cart'])


@commands_router.callback_query(OrderGroup.show_regions)
async def show_districts(c: types.CallbackQuery, cache: Cache, db: Database, state: FSMContext):
    k = f'lang_{c.from_user.id}'
    lang = await cache.get(k)
    min_sum = await cache.get("min_sum")
    lang = lang.decode()
    min_sum = int(min_sum.decode())
    formatted_min_sum = "{:,}".format(min_sum) 

    user_products = await db.cart.get_cart_products(c.from_user.id)
    user_products_sum = sum([int(obj.total_price) for obj in user_products])

    if c.data == 'make_order':
        if min_sum > user_products_sum:
            await c.answer(
                text=transliterate(
                    text="Buyurtma uchun tovar summasi yetarli emas. "
                    f"Kamida {formatted_min_sum}-so'mlik harid qilishingiz kerak.",
                    to_variant=lang
                ),
                show_alert=True
            )
            await c.answer()
        else:
            await c.message.edit_reply_markup(reply_markup=common.show_regions(lang))
    else:
        if c.data == 'Farg‘ona':
            await state.set_data(dict(region=c.data))
            await c.message.edit_reply_markup(reply_markup=common.show_distincts(c.data, lang))
            await state.set_state(OrderGroup.show_districts)
        else:
            await c.message.answer(
                default_languages[lang]["connection"],
            )

@commands_router.callback_query(OrderGroup.show_districts)
async def show_districts(c: types.CallbackQuery, cache: Cache, db: Database, state: FSMContext):
    k = f'lang_{c.from_user.id}'
    lang = await cache.get(k)
    lang = lang.decode()

    await c.answer()

    await state.update_data(dict(district=c.data))
    await c.message.delete()
    await c.message.answer(default_languages[lang]["send_location_order"], reply_markup=common.get_location(lang))
    await state.set_state(OrderGroup.get_geo)

@commands_router.message(OrderGroup.get_geo, F.location)
async def cart_handler(message: types.Message, cache: Cache, db: Database, state: FSMContext):
    cart_products = await db.cart.get_cart_products(user_id=message.from_user.id)
    user = await db.user.get_me(user_id=message.from_user.id)

    k = f'lang_{message.from_user.id}'
    lang = await cache.get(k)
    lang = lang.decode()

    lat = message.location.latitude
    lon = message.location.longitude

    data = await state.get_data()
    region = data.get("region")
    district = data.get("district")

    total_price = 0
    new_order_id = await db.order.new(user_id=message.from_user.id)

    result = "Yangi buyurtma!\n\n"
    result += f"Buyurtma raqami: {new_order_id}\n"
    result += "Holati: 🟡 Kutilmoqda\n\n"
    result += f"Foydalanuvchi: {user.full_name}\n"
    result += f"Telefon raqam: {user.phone_number}\n"
    result += f"Manzil: https://www.google.com/maps?q={lat},{lon}\n"
    result += f"Viloyat: {region}\n"
    result += f"Shahar: {district}\n\n"

    data = []
    for cart_product in cart_products:
        result += f"Buyurtma:\n"
        product = await db.product.get(cart_product.product_id)
        result += f"Nomi: {product.product_name}\n"
        result += f"Miqdori: {cart_product.total_count}\n"
        formatted_cart_price = "{:,}".format(int(cart_product.total_price)) 
        result += f"Umumiy summa: {formatted_cart_price}\n\n"
        total_price += cart_product.total_price
        data.append((cart_product.id, product.product_name, cart_product.total_price, cart_product.total_count))

    # Add order
    for i in data:
        await db.order.new_item(
            order_id=new_order_id,
            user_id=message.from_user.id,
            product_name=i[1],
            total_price=i[2],
            total_count=i[3],
            lat_long=f"{lat},{lon}"
        )
    
    # Clear cart
    for j in data:
        await db.cart.delete_cart(cart_id=j[0])


    formatted_price = "{:,}".format(total_price) 
    result += f"Jami narx: {formatted_price}"

    await message.bot.send_message(
        chat_id=conf.CHAT_ID,
        text=result,
        reply_markup=common.get_order(new_order_id)
    )
    await message.answer(default_languages[lang]['order__'], reply_markup=common.get_main_menu(lang))
    await state.clear()


@commands_router.callback_query(F.data.startswith('get_order'))
async def show_districts(c: types.CallbackQuery, cache: Cache, db: Database, state: FSMContext):
    user = await db.user.get_me(user_id=c.from_user.id)
    if not user:
        return await c.answer("Iltimos avval bot orqali ro'yxatdan o'ting", show_alert=True)
    
    msg_text = c.message.text
    new_status = "Holati: 🟢 Qabul qilindi\n\n" \
                 f"Kuryer haqida ma'lumot:\n" \
                 f"Ismi: {c.from_user.first_name}\n" \
                 f"Telegram akkaunt: @{c.from_user.username}\n\n"
    new_text = msg_text.replace("Holati: 🟡 Kutilmoqda\n\n", new_status)

    _, order_id = c.data.split()

    await c.message.edit_text(text=new_text, reply_markup=common.order_complete(c.from_user.id, order_id))


@commands_router.callback_query(F.data.startswith('order_complete'))
async def show_districts(c: types.CallbackQuery, cache: Cache, db: Database, state: FSMContext):
    user = await db.user.get_me(user_id=c.from_user.id)
    if not user:
        return await c.answer("Iltimos avval bot orqali ro'yxatdan o'ting", show_alert=True)
    
    _, user_id, order_id = c.data.split()
    if int(user_id) != c.from_user.id:
        return await c.answer("Buyurtmani boshqa kuryer qabul qilgan")
    
    await db.approved_order.new(
        user_id=c.from_user.id,
        order_id=int(order_id)
    )

    await db.order.update_status(
        order_id=int(order_id),
        status=True
    )

    await c.message.edit_reply_markup(reply_markup=None)


@commands_router.message()
async def receive_message(message: types.Message, db: Database):
    undelivered_order = await db.order.filter_orders(
        user_id=message.from_user.id,
        status=False
    )

    if undelivered_order:
        return await message.answer("Iltimos kuting. Tez orada buyurtmangiz yetib boradi.")
