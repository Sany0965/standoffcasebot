import telebot
import random
import sqlite3
import threading
import time
import datetime
from telebot import types

# Замените 'YOUR_BOT_TOKEN' на ваш токен бота
TOKEN = 'YOUR_BOT_TOKEN'
admins = [********] #Вместо звездочек вставьте свой id 

bot = telebot.TeleBot(TOKEN)

# Имя файла базы данных SQLite
DB_FILE = 'user_profiles.db'

# Переменная для хранения профилей пользователей
user_profiles = {}

transactions_history = []


PROMOCODES_FILE = 'promocodes.txt'

# Словарь с предметами и их редкостями для Gift Box
gift_box_items = {
    "origin box": {"rarity": "rare", "photo": "origin_box.jpg", "price": 100},
    "furious box": {"rarity": "rare", "photo": "furious_box.jpg", "price": 100},
    "rival box": {"rarity": "rare", "photo": "rival_box.jpg", "price": 100},
    "origin case": {"rarity": "rare", "photo": "origin_case.jpg", "price": 10000},
    "furious case": {"rarity": "epic", "photo": "furious_case.jpg", "price": 580},
    "AWM Sport V2": {"rarity": "legendary", "photo": "awm_sport_v2.jpg", "price": 44444.44},
    "karambit GOLD": {"rarity": "arcana", "photo": "karambit_gold.jpg", "price": 75000},
}

# Словарь с предметами и их редкостями для Fable Case
fable_case_items = {
    "бабочка старфолл": {"rarity": "arcana", "photo": "butterfly_starfall.jpg", "price": 1398},
    "бабочка чёрная вдова": {"rarity": "arcana", "photo": "butterfly_black_widow.jpg", "price": 1425.55},
    "бабочка драгон глаз": {"rarity": "arcana", "photo": "butterfly_dragon_eye.jpg", "price": 1700},
    "бабочка легаси": {"rarity": "arcana", "photo": "butterfly_legacy.jpg", "price": 1843.90},
    "m4 samurai": {"rarity": "arcana", "photo": "m4_samurai.jpg", "price": 93},
    "f/s venom": {"rarity": "arcana", "photo": "fs_venom.jpg", "price": 54.59},
    "m4 lizard": {"rarity": "legendary", "photo": "m4_lizard.jpg", "price": 12.50},
    "mp7 lich": {"rarity": "legendary", "photo": "mp7_lich.jpg", "price": 12.30},
    "tec-9 fable": {"rarity": "legendary", "photo": "tec9_fable.jpg", "price": 11.50},
    "fn fal tactical": {"rarity": "epic", "photo": "fn_fal_tactical.jpg", "price": 1.44},
    "ump45 cerberus": {"rarity": "epic", "photo": "ump45_cerberus.jpg", "price": 1.24},
    "usp pisces": {"rarity": "epic", "photo": "usp_pisces.jpg", "price": 1.54},
    "m110 cyber": {"rarity": "rare", "photo": "m110_cyber.jpg", "price": 0.30},
    "f/s tactical": {"rarity": "rare", "photo": "fs_tactical.jpg", "price": 0.30},
    "дигл ace": {"rarity": "rare", "photo": "deagle_ace.jpg", "price": 0.30},
    "g22 starfall": {"rarity": "rare", "photo": "g22_starfall.jpg", "price": 0.30},
}

