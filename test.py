from src.bot.utils.transliterate import transliterate

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


regions_and_districts = {}
for k in regions:
    regions_and_districts[k] = transliterate(k, 'CYRILLIC')

for k in regions:
    for v in regions[k]:
        regions_and_districts[v] = transliterate(v, 'CYRILLIC')

print(regions_and_districts)
