import re

all_languages = ['LATIN', 'CYRILLIC']

message_history = {}

default_languages = {
    "language_not_found": "Siz to'g'ri tilni tanlamadingiz!\n"
                          "Сиз тўғри тилни танламадингиз!",
    "welcome_message": "Assalomu alaykum, xush kelibsiz!\n"
                       "Quyidagi tillardan birini tanlang!\n\n"
                       "Ассалому алайкум, хуш келибсиз!\n"
                       "Қуйидаги тиллардан бирини танланг!",

    "LATIN": {
        "not": "❌ Siz botdan foydalana olmaysiz, siz qora ro'yxatdasiz.\n"
               "❗ Botdan foydalanish uchun admin bilan bog'laning: @ruqiyasuv",
        "connection": "Bizda faqat hozirda Farg‘ona uchun xizmatlarimiz mavjud:\n"
                      "Boshqa viloyatlar uchun Diller qidirilmoqda:\n"
                      "Takliflar uchun:\n"
                      "📞+998916694474 📩 @Ruqiyasuv",
        "name_update": "To'liq ismni o'zgartirish",
        "phone_update": "Telefon raqamini o'zgartirish",
        "lang_update": "Tilni o'zgartirish",
        "full_name_update": "Sizning to'liq ismingiz muvaffaqiyatli yangilandi:",
        "admin_not": "👮🏻‍♂️ Uzur siz Admin emassiz",
        "admin": "️Admin",
        "admin_welcome": "👮🏻‍♂️Admin Xushkelibsiz",
        "back": "Orqaga",
        "country": "Tuman tanlang:",
        "state_": "Viloyat tanlang:",
        "order__": "Buyurtmangiz qabul qilindi, kuriyerlarimiz siz bilan 24 soat ichida bog'lanishadi.",
        "min_order_required": "minimal buyurtma talab qilinadi",
        "min_order_error": "minimal buyurtma yetmadi",
        "send_receipt": "chek yuboring",
        "order": "Mening buyurtmalarim",
        "order_save": "Sizning buyurtmangiz qabul qilindi va saqlandi.",
        "send_location_order": "Buyurtmangizni tasdiqlash uchun manzilingizni yuboring.",
        "product_add_cart": "Mahsulotlaringiz pastdagi savatchaga tushdi o'sha yerdan buyurtma berishingiz mumkin:",
        "products_quantity_enter": "Mahsulot miqdorini kiriting:",
        "invalid_quantity": "Iltimos, son va 'ta' so'zidan iborat qiymat kiriting, masalan: 10 yoki 10 ta",
        "send_location": "Joylashuvni yuborish",
        "product_shopping_cart": "Sizning savatchangiz:",
        "product_not_cart": "Savatingiz boʻsh.",
        "cart": "🛒 Savatcha",
        "place_order": "Buyurtma berish",
        "delivery_time": "Yetkazib berish ",
        "products_price": "Narxi",
        "products_description": "tavsifi",
        "products": "Mahsulotlar",
        "category_select": "Mahsulotlarni tanlang",
        "order_not_found": "Buyurtma topilmadi!",
        "successful_changed": "Muvaffaqiyatli o'zgartirildi",
        "select_language": "Til tanlang!",
        'categories': '✅ Buyurtma berish',
        "my_orders": "📦 Mening buyurtmalarim",
        "contact_us": "📲 Biz bilan bog‘lanish",
        "settings": "⚙️ Sozlamalar",
        "full_name": "Iltimos to'liq ismni kiriting",
        "contact": "Iltimos raqamingizni yuboring",
        "contact_update": "Sizning telefon raqamingiz muvaffaqiyatli yangilandi:",
        "successful_registration": "Muvaffaqiyatli ro'yxatdan o'tdi",
        "sorry": "Kechirasiz, boshqa raqamni sinab ko'ring",
        "send_number": "Raqamni yuborish",
        "min_count_product": "Minimal {} ta tovar harid qilishingiz mumkin"
    },

    "CYRILLIC": {
        "not": "❌ Сиз ботдан фойдалана олмайсиз, сиз қора рўйхатдасиз.\n"
               "❗ Ботдан фойдаланиш учун админ билан боғланинг: @ruqiyasuv",
        "connection": "Бизда фақат ҳозирда Фарғона учун хизматларимиз мавжуд:\n"
                      "Бошқа вилоятлар учун Диллер қидирилмоқда:\n"
                      "Таклифлар учун:\n"
                      "📞+998916694474 📩 @Ruqiyasuv",
        "name_update": "Тўлиқ исмни ўзгартириш",
        "phone_update": "Телефон рақамини ўзгартириш",
        "lang_update": "Тилни ўзгартириш",
        "contact_update": "Сизнинг телефон рақамингиз муваффақиятли янгиланди:",
        "full_name_update": "Сизнинг тўлиқ исмингиз муваффақиятли янгиланди:",
        "admin_welcome": "👮🏻‍♂️️Админ Хушкелибсиз",
        "admin_not": "👮🏻‍♂️ Узур сиз Админ эмассиз",
        "admin": "Админ",
        "back": "Орқага",
        "country": "Туман танланг:",
        "state_": "Вилоят танланг:",
        "order__": "Буюртмангиз қабул қилинди, куриерларимиз сиз билан 24 соат ичида боғланишади.",
        "min_order_required": "минимал буюртма талаб қилинади",
        "min_order_error": "минимал буюртма етмади",
        "send_receipt": "чек юборинг",
        "order": "Менинг буюртмаларим",
        "invalid_quantity": "Илтимос, сон ва 'та' сўзидан иборат қиймат киритинг, масалан: 10 ёки 10 та",
        "order_save": "Сизнинг буюртмангиз қабул қилинди ва сақланди.",
        "send_location_order": "Буюртмангизни тасдиқлаш учун манзилингизни юборанг.",
        "product_add_cart": "Маҳсулотларингиз пастдаги саватчага тушди ўша ердан буюртма беришингиз мумкин:",
        "products_quantity_enter": "Маҳсулот миқдорини киритинг:",
        "send_location": "Жойлашувни юбориш",
        "product_shopping_cart": "Сизнинг саватингиз:",
        "product_not_cart": "Саватингиз бўш.",
        "cart": "🛒 Cаватча",
        "place_order": "Буюртма бериш",
        "delivery_time": "Етказиб бериш ",
        "products_price": "Hархи",
        "products_description": "тавсифи",
        "products": "Маҳсулотлар",
        "category_select": "Маҳсулотларни танланг",
        "order_not_found": "Буюртма топилмади!",
        "successful_changed": "Муваффақиятли ўзгартирилди",
        "select_language": "Тил танланг!",
        'categories': '✅ Буюртма бериш',
        "my_orders": "📦 Менинг буюртмаларим",
        "contact_us": "📲 Биз билан боғланиш",
        "settings": "⚙️ Созламалар",
        "full_name": "Илтимос тўлиқ исмни киритинг",
        "contact": "Илтимос рақамингизни юборинг",
        "successful_registration": "Муваффақиятли рўйхатдан ўтди",
        "sorry": "Кечирасиз, бошқа рақамни синаб кўринг",
        "send_number": "Ракамни юбориш",
        "min_count_product": "Минимал {} та товар ҳарид қилишингиз мумкин"
    }
}