# Словарь предметов для Subject X
subject_x_case_items = {
    "Gloves immolation": {"rarity": "arcana", "photo": "gloves_immolation_arcana.jpg", "price": 1158},
    "Gloves mortal_veil": {"rarity": "arcana", "photo": "gloves_mortal_veil_arcana.jpg", "price": 1398},
    "Gloves plague": {"rarity": "arcana", "photo": "gloves_plague_arcana.jpg", "price": 1510},
    "Gloves haunt": {"rarity": "arcana", "photo": "gloves_haunt_arcana.jpg", "price": 2600},
    "Gloves shatter": {"rarity": "arcana", "photo": "gloves_shatter_arcana.jpg", "price": 2748},
    "Gloves flux": {"rarity": "arcana", "photo": "gloves_flux_arcana.jpg", "price": 1578},
    "M60 QUANTUM": {"rarity": "rare", "photo": "m60_quantum.jpg", "price": 0.40},
    "BERRETAS HYBRID": {"rarity": "rare", "photo": "berretas_hybrid.jpg", "price": 1},
    "G22 HAUNT": {"rarity": "epic", "photo": "g22_haunt.jpg", "price": 21},
    "M40 VENOM SHADE": {"rarity": "epic", "photo": "m40_venom_shade.jpg", "price": 8},
    "AKR 12 HAUNT": {"rarity": "legendary", "photo": "akr_12_haunt.jpg", "price": 60},
    "M4 K-NAI": {"rarity": "arcana", "photo": "m4_k-nai_arcana.jpg", "price": 1580},
    "STICKER RABID COLOR": {"rarity": "arcana", "photo": "sticker_rabid_color.jpg", "price": 750},
    "STICKER CRAZY DEVIL COLOR": {"rarity": "rare", "photo": "sticker_crazy_devil_color.jpg", "price": 5},
    "STICKER CLEAVER-MINDED COLOR": {"rarity": "epic", "photo": "sticker_cleaver-minded_color.jpg", "price": 22},
    "STICKER MIND CONTROL": {"rarity": "epic", "photo": "sticker_mind_control.jpg", "price": 24},
    "STICKER ELUSIVE BEAST COLOR": {"rarity": "legendary", "photo": "sticker_elusive_beast_color.jpg", "price": 55},
    "CHARM SUBJECT X": {"rarity": "rare", "photo": "charm_subject_x.jpg", "price": 5},
    "CHARM CLEAVER": {"rarity": "rare", "photo": "charm_cleaver.jpg", "price": 13},
    "CHARM GENE-X": {"rarity": "epic", "photo": "charm_gene-x.jpg", "price": 25},
    "CHARM PHANTOM SCAN": {"rarity": "epic", "photo": "charm_phantom_scan.jpg", "price": 72},
    "CHIBI LAB WHIZ": {"rarity": "legendary", "photo": "chibi_lab_whiz.jpg", "price": 185},
    "CHARM LAB CRYPT": {"rarity": "arcana", "photo": "charm_lab_crypt.jpg", "price": 840},
    "GRAFFITI SUBJECT X": {"rarity": "rare", "photo": "graffiti_subject_x.jpg", "price": 0.5},
    "GRAFFITI OMEN": {"rarity": "rare", "photo": "graffiti_omen.jpg", "price": 2},
    "GRAFFITI EMPOWERED": {"rarity": "epic", "photo": "graffiti_empowered.jpg", "price": 8},
    "GRAFFITI CRIMSON SCULL": {"rarity": "epic", "photo": "graffiti_crimson_scull.jpg", "price": 7},
    "GRAFFITI LAB BAT": {"rarity": "legendary", "photo": "graffiti_lab_bat.jpg", "price": 20},
    "GRAFFITI BITE": {"rarity": "arcana", "photo": "graffiti_bite.jpg", "price": 2},

}

subject_x_case_probabilities = {
    "arcana": 5,       # Вероятность 7% для арканы
    "legendary": 14,   # Вероятность 14% для легендарки
    "epic": 29,        # Вероятность 29% для эпика
    "rare": 52         # Вероятность 50% для редкого предмета
}


# Вероятности для Fable Case
fable_case_probabilities = {
    "arcana": 6,       # Вероятность 2% для арканы
    "legendary": 14,  # Вероятность 15% для легендарки
    "epic": 30,       # Вероятность 30% для эпика
    "rare": 50        # Вероятность 53% для редкого предмета
}

# Вероятности для Gift Box
gift_box_probabilities = {
    "rare": 90,      # Вероятность 90% для редкого предмета
    "epic": 5,       # Вероятность 5% для эпика
    "arcana": 2,     # Вероятность 2% для арканы
    "legendary": 3   # Вероятность 3% для легендарки
}