user_languages = {}
local_user = {}

introduction_template = {
    'LATIN': """
<b>💧 Ruqiya Shifo suvi</b>
Tanangiz va ruhingiz salomatligi uchun Ruqiya qilingan tabiiy toza ichimlik suvi.

<b>🚛 Yetkazib berish bepul</b>
""",
    'CYRILLIC': """
<b>💧 Руқия Шифо суви</b>  
Танангиз ва руҳингиз саломатлиги учун Руқия қилинган табиий тоза ичимлик суви.  

<b>🚛 Етказиб бериш бепул</b>
"""
}

order_text = {
    "en": "Order number {} \n order status {}",
    "ru": "Номер заказа {} \n Статус заказа {}"
}

regions = {
    "Toshkent": ["Uchtepa", "Yashnobod", "Mirzo Ulug‘bek", "Chilonzor", "Yakkasaroy", "Mirobod", "Shayxontohur", "Yunusobod", "Olmaliq"],
    "Andijon": ["Andijon", "Asaka", "Baliqchi", "Buloqbosh", "Izboskan", "Jalolobod", "Qo‘rg‘ontepa", "Marhamat", "Oltinko‘l", "Xo‘jaobod"],
    "Buxoro": ["Buxoro", "G‘ijduvon", "Kogon", "Qorako‘l", "Romitan", "Shofirkon", "Vobkent", "Galaosiyo", "Peshku", "Qorako‘l"],
    "Farg‘ona": ["Farg‘ona", "Qo‘qon", "Marg‘ilon", "Buvayda", "Chimyon", "Dang‘ara", "Furqat", "Qoshtegirmon", "Yozyovon", "Uchko‘prik"],
    "Jizzax": ["Jizzax", "Arnasoy", "Do‘stlik", "G‘allaorol", "Sharof Rashidov", "Zafarobod", "Zarbdor", "Mirzachul", "Paxtakor", "Yangiobod"],
    "Namangan": ["Namangan", "Chortoq", "Pop", "Uychi", "Chartak", "Chust", "Kosonsoy", "To‘raqo‘rg‘on", "Yangiqo‘rg‘on", "Mingbuloq"],
    "Navoiy": ["Navoiy", "Qiziltepa", "Navbahor", "Karmana", "Tomdi", "Uchquduq", "Beshrabot", "Nurota", "Xatirchi", "Konimex"],
    "Qashqadaryo": ["Qarshi", "Shahrisabz", "Koson", "Chiroqchi", "Dehqonobod", "G‘uzor", "Qamashi", "Muborak", "Kitob", "Mirishkor"],
    "Samarqand": ["Samarqand", "Ishtixon", "Paxtachi", "Bulung‘ur", "Jomboy", "Kattakurgan", "Narpay", "Nurobod", "Oqdaryo", "Payariq"],
    "Sirdaryo": ["Guliston", "Sirdaryo", "Mirzaobod", "Sardoba", "Boyovut", "Oqoltin", "Sayxunobod", "Yangiyer", "Shirin", "Hovos"],
    "Surxondaryo": ["Termiz", "Sho‘rtan", "Uzun", "Angor", "Bandixon", "Boysun", "Qiziriq", "Denov", "Jarqo‘rg‘on", "Sho‘rchi"],
    "Toshkent viloyati": ["Nurafshon", "Zangiota", "O‘rtachirchiq", "Yangiyo‘l", "Bekobod", "Qibray", "Piskent", "Oqqo‘rg‘on", "Chirchiq"],
    "Xorazm": ["Urganch", "Xonqa", "Yangiariq", "Bog‘ot", "Gurlan", "Hazorasp", "Xiva", "Qo‘shko‘pir", "Shovot", "Tuproqqal’a"],
    "Qoraqalpog‘iston Respublikasi": ["Nukus", "Qungrad", "Mo‘ynoq", "Amudaryo", "Beruniy", "Chimboy", "Ellikqala", "Kegeyli", "Moynaq", "Nukus"]
}


def get_product_info(user_lang: str, product_name: str, price: str):
    data = {
        "LATIN": f"📦 Maxsulotlar: {product_name}\n" \
            f"✅ Narxi: {price} so'm\n" \
            f"🚚 Yetkazib berish Bepul",
        "CYRILLIC": f"📦 Маҳсулотлар: {product_name}\n" \
            f"✅ Hархи: {price} сўм\n" \
            f"🚚 Етказиб бериш Бепул"
    }
    return data[user_lang]


def check_phone(phone_number):
    pattern = r'^\+998\d{9}$'
    return re.match(pattern, phone_number) is not None


def fix_phone(phone: str):
    if not phone.startswith('+'):
        return f"+{phone}"
    return phone