halloween_charms_park_items = {
    "Charm Horseman's": {"rarity": "rare", "photo": "charm_horsemans.jpg", "price": 160},
    "Charm Brainless": {"rarity": "rare", "photo": "charm_brainless.jpg", "price": 70},
    "Charm Friendly": {"rarity": "rare", "photo": "charm_friendly.jpg", "price": 96},
    "Charm Meteor": {"rarity": "rare", "photo": "charm_meteor.jpg", "price": 111},
    "Charm Scarecrow": {"rarity": "epic", "photo": "charm_scarecrow.jpg", "price": 193},
    "Chibi Crunch": {"rarity": "epic", "photo": "chibi_crunch.jpg", "price": 60},
    "Charm Witchcraft": {"rarity": "epic", "photo": "charm_witchcraft.jpg", "price": 143},
    "Charm Crooked": {"rarity": "epic", "photo": "charm_crooked.jpg", "price": 60},
    "Charm Halloween": {"rarity": "legendary", "photo": "charm_halloween.jpg", "price": 1189},
    "Charm Vampire Bat": {"rarity": "legendary", "photo": "charm_vampire_bat.jpg", "price": 987},
    "Charm Spooky": {"rarity": "legendary", "photo": "charm_spooky.jpg", "price": 730},
    "Charm Reaper": {"rarity": "arcana", "photo": "charm_reaper.jpg", "price": 8700},
    "Charm Suspicious": {"rarity": "arcana", "photo": "charm_suspicious.jpg", "price": 15877},
}



halloween_charms_park_probabilities = {
    "rare": 72,       # Вероятность 72.10% для редкого предмета
    "epic": 24,       # Вероятность 24.10% для эпика
    "legendary": 3,   # Вероятность 3.60% для легендарки
    "arcana": 1        # Вероятность 0.20% для арканы
}



halloween_charms_park_case_price = 3050

def is_admin(user_id):
    return user_id in admins
@bot.message_handler(commands=['post'])
def send_post(message):
    user_id = message.from_user.id

    # Проверка, является ли пользователь администратором
    if is_admin(user_id):
        # Получите текст для рассылки из сообщения пользователя
        text_to_send = message.text.replace('/post', '').strip()

        # Получите список всех пользователей
        all_users = [profile_id for profile_id in user_profiles]

        # Отправка сообщения каждому пользователю
        for user_id in all_users:
            try:
                bot.send_message(user_id, text_to_send)
            except Exception as e:
                print(f"Ошибка при отправке сообщения пользователю {user_id}: {str(e)}")

        # Отправьте подтверждение администратору
        bot.send_message(message.chat.id, "Сообщение успешно разослано всем пользователям.")
    else:
        bot.send_message(message.chat.id, "Вы не являетесь администратором.")


def activate_promocode(user_id, promocode):
    try:
        with open(PROMOCODES_FILE, 'r') as file:
            for line in file:
                parts = line.strip().split(' ')
                if len(parts) == 2:
                    code, gold = parts
                    if code == promocode:
                        user_profile = user_profiles.get(user_id)
                        if user_profile:
                            # Проверяем, использовал ли пользователь этот промокод ранее
                            used_promocodes = user_profile.get('used_promocodes', [])
                            if promocode not in used_promocodes:
                                user_profile['gold'] += float(gold)
                                used_promocodes.append(promocode)  # Добавляем промокод в список использованных
                                user_profile['used_promocodes'] = used_promocodes
                                save_user_profile(user_profile)
                                return f"Вы активировали промокод и получили {gold} голды! 💰"
                            else:
                                return "Промокод уже использован. Вы не можете использовать его снова."
                        else:
                            return "Профиль не найден. Пожалуйста, начните с команды /start."
            return "Промокод не найден. Пожалуйста, проверьте его правильность."
    except Exception as e:
        print("Error:", e)
        return "Произошла ошибка при активации промокода. Пожалуйста, попробуйте позже."



# Обработчик команды "Промокод ✏️"
@bot.message_handler(func=lambda message: message.text == "Промокод ✏️")
def enter_promocode(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Введите промокод:")
    bot.register_next_step_handler(message, process_promocode)

# Функция для обработки введенного промокода
def process_promocode(message):
    user_id = message.from_user.id
    promocode = message.text.strip()
    response = activate_promocode(user_id, promocode)
    bot.send_message(user_id, response, reply_markup=main_menu_keyboard)

def activate_promo_code(user_id, promo_code):
    user_profile = user_profiles.get(user_id)

    # Проверяем, использовал ли пользователь этот промокод ранее
    if promo_code not in user_profile.get('used_promo_codes', []):
        # Если промокод не был использован, активируем его
        user_profile['gold'] += promo_codes.get(promo_code, 0)
        user_profile.setdefault('used_promo_codes', []).append(promo_code)
        save_user_profile(user_profile)
        return True
    else:
        return False


# Создаем клавиатуру с кнопками "Профиль", "Открыть Fable Case🗃", "Открыть Gift box 🎁" и "Промокод ✏️"
main_menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
profile_button = types.KeyboardButton("Профиль🤖")
open_fable_case_button = types.KeyboardButton("Открыть Fable Case🗃")
open_gift_box_button = types.KeyboardButton("Открыть Gift box 🎁")
bonus_button = types.KeyboardButton("Бонус 🌟")
promo_button = types.KeyboardButton("Промокод ✏️")
subject_x_button = types.KeyboardButton("Subject X 📦")
halloweens_charms_park_case_button = types.KeyboardButton("Открыть Halloween 2020 Charms Park Case🎃")

main_menu_keyboard.row(subject_x_button, halloweens_charms_park_case_button)
main_menu_keyboard.row(profile_button, open_fable_case_button, open_gift_box_button)
main_menu_keyboard.row(bonus_button, promo_button)


@bot.message_handler(func=lambda message: message.text == "Бонус 🌟")
def bonus(message):
    user_id = message.from_user.id
    user_profile = user_profiles.get(user_id)
    if user_profile:
        if give_daily_bonus(user_id):
            bot.reply_to(message, "Вы получили ежедневный бонус в 20000 золота! 🎁")
            save_user_profile(user_profile)  # Сохраняем обновленный профиль пользователя
            # После выдачи бонуса, выводим, через сколько часов можно получить следующий
            next_bonus_time = user_profile['last_bonus_time'] + 24 * 3600
            current_time = int(time.time())
            hours_until_next_bonus = (next_bonus_time - current_time) // 3600
            minutes_until_next_bonus = ((next_bonus_time - current_time) % 3600) // 60
            bot.send_message(user_id, f"Следующий бонус будет доступен через {hours_until_next_bonus} часов и {minutes_until_next_bonus} минут.")
        else:
            bot.reply_to(message, "Вы уже получили сегодняшний бонус. Попробуйте позже.")
    else:
        bot.reply_to(message, "Произошла ошибка. Пожалуйста, попробуйте позже.")

# Функция для создания базы данных и таблицы, если их нет
def create_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_profiles (
            user_id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            username TEXT,
            opened_cases INTEGER,
            arcana_received INTEGER,
            legendary_received INTEGER,
            rare_received INTEGER,
            epic_received INTEGER,
            gold REAL,
            last_bonus_time INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Функция для загрузки профиля пользователя из базы данных
def load_user_profile(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_profiles WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        user_profile = {
            'user_id': row[0],
            'first_name': row[1],
            'last_name': row[2],
            'username': row[3],
            'opened_cases': row[4],
            'arcana_received': row[5],
            'legendary_received': row[6],
            'rare_received': row[7],
            'epic_received': row[8],
            'gold': row[9],
            'last_bonus_time': row[10]
        }
    else:
        user_profile = {
            'user_id': user_id,
            'first_name': None,
            'last_name': None,
            'username': None,
            'opened_cases': 0,
            'arcana_received': 0,
            'legendary_received': 0,
            'rare_received': 0,
            'epic_received': 0,
            'gold': 0,
            'last_bonus_time': 0
        }
    return user_profile

# Функция для сохранения профиля пользователя в базе данных
def save_user_profile(user_profile):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO user_profiles (
            user_id, first_name, last_name, username,
            opened_cases, arcana_received, legendary_received, rare_received, epic_received, gold, last_bonus_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_profile['user_id'], user_profile['first_name'], user_profile['last_name'],
        user_profile['username'], user_profile['opened_cases'], user_profile['arcana_received'],
        user_profile['legendary_received'], user_profile['rare_received'], user_profile['epic_received'],
        user_profile['gold'], user_profile['last_bonus_time']
    ))
    conn.commit()
    conn.close()

# Функция для начисления бонуса в голдах
def give_daily_bonus(user_id):
    user_profile = user_profiles.get(user_id)
    if user_profile:
        last_bonus_time = user_profile.get('last_bonus_time', 0)
        current_time = int(time.time())
        if current_time - last_bonus_time >= 24 * 3600:  # Проверка, прошло ли 24 часа с последнего бонуса
            user_profile['gold'] += 20000
            user_profile['last_bonus_time'] = current_time
            save_user_profile(user_profile)
            return True  # Бонус успешно начислен
    return False  # Бонус не начислен

# Обработка команды /start
@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user
    bot.send_message(message.chat.id,
        f"Привет, {user.first_name}! Я бот для открытия кейсов и подарков.",
        reply_markup=main_menu_keyboard
    )
    create_database()  # Создаем базу данных, если ее нет
    user_profiles[user.id] = load_user_profile(user.id)  # Загружаем профиль пользователя из базы данных, если он есть

# Функция для обработки команды "Профиль"
# Функция для обработки команды "Профиль"
@bot.message_handler(func=lambda message: message.text == "Профиль🤖")
def profile(message):
    user = message.from_user
    if user.id in user_profiles:
        profile_info = user_profiles[user.id]
        first_name = user.first_name if user.first_name else 'Неизвестно'
        last_name = user.last_name if user.last_name else 'Неизвестно'
        username = user.username if user.username else 'Неизвестно'
        opened_cases = profile_info['opened_cases']
        arcana_received = profile_info['arcana_received']
        legendary_received = profile_info['legendary_received']
        rare_received = profile_info['rare_received']
        epic_received = profile_info['epic_received']
        gold = profile_info['gold']

        # Проверяем, есть ли информация о транзакциях пользователя за последние 24 часа
        transactions_today = get_transactions_today(user.id)
        spent_gold_today = sum(transaction['item_price'] for transaction in transactions_today)

        profile_text = (
            f"Имя: {first_name} {last_name}\n"
            f"Username: {username}\n"
            f"ID: {user.id}\n"
            f"Открытых кейсов: {opened_cases}\n"
            f"Полученных аркан: {arcana_received}\n"
            f"Полученных legendary: {legendary_received}\n"
            f"Полученных rare: {rare_received}\n"
            f"Полученных epic: {epic_received}\n"
            f"Голд: {gold:.2f} 💰\n"
            f"Продано скинов за последние 24 часа на сумму: {spent_gold_today:.2f} 💰"
        )
        bot.send_message(message.chat.id, profile_text, reply_markup=main_menu_keyboard)
    else:
        bot.send_message(message.chat.id, "Профиль не найден. Пожалуйста, начните с команды /start.", reply_markup=main_menu_keyboard)

# Функция для получения информации о транзакциях пользователя за последние 24 часа
def get_transactions_today(user_id):
    current_date = datetime.datetime.now().date()

    # Фильтруем транзакции за последние 24 часа
    transactions_today = [transaction for transaction in transactions_history
                          if transaction['user_id'] == user_id
                          and transaction['transaction_date'] == current_date]

    return transactions_today
# Функция для обработки команды "Открыть Fable Case🗃"
@bot.message_handler(func=lambda message: message.text == "Открыть Fable Case🗃")
def open_fable_case(message):
    user = message.from_user
    chat_id = message.chat.id

    if user.id in user_profiles:
        user_profile = user_profiles[user.id]

        # Проверяем, хватает ли у пользователя голды для открытия Fable Case
        if user_profile['gold'] >= 100:
            rarity, item = open_fable_case_item()

            # Обновляем информацию о профиле пользователя
            user_profile['opened_cases'] += 1
            user_profile['gold'] -= 100
            save_user_profile(user_profile)

            # Отправляем сообщение с текстом, фотографией и кнопкой "Продать"
            result_message = (f"{user.first_name} открывает Fable Case...\n"
                              f"Вам выпал предмет {fable_case_items[item]['rarity']}: {item}")
            photo_path = fable_case_items[item]['photo']
            item_price = fable_case_items[item]['price']
            item_price_text = f"Цена: {item_price} 💰"
            keyboard = types.InlineKeyboardMarkup()
            sell_button = types.InlineKeyboardButton(text="Продать", callback_data=f"sell_{item}")
            keyboard.add(sell_button)

            with open(photo_path, 'rb') as photo:
                bot.send_photo(chat_id, photo, caption=f"{result_message}\n{item_price_text}", reply_markup=keyboard)

        else:
            bot.send_message(chat_id, "У вас недостаточно голды для открытия Fable Case. Вы можете получить бонус или продать предметы, чтобы заработать больше голды.", reply_markup=main_menu_keyboard)
    else:
        bot.send_message(chat_id, "Профиль не найден. Пожалуйста, начните с команды /start.", reply_markup=main_menu_keyboard)

# Функция для выбора предмета из Fable Case
def open_fable_case_item():
    # Создаем список всех возможных предметов с учетом их вероятностей
    all_items = []
    for item, info in fable_case_items.items():
        rarity = info["rarity"]
        probability = fable_case_probabilities.get(rarity, 0)
        all_items.extend([item] * probability)

    # Случайным образом выбираем предмет из списка
    item = random.choice(all_items)
    rarity = fable_case_items[item]['rarity']

    return rarity, item


# Функция для открытия Halloween 2020 Charms Park Case
@bot.message_handler(func=lambda message: message.text == "Открыть Halloween 2020 Charms Park Case🎃")
def open_halloween_charms_park_case(message):
    user = message.from_user
    chat_id = message.chat.id

    if user.id in user_profiles:
        user_profile = user_profiles[user.id]

        # Проверяем, хватает ли у пользователя голды для открытия Halloween Charms Park Case
        if user_profile['gold'] >= halloween_charms_park_case_price:
            rarity, item = open_halloween_charms_park_case_item()

            # Обновляем информацию о профиле пользователя
            user_profile['opened_cases'] += 1
            user_profile['gold'] -= halloween_charms_park_case_price
            save_user_profile(user_profile)

            # Отправляем сообщение с текстом, фотографией и кнопкой "Продать"
            result_message = (f"{user.first_name} открывает Halloween 2020 Charms Park Case...\n"
                              f"Вам выпал предмет {halloween_charms_park_items[item]['rarity']}: {item}")
            photo_path = halloween_charms_park_items[item]['photo']
            item_price = halloween_charms_park_items[item]['price']
            item_price_text = f"Цена: {item_price} 💰"
            keyboard = types.InlineKeyboardMarkup()
            sell_button = types.InlineKeyboardButton(text="Продать", callback_data=f"sell_{item}")
            keyboard.add(sell_button)

            with open(photo_path, 'rb') as photo:
                bot.send_photo(chat_id, photo, caption=f"{result_message}\n{item_price_text}", reply_markup=keyboard)

        else:
            bot.send_message(chat_id, "У вас недостаточно голды для открытия Halloween 2020 Charms Park Case. Вы можете получить бонус или продать предметы, чтобы заработать больше голды.", reply_markup=main_menu_keyboard)
    else:
        bot.send_message(chat_id, "Профиль не найден. Пожалуйста, начните с команды /start.", reply_markup=main_menu_keyboard)

# Функция для выбора предмета из Halloween Charms Park Case
# Функция для выбора предмета из Halloween Charms Park Case
def open_halloween_charms_park_case_item():
    # Создаем список всех возможных предметов с учетом их вероятностей
    all_items = []
    for item, info in halloween_charms_park_items.items():
        # Здесь необходимо определить переменную `rarity`
        rarity = info["rarity"]
        probability = round(halloween_charms_park_probabilities.get(rarity, 0))
        all_items.extend([item] * probability)

    # Случайным образом выбираем предмет из списка
    item = random.choice(all_items)
    rarity = halloween_charms_park_items[item]['rarity']

    return rarity, item

# Этот код вызывает функцию open_halloween_charms_park_case_item
# Убедитесь, что вы используете переменную `rarity` в правильной области видимости
if __name__ == "__main__":
    rarity, item = open_halloween_charms_park_case_item()
    print(f"Открыт предмет {item} с редкостью {rarity}")







# Функция для обработки команды "Открыть Subject X 📦"
@bot.message_handler(func=lambda message: message.text == "Subject X 📦")
def subject_x_menu(message):
    # Ваш код обработки команды "Subject X"

    user = message.from_user
    chat_id = message.chat.id

    if user.id in user_profiles:
        user_profile = user_profiles[user.id]

        # Проверяем, хватает ли у пользователя голды для открытия Subject X 📦
        if user_profile['gold'] >= 2000:
            item = open_subject_x_case_item()

            # Обновляем информацию о профиле пользователя
            user_profile['opened_cases'] += 1
            user_profile['gold'] -= 2000
            save_user_profile(user_profile)

            # Отправляем сообщение с текстом, фотографией и кнопкой "Продать"
            result_message = (f"{user.first_name} открывает Subject X 📦...\n"
                              f"Вам выпал предмет {subject_x_case_items[item]['rarity']}: {item}")
            photo_path = subject_x_case_items[item]['photo']
            item_price = subject_x_case_items[item]['price']
            item_price_text = f"Цена: {item_price} 💰"
            keyboard = types.InlineKeyboardMarkup()
            sell_button = types.InlineKeyboardButton(text="Продать", callback_data=f"sell_{item}")
            keyboard.add(sell_button)

            with open(photo_path, 'rb') as photo:
                bot.send_photo(chat_id, photo, caption=f"{result_message}\n{item_price_text}", reply_markup=keyboard)

        else:
            bot.send_message(chat_id, "У вас недостаточно голды для открытия Subject X 📦. Вы можете получить бонус или продать предметы, чтобы заработать больше голды.", reply_markup=main_menu_keyboard)
    else:
        bot.send_message(chat_id, "Профиль не найден. Пожалуйста, начните с команды /start.", reply_markup=main_menu_keyboard)

# Функция для выбора предмета из Subject X 📦
def open_subject_x_case_item():
    # Создаем список всех возможных предметов с учетом их вероятностей
    all_items = []
    for item, info in subject_x_case_items.items():
        rarity = info["rarity"]
        probability = subject_x_case_probabilities.get(rarity, 0)
        all_items.extend([item] * probability)

    # Случайным образом выбираем предмет из списка
    item = random.choice(all_items)

    return item



# Функция для обработки команды "Открыть Gift box 🎁"
@bot.message_handler(func=lambda message: message.text == "Открыть Gift box 🎁")
def open_gift_box(message):
    user = message.from_user
    chat_id = message.chat.id

    if user.id in user_profiles:
        user_profile = user_profiles[user.id]

        # Проверяем, хватает ли у пользователя голды для открытия Gift Box
        if user_profile['gold'] >= 25000:
            rarity, item = open_gift_box_item()

            # Обновляем информацию о профиле пользователя
            user_profile['opened_cases'] += 1
            user_profile['gold'] -= 25000
            save_user_profile(user_profile)

            # Отправляем сообщение с текстом, фотографией и кнопкой "Продать"
            result_message = (f"{user.first_name} открывает Gift Box...\n"
                              f"Вам выпал предмет {gift_box_items[item]['rarity']}: {item}")
            photo_path = gift_box_items[item]['photo']
            item_price = gift_box_items[item]['price']
            item_price_text = f"Цена: {item_price} 💰"
            keyboard = types.InlineKeyboardMarkup()
            sell_button = types.InlineKeyboardButton(text="Продать", callback_data=f"sell_{item}")
            keyboard.add(sell_button)

            with open(photo_path, 'rb') as photo:
                bot.send_photo(chat_id, photo, caption=f"{result_message}\n{item_price_text}", reply_markup=keyboard)

        else:
            bot.send_message(chat_id, "У вас недостаточно голды для открытия Gift Box. Вы можете получить бонус или продать предметы, чтобы заработать больше голды.", reply_markup=main_menu_keyboard)
    else:
        bot.send_message(chat_id, "Профиль не найден. Пожалуйста, начните с команды /start.", reply_markup=main_menu_keyboard)

# Функция для выбора предмета из Gift Box
def open_gift_box_item():
    # Создаем список всех возможных предметов с учетом их вероятностей
    all_items = []
    for item, info in gift_box_items.items():
        rarity = info["rarity"]
        probability = gift_box_probabilities.get(rarity, 0)
        all_items.extend([item] * probability)

    # Случайным образом выбираем предмет из списка
    item = random.choice(all_items)
    rarity = gift_box_items[item]['rarity']

    return rarity, item

# Обработка команды /bonus
@bot.message_handler(func=lambda message: message.text == "Бонус 🌟")
def bonus(message):
    user = message.from_user
    chat_id = message.chat.id

    if user.id in user_profiles:
        user_profile = user_profiles[user.id]

        if give_daily_bonus(user.id):
            updated_user_profile = user_profiles[user.id]
            bot.send_message(chat_id, f"Вы получили ежедневный бонус 1000 голды! Теперь у вас {updated_user_profile['gold']} голды. Возвращайтесь каждый день для нового бонуса.", reply_markup=main_menu_keyboard)
        else:
            bot.send_message(chat_id, "Вы уже получили ежедневный бонус сегодня. Приходите завтра снова!", reply_markup=main_menu_keyboard)
    else:
        bot.send_message(chat_id, "Профиль не найден. Пожалуйста, начните с команды /start.", reply_markup=main_menu_keyboard)

# Обработка нажатий на кнопки "Продать" в сообщениях с предметами
@bot.callback_query_handler(func=lambda call: call.data.startswith("sell_"))
def sell_item(call):
    user = call.from_user
    chat_id = call.message.chat.id
    item_name = call.data[5:]

    if user.id in user_profiles:
        user_profile = user_profiles[user.id]

        # Проверяем, существуют ли ключи в профиле пользователя
        if 'spent_gold_today' not in user_profile:
            user_profile['spent_gold_today'] = 0
        if 'total_sold_value_24h' not in user_profile:
            user_profile['total_sold_value_24h'] = 0

        if item_name in fable_case_items or item_name in gift_box_items or item_name in subject_x_case_items or item_name in halloween_charms_park_items:
            item_price = 0

            if item_name in fable_case_items:
                item_price = fable_case_items[item_name]['price']
            elif item_name in gift_box_items:
                item_price = gift_box_items[item_name]['price']
            elif item_name in subject_x_case_items:
                item_price = subject_x_case_items[item_name]['price']
            elif item_name in halloween_charms_park_items:
                item_price = halloween_charms_park_items[item_name]['price']

            # Обновляем информацию о продаже в профиле пользователя
            user_profile['spent_gold_today'] += item_price
            user_profile['total_sold_value_24h'] += item_price
            user_profile['gold'] += item_price
            save_user_profile(user_profile)

            # Добавляем информацию о транзакции в историю
            transaction = {
                'user_id': user.id,
                'item_name': item_name,
                'item_price': item_price,
                'transaction_date': datetime.datetime.now().date()
            }
            transactions_history.append(transaction)

            bot.send_message(chat_id, f"Вы успешно продали предмет {item_name} за {item_price} голды. Теперь у вас {user_profile['gold']} голды.", reply_markup=main_menu_keyboard)
            bot.delete_message(chat_id, call.message.message_id)  # Удаляем сообщение с кнопкой "Продать"
        else:
            bot.send_message(chat_id, "Ошибка: Неверное имя предмета.", reply_markup=main_menu_keyboard)
    else:
        bot.send_message(chat_id, "Профиль не найден. Пожалуйста, начните с команды /start.", reply_markup=main_menu_keyboard)

@bot.message_handler(commands=['help'])
def help_command(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Произошла ошибка. Пожалуйста, напишите об этом [сюда](https://t.me/pizzaway).\n\nИсходный код и тема на GitHub: [GitHub Repository](https://github.com/Sany0965/standoffcasebot)", parse_mode='Markdown', disable_web_page_preview=True)


# Функция для запуска бота
def run_bot():
    bot.polling()

if __name__ == "__main__":
    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
