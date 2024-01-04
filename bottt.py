import telebot
from telebot import types
import re


bot = telebot.TeleBot('6514143043:AAEY1YJNY7W6V6NnR9unJI9wCCOfb4LOyYQ') #токен телеграм бота
bot_status = {} #текущий статус бота
theme = {} #тема расчетов
#ипотечный кредит
cost_of_apartment = {} #стоимость квартиры
banks = ['сбербанк', 'россельхозбанк', 'втб', 'банк "открытие"', 'газпромбанк', 'тинькофф'] #список банков для ипотечного кредита
credit_rates = {banks[0]: 6,
                banks[1]: 5,
                banks[2]: 6,
                banks[3]: 6,
                banks[4]: 2.5,
                banks[5]: 5.7,} #список ставок по ипотечному кредиту
amount_of_children = {}  #количество детей в семье
bank_name = {} #название выбранного кредита для ипотечного кредита
amount_of_subsidy = {} #сумма субсидий по программе "Молодая семья"
amount_of_people = {} #количество людей в семье
data_young_family = {} #возможность получать субсидию по программе "Молодая семья"
credit_duration = {} # срок ипотечного кредита
credit_rate = {} #ставка по ипотечному кредиту
estimated_area = {} #предполагаемая площадь
data_mothers_capital = {} #наличие материнского капитала
amount_of_mothers_capital = {} #сумма материнского капитала
own_money_for_first_payment = {} #первый платеж за счет собственных средств
#образовательный кредит
banks_educational_credit = ['сбербанк', 'алмазэргиэнбанк', 'банк рнкб', 'альфа-банк', 'газпромбанк', 'втб', 'тинькофф'] #список банков для образовательного кредита
educational_credit_rates = {
    banks_educational_credit[0]: 3,
    banks_educational_credit[1]: 3,
    banks_educational_credit[2]: 3,
    banks_educational_credit[3]: 4,
    banks_educational_credit[4]: 3.9,
    banks_educational_credit[5]: 3.9,
    banks_educational_credit[6]: 3.9,
}
mins_educational_credit_size = {
    banks_educational_credit[0]: 10000,
    banks_educational_credit[1]: 10000,
    banks_educational_credit[2]: 10000,
    banks_educational_credit[3]: 10000,
    banks_educational_credit[4]: 10000,
    banks_educational_credit[5]: 100000,
}
maxs_educational_credit_size = {
    banks_educational_credit[0]: 10000000,
    banks_educational_credit[1]: 5000000,
    banks_educational_credit[2]: 5000000,
    banks_educational_credit[3]: 15000000,
    banks_educational_credit[4]: 7000000,
    banks_educational_credit[5]: 40000000,
}
mins_educational_credit_duration = {
    banks_educational_credit[0]: 0,
    banks_educational_credit[1]: 0,
    banks_educational_credit[2]: 0,
    banks_educational_credit[3]: 12,
    banks_educational_credit[4]: 13,
    banks_educational_credit[5]: 6,
}
maxs_educational_credit_duration = {
    banks_educational_credit[0]: 180,
    banks_educational_credit[1]: 180,
    banks_educational_credit[2]: 180,
    banks_educational_credit[3]: 120,
    banks_educational_credit[4]: 60,
    banks_educational_credit[5]: 60,
}
first_year_god = {
    (banks_educational_credit[0], 3): 0.0003333333,
    (banks_educational_credit[0], 4): 0.00025,
    (banks_educational_credit[0], 5): 0.0002,
    (banks_educational_credit[0], 6): 0.00016667,
    (banks_educational_credit[0], 7): 0.00014286,
    (banks_educational_credit[2], 2): 0.0005,
    (banks_educational_credit[2], 3): 0.000333,
    (banks_educational_credit[2], 4): 0.00025,
    (banks_educational_credit[2], 5): 0.0002,
    (banks_educational_credit[2], 6): 0.00016667,
    (banks_educational_credit[2], 7): 0.00014286,
    banks_educational_credit[1]: 0.001,
}
second_year_god = {
    (banks_educational_credit[0], 3): 0.001,
    (banks_educational_credit[0], 4): 0.00075,
    (banks_educational_credit[0], 5): 0.0006,
    (banks_educational_credit[0], 6): 0.0005,
    (banks_educational_credit[0], 7): 0.00042857,
    (banks_educational_credit[2], 2): 0.0015,
    (banks_educational_credit[2], 3): 0.001,
    (banks_educational_credit[2], 4): 0.00075,
    (banks_educational_credit[2], 5): 0.0006,
    (banks_educational_credit[2], 6): 0.0005,
    (banks_educational_credit[2], 7): 0.00042857,
    banks_educational_credit[1]: 0.0015,
}
last_years_god = {
    (banks_educational_credit[0], 3): 0.0025,
    (banks_educational_credit[0], 4): 0.0021875,
    (banks_educational_credit[0], 5): 0.002,
    (banks_educational_credit[0], 6): 0.001875,
    (banks_educational_credit[0], 7): 0.00178571,
    (banks_educational_credit[2], 2): 0.0025,
    (banks_educational_credit[2], 3): 0.0025,
    (banks_educational_credit[2], 4): 0.001875,
    (banks_educational_credit[2], 5): 0.0015,
    (banks_educational_credit[2], 6): 0.00125,
    (banks_educational_credit[2], 7): 0.001071,
    banks_educational_credit[1]: 0.0025,
}
main_periods_god = {
    (banks_educational_credit[0], 1): 0.00701,
    (banks_educational_credit[0], 2): 0.00702,
    (banks_educational_credit[0], 3): 0.006983,
    (banks_educational_credit[0], 4): 0.00696406,
    (banks_educational_credit[0], 5): 0.006952,
    (banks_educational_credit[0], 6): 0.006945,
    (banks_educational_credit[0], 7): 0.0069386,
    banks_educational_credit[1]: 0.007103,
    (banks_educational_credit[2], 2): 0.007072,
    (banks_educational_credit[2], 3): 0.007072,
    (banks_educational_credit[2], 4): 0.007072,
    (banks_educational_credit[2], 5): 0.007072,
    (banks_educational_credit[2], 6): 0.007072,
    (banks_educational_credit[2], 7): 0.007072,
}
first_year_sem = {
    (banks_educational_credit[0], 5): 0.0003,
    (banks_educational_credit[0], 6): 0.00025,
    (banks_educational_credit[0], 7): 0.00021429,
    (banks_educational_credit[0], 8): 0.0001875,
    (banks_educational_credit[0], 9): 0.00016667,
    (banks_educational_credit[0], 10): 0.00015,
    (banks_educational_credit[0], 11): 0.00013636,
    (banks_educational_credit[0], 12): 0.000125,
    (banks_educational_credit[0], 13): 0.00011538,
    (banks_educational_credit[0], 14): 0.00010714,
    (banks_educational_credit[2], 3): 0.000333,
    (banks_educational_credit[2], 4): 0.00025,
    (banks_educational_credit[2], 5): 0.0002,
    (banks_educational_credit[2], 6): 0.000167,
    (banks_educational_credit[2], 7): 0.000143,
    (banks_educational_credit[2], 8): 0.000125,
    (banks_educational_credit[2], 9): 0.000111,
    (banks_educational_credit[2], 10): 0.0001,
    (banks_educational_credit[2], 11): 0.000091,
    (banks_educational_credit[2], 12): 0.000083,
    (banks_educational_credit[2], 13): 0.000077,
    (banks_educational_credit[2], 14): 0.000071,
    banks_educational_credit[1]: 0.001,
}
second_year_sem = {
    (banks_educational_credit[0], 5): 0.0009,
    (banks_educational_credit[0], 6): 0.00075,
    (banks_educational_credit[0], 7): 0.00064286,
    (banks_educational_credit[0], 8): 0.0005625,
    (banks_educational_credit[0], 9): 0.0005,
    (banks_educational_credit[0], 10): 0.00045,
    (banks_educational_credit[0], 11): 0.00040909,
    (banks_educational_credit[0], 12): 0.000375,
    (banks_educational_credit[0], 13): 0.00034615,
    (banks_educational_credit[0], 14): 0.00032143,
    (banks_educational_credit[2], 3): 0.0015,
    (banks_educational_credit[2], 4): 0.001125,
    (banks_educational_credit[2], 5): 0.0009,
    (banks_educational_credit[2], 6): 0.00075,
    (banks_educational_credit[2], 7): 0.000643,
    (banks_educational_credit[2], 8): 0.000562,
    (banks_educational_credit[2], 9): 0.0005,
    (banks_educational_credit[2], 10): 0.00045,
    (banks_educational_credit[2], 11): 0.000409,
    (banks_educational_credit[2], 12): 0.000375,
    (banks_educational_credit[2], 13): 0.000346,
    (banks_educational_credit[2], 14): 0.000321,
    banks_educational_credit[1]: 0.0015,
}
last_years_sem = {
    (banks_educational_credit[0], 5): 0.0015,
    (banks_educational_credit[0], 6): 0.001875,
    (banks_educational_credit[0], 7): 0.002054,
    (banks_educational_credit[0], 8): 0.001875,
    (banks_educational_credit[0], 9): 0.001944,
    (banks_educational_credit[0], 10): 0.001792,
    (banks_educational_credit[0], 11): 0.001846,
    (banks_educational_credit[0], 12): 0.001719,
    (banks_educational_credit[0], 13): 0.001769,
    (banks_educational_credit[0], 14): 0.00166071,
    (banks_educational_credit[2], 3): 0.0025,
    (banks_educational_credit[2], 4): 0.0025,
    (banks_educational_credit[2], 5): 0.0025,
    (banks_educational_credit[2], 6): 0.002083,
    (banks_educational_credit[2], 7): 0.001786,
    (banks_educational_credit[2], 8): 0.001563,
    (banks_educational_credit[2], 9): 0.001389,
    (banks_educational_credit[2], 10): 0.00125,
    (banks_educational_credit[2], 11): 0.001136,
    (banks_educational_credit[2], 12): 0.001042,
    (banks_educational_credit[2], 13): 0.000962,
    (banks_educational_credit[2], 14): 0.000893,
    banks_educational_credit[1]: 0.0025,
}
main_periods_sem = {
    (banks_educational_credit[0], 1): 0.00696,
    (banks_educational_credit[0], 2): 0.00698,
    (banks_educational_credit[0], 3): 0.00700667,
    (banks_educational_credit[0], 4): 0.007015,
    (banks_educational_credit[0], 5): 0.007026,
    (banks_educational_credit[0], 6): 0.007005,
    (banks_educational_credit[0], 7): 0.00699143,
    (banks_educational_credit[0], 8): 0.006981,
    (banks_educational_credit[0], 9): 0.006972,
    (banks_educational_credit[0], 10): 0.006966,
    (banks_educational_credit[0], 11): 0.00696,
    (banks_educational_credit[0], 12): 0.00695583,
    (banks_educational_credit[0], 13): 0.00695231,
    (banks_educational_credit[0], 14): 0.00694857,
    banks_educational_credit[1]: 0.007103,
    (banks_educational_credit[2], 3): 0.007072,
    (banks_educational_credit[2], 4): 0.007072,
    (banks_educational_credit[2], 5): 0.007072,
    (banks_educational_credit[2], 6): 0.007072,
    (banks_educational_credit[2], 7): 0.007072,
    (banks_educational_credit[2], 8): 0.007072,
    (banks_educational_credit[2], 9): 0.007072,
    (banks_educational_credit[2], 10): 0.007072,
    (banks_educational_credit[2], 11): 0.007072,
    (banks_educational_credit[2], 12): 0.007072,
    (banks_educational_credit[2], 13): 0.007072,
    (banks_educational_credit[2], 14): 0.007072,

}
min_educational_credit_size = {}
max_educational_credit_size = {}
type_of_educational_credit = {} #вид образовательного кредита
bank_educational_credit = {} #выбранный банк для образовательного кредита
cost_of_education = {} #стоимость обучения
duration_of_education_credit = {} #длительность образовательного кредита
educational_credit_payment = {} #платеж по образовательному кредиту
educational_credit_rate = {} #ставка по образовательному кредиту
min_educational_credit_duration = {}
max_educational_credit_duration = {}
cost_of_education_lgot = {}
first_year = {}
second_year = {}
last_years = {}
main_period = {}
type_of_payment = {}
month_or_year = {}
duration_of_education_lgot = {}
#налоговый вычет
final_vichet = 0
sum_without_ndfl = {}
amount_of_children ={}
data_children_invalid = {}
data_children_vichet = {}
amount_children_vichet = {}
children_month = {}
data_3000_vichet = {}
month_3000 = {}
data_500_vichet = {}
month_500 = {}
data_social_vichet = {}
social_vichet = {}
data_im_vichet = {}
im_vichet = {}


def normalize_price(input_price):
    # Проверяем наличие букв в строке
    if any(char.isalpha() for char in input_price):
        return False

    # Убираем все пробелы из строки
    normalized_price = re.sub(r'\s', '', input_price)

    # Извлекаем только цифры из строки
    digits_only = re.sub(r'\D', '', normalized_price)

    # Преобразуем строку в число
    result = int(digits_only)

    return result

def format_price(price):
    return '{:,}'.format(price).replace(',', ' ')

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text='Ипотечный кредит')
    btn2 = types.KeyboardButton(text='Образовательный кредит')
    btn3 = types.KeyboardButton(text='Налоговый вычет')
    keyboard.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, '*ЧТО УМЕЕТ ЭТОТ БОТ?*\n........\nВыберите интересующую Вас тему', parse_mode="Markdown", reply_markup=keyboard)
    bot_status[message.chat.id] = 'waiting_for_theme'



@bot.message_handler(func=lambda message: bot_status[message.chat.id] == 'waiting_for_theme')
def get_theme(message):
    theme[message.chat.id] = message.text
    if theme[message.chat.id].lower() == 'ипотечный кредит':
        remove_keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Введите стоимость квартиры', reply_markup=remove_keyboard)
        bot_status[message.chat.id] = 'waiting_for_cost_of_apartment'
    elif theme[message.chat.id].lower() == 'образовательный кредит':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text='Льготный(с гос. поддержкой)')
        btn2 = types.KeyboardButton(text='Нельготный')
        keyboard.add(btn1, btn2)
        bot.send_message(message.chat.id, 'Какой тип образовательного кредита Вы хотите получить?', reply_markup=keyboard)
        bot_status[message.chat.id] = 'waiting_for_type_of_educational_credit'
    elif theme[message.chat.id].lower() == 'налоговый вычет':
        remove_keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Введите суммарный доход с начала года, если он больше 350 000 руб., то введите суммарный доход до того месяца, когда он не превышал 350 000 руб.', reply_markup=remove_keyboard)
        bot_status[message.chat.id] = 'waiting_for_sum_without_ndfl'
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, для выбора воспользуйтесь кнопками ниже')


@bot.message_handler(func=lambda message: bot_status[message.chat.id] == 'waiting_for_sum_without_ndfl')
def get_sum_without_ndfl(message):
    if normalize_price(message.text) and normalize_price(message.text) != 0:
        if normalize_price(message.text) <= 350000:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton(text='Да')
            btn2 = types.KeyboardButton(text='Нет')
            keyboard.add(btn1, btn2)
            sum_without_ndfl[message.chat.id] = normalize_price(message.text)
            bot_status[message.chat.id] = 'waiting_for_data_children_vichet'
            bot.send_message(message.chat.id, 'Имеете ли Вы право получать вычет на детей?', reply_markup=keyboard)
        elif int(message.text) > 350000:
            bot.send_message(message.chat.id, 'Ваш доход должен быть меньше 350 000 руб.')
    else:
        bot.send_message(message.chat.id, 'Введите корректные данные (например 100 000)')


@bot.message_handler(func=lambda message: bot_status[message.chat.id] == 'waiting_for_data_children_vichet')
def get_data_children_vichet(message):
    data_children_vichet[message.chat.id] = message.text
    if data_children_vichet[message.chat.id].lower() == 'да':
        remove_keyboard = types.ReplyKeyboardRemove()
        bot_status[message.chat.id] = 'waiting_for_amount_of_children'
        bot.send_message(message.chat.id, 'Сколько детей у Вас в семье?', reply_markup=remove_keyboard)
    elif data_children_vichet[message.chat.id].lower() == 'нет':
        bot_status[message.chat.id] = 'waiting_for_data_3000_vichet'
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text='Да')
        btn2 = types.KeyboardButton(text='Нет')
        keyboard.add(btn1, btn2)
        bot.send_message(message.chat.id, 'Относитесь ли Вы к лицам, перечисленным в пп. 1 п. 1 ст. 218 НК РФ?', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, ответьте Да или Нет')


@bot.message_handler(func=lambda message: bot_status[message.chat.id] == 'waiting_for_amount_of_children')
def get_amount_of_children(message):
    if message.text.isdigit():
        if int(message.text) == 1:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton(text='Да')
            btn2 = types.KeyboardButton(text='Нет')
            keyboard.add(btn1, btn2)
            amount_of_children[message.chat.id] = int(message.text)
            bot_status[message.chat.id] = 'waiting_for_data_children_invalid'
            bot.send_message(message.chat.id, 'Есть ли у Вашего ребенка инвалидность I или II группы?', reply_markup=keyboard)
        elif int(message.text) == 2:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton(text='0')
            btn2 = types.KeyboardButton(text='1')
            btn3 = types.KeyboardButton(text='2')
            keyboard.add(btn1, btn2, btn3)
            amount_of_children[message.chat.id] = int(message.text)
            bot_status[message.chat.id] = 'waiting_for_data_children_invalid'
            bot.send_message(message.chat.id, 'Сколько из Ваших детей имеют инвалидность I или II группы?', reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, 'Введите корректные данные (1 или 2)')
    else:
        bot.send_message(message.chat.id, 'Введите корректные данные (1 или 2)')

@bot.message_handler(func=lambda message: bot_status[message.chat.id] == 'waiting_for_data_children_invalid')
def get_data_children_invalid(message):
    data_children_invalid[message.chat.id] = message.text
    if data_children_invalid[message.chat.id].lower() == 'да':
        amount_children_vichet[message.chat.id] = 13400
        bot_status[message.chat.id] = 'waiting_for_children_month'
        bot.send_message(message.chat.id, 'Введите расчетный период в месяцах (до того месяца, когда Ваш доход не превысил 350 000 руб.) ')
    elif data_children_invalid[message.chat.id].lower() == 'нет' or data_children_invalid[message.chat.id] == '0':
        amount_children_vichet[message.chat.id] = 0
        bot_status[message.chat.id] = 'waiting_for_children_month'
        bot.send_message(message.chat.id, 'Введите расчетный период в месяцах (до того месяца, когда Ваш доход не превысил 350 000 руб.) ')
    elif data_children_invalid[message.chat.id].lower() == '1':
        amount_children_vichet[message.chat.id] = 14800
        bot_status[message.chat.id] = 'waiting_for_children_month'
        bot.send_message(message.chat.id, 'Введите расчетный период в месяцах (до того месяца, когда Ваш доход не превысил 350 000 руб.) ')
    elif data_children_invalid[message.chat.id] == '2':
        amount_children_vichet[message.chat.id] = 26800
        bot_status[message.chat.id] = 'waiting_for_children_month'
        bot.send_message(message.chat.id, 'Введите расчетный период в месяцах (до того месяца, когда Ваш доход не превысил 350 000 руб.) ')
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, для ответа воспользуйтесь кнопками ниже')


@bot.message_handler(func=lambda message: bot_status[message.chat.id] == 'waiting_for_children_month')
def get_children_month(message):
    if message.text.isdigit():
        if int(message.text) > 0:
            children_month[message.chat.id] = int(message.text)
            global final_vichet
            final_vichet += amount_children_vichet[message.chat.id] * children_month[message.chat.id]
            bot_status[message.chat.id] = 'waiting_for_data_3000_vichet'
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton(text='Да')
            btn2 = types.KeyboardButton(text='Нет')
            keyboard.add(btn1, btn2)
            bot.send_message(message.chat.id, 'Относитесь ли Вы к лицам, перечисленным в пп. 1 п. 1 ст. 218 НК РФ?', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, 'Введите корректные данные (например 2)')

@bot.message_handler(func=lambda message: bot_status[message.chat.id] == 'waiting_for_data_3000_vichet')
def get_data_3000_vichet(message):
    data_3000_vichet[message.chat.id] = message.text
    if data_3000_vichet[message.chat.id].lower() == 'да':
        remove_keyboard = types.ReplyKeyboardRemove()
        bot_status[message.chat.id] = 'waiting_for_3000_month'
        bot.send_message(message.chat.id, 'Введите расчетный период в месяцах (до того месяца, когда Ваш доход не превысил 350 000 руб.) ', reply_markup=remove_keyboard)
    elif data_3000_vichet[message.chat.id].lower() == 'нет':
        bot_status[message.chat.id] = 'waiting_for_data_500_vichet'
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text='Да')
        btn2 = types.KeyboardButton(text='Нет')
        keyboard.add(btn1, btn2)
        bot.send_message(message.chat.id, 'Относитесь ли Вы к лицам, перечисленным в пп. 2 п. 1 ст. 218 НК РФ?', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, ответьте Да или Нет')


@bot.message_handler(func=lambda message: bot_status[message.chat.id] == 'waiting_for_3000_month')
def get_3000_month(message):
    if message.text.isdigit():
        if int(message.text) > 0:
            month_3000[message.chat.id] = int(message.text)
            global final_vichet
            final_vichet += 3000 * month_3000[message.chat.id]
            bot_status[message.chat.id] = 'waiting_for_data_social_vichet'
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton(text='Да')
            btn2 = types.KeyboardButton(text='Нет')
            keyboard.add(btn1, btn2)
            bot.send_message(message.chat.id, 'Имеете ли Вы право на социальный вычет?', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, 'Введите корректные данные (например 2)')


@bot.message_handler(func=lambda message: bot_status[message.chat.id] == 'waiting_for_data_500_vichet')
def get_data_500_vichet(message):
    data_500_vichet[message.chat.id] = message.text
    if data_500_vichet[message.chat.id].lower() == 'да':
        remove_keyboard = types.ReplyKeyboardRemove()
        bot_status[message.chat.id] = 'waiting_for_500_month'
        bot.send_message(message.chat.id, 'Введите расчетный период в месяцах (до того месяца, когда Ваш доход не превысил 350 000 руб.) ', reply_markup=remove_keyboard)
    elif data_500_vichet[message.chat.id].lower() == 'нет':
        bot_status[message.chat.id] = 'waiting_for_data_social_vichet'
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text='Да')
        btn2 = types.KeyboardButton(text='Нет')
        keyboard.add(btn1, btn2)
        bot.send_message(message.chat.id, 'Имеете ли Вы право на социальный вычет?', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, ответьте Да или Нет')


@bot.message_handler(func=lambda message: bot_status[message.chat.id] == 'waiting_for_500_month')
def get_500_month(message):
    if message.text.isdigit():
        if int(message.text) > 0:
            month_500[message.chat.id] = int(message.text)
            global final_vichet
            final_vichet += 500 * month_500[message.chat.id]
            bot_status[message.chat.id] = 'waiting_for_data_social_vichet'
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton(text='Да')
            btn2 = types.KeyboardButton(text='Нет')
            keyboard.add(btn1, btn2)
            bot.send_message(message.chat.id, 'Имеете ли Вы право на социальный вычет?', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, 'Введите корректные данные (например 2)')


@bot.message_handler(func=lambda message: bot_status[message.chat.id] == 'waiting_for_data_social_vichet')
def get_data_social_vichet(message):
    data_social_vichet[message.chat.id] = message.text
    if data_social_vichet[message.chat.id].lower() == 'да':
        remove_keyboard = types.ReplyKeyboardRemove()
        bot_status[message.chat.id] = 'waiting_for_social_vichet'
        bot.send_message(message.chat.id, 'Введите сумму социального вычета', reply_markup=remove_keyboard)
    elif data_social_vichet[message.chat.id].lower() == 'нет':
        bot_status[message.chat.id] = 'waiting_for_data_im_vichet'
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text='Да')
        btn2 = types.KeyboardButton(text='Нет')
        keyboard.add(btn1, btn2)
        bot.send_message(message.chat.id, 'Имеете ли Вы право на имущественный вычет?', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, ответьте Да или Нет')


@bot.message_handler(func=lambda message: bot_status[message.chat.id] == 'waiting_for_social_vichet')
def get_social_vichet(message):
    if normalize_price(message.text):
        if normalize_price(message.text) != 0:
            social_vichet[message.chat.id] = normalize_price(message.text)
            global final_vichet
            final_vichet += social_vichet[message.chat.id]
            bot_status[message.chat.id] = 'waiting_for_data_im_vichet'
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton(text='Да')
            btn2 = types.KeyboardButton(text='Нет')
            keyboard.add(btn1, btn2)
            bot.send_message(message.chat.id, 'Имеете ли Вы право на имущественный вычет?', reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, 'Введите корректные данные (например 5000)')
    else:
        bot.send_message(message.chat.id, 'Введите корректные данные (например 5000)')

@bot.message_handler(func=lambda message: bot_status[message.chat.id] == 'waiting_for_data_im_vichet')
def get_data_im_vichet(message):
    data_im_vichet[message.chat.id] = message.text
    if data_im_vichet[message.chat.id].lower() == 'да':
        remove_keyboard = types.ReplyKeyboardRemove()
        bot_status[message.chat.id] = 'waiting_for_im_vichet'
        bot.send_message(message.chat.id, 'Введите сумму имущественного вычета', reply_markup=remove_keyboard)
    elif data_im_vichet[message.chat.id].lower() == 'нет':
        bot.send_message(message.chat.id, f'Налог - {format_price((sum_without_ndfl[message.chat.id] - final_vichet) * 0.13)} руб.\nСумма за вычетом НДФЛ - {format_price(sum_without_ndfl[message.chat.id] - (sum_without_ndfl[message.chat.id] - final_vichet) * 0.13)} руб.')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text='Ипотечный кредит')
        btn2 = types.KeyboardButton(text='Образовательный кредит')
        btn3 = types.KeyboardButton(text='Налоговый вычет')
        keyboard.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, 'Выберите интересующую Вас тему', parse_mode="Markdown", reply_markup=keyboard)
        bot_status[message.chat.id] = 'waiting_for_theme'
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, ответьте Да или Нет')


@bot.message_handler(func=lambda message: bot_status[message.chat.id] == 'waiting_for_im_vichet')
def get_im_vichet(message):
    if normalize_price(message.text):
        if normalize_price(message.text) != 0:
            im_vichet[message.chat.id] = normalize_price(message.text)
            global final_vichet
            final_vichet += im_vichet[message.chat.id]
            bot.send_message(message.chat.id, f'Налог - {format_price((sum_without_ndfl[message.chat.id] - final_vichet) * 0.13)} руб.\nСумма за вычетом НДФЛ - {format_price(sum_without_ndfl[message.chat.id] - (sum_without_ndfl[message.chat.id] - final_vichet) * 0.13)} руб.')
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton(text='Ипотечный кредит')
            btn2 = types.KeyboardButton(text='Образовательный кредит')
            btn3 = types.KeyboardButton(text='Налоговый вычет')
            keyboard.add(btn1, btn2, btn3)
            bot.send_message(message.chat.id, 'Выберите интересующую Вас тему', parse_mode="Markdown", reply_markup=keyboard)
            bot_status[message.chat.id] = 'waiting_for_theme'
        else:
            bot.send_message(message.chat.id, 'Введите корректные данные (например 5000)')
    else:
        bot.send_message(message.chat.id, 'Введите корректные данные (например 5000)')

@bot.message_handler(func=lambda message: bot_status[message.chat.id] == 'waiting_for_type_of_educational_credit')
def get_type_of_educational_credit(message):
    type_of_educational_credit[message.chat.id] = message.text.lower()
    if type_of_educational_credit[message.chat.id].lower() == 'льготный(с гос. поддержкой)' or type_of_educational_credit[message.chat.id].lower() == 'льготный':
        type_of_educational_credit[message.chat.id] = 'льготный'
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text=banks_educational_credit[0].upper())
        btn2 = types.KeyboardButton(text=banks_educational_credit[1].upper())
        btn3 = types.KeyboardButton(text=banks_educational_credit[2].upper())
        keyboard.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, 'В каком банке Вы бы хотели получить льготный образовательный кредит?', reply_markup=keyboard)
        bot_status[message.chat.id] = 'waiting_for_bank_educational_credit'

    elif type_of_educational_credit[message.chat.id].lower() == 'нельготный':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text=banks_educational_credit[3].upper())
        btn2 = types.KeyboardButton(text=banks_educational_credit[4].upper())
        btn3 = types.KeyboardButton(text=banks_educational_credit[5].upper())
        btn4 = types.KeyboardButton(text=banks_educational_credit[6].upper())
        keyboard.add(btn1, btn2, btn3, btn4)
        bot_status[message.chat.id] = 'waiting_for_bank_educational_credit'
        bot.send_message(message.chat.id, 'В каком банке Вы бы хотели получить образовательный кредит?', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, для выбора воспользуйтесь кнопками ниже')


@bot.message_handler(func=lambda message: bot_status[message.chat.id] == 'waiting_for_bank_educational_credit')
def get_bank_educational_credit(message):
    bank_educational_credit[message.chat.id] = message.text.lower()
    min_educational_credit_size[message.chat.id] = mins_educational_credit_size[bank_educational_credit[message.chat.id]]
    max_educational_credit_size[message.chat.id] = maxs_educational_credit_size[bank_educational_credit[message.chat.id]]
    min_educational_credit_duration[message.chat.id] = mins_educational_credit_duration[bank_educational_credit[message.chat.id]]
    max_educational_credit_duration[message.chat.id] = maxs_educational_credit_duration[bank_educational_credit[message.chat.id]]
    if bank_educational_credit[message.chat.id].lower() in banks_educational_credit and type_of_educational_credit[message.chat.id] == 'нельготный':
        remove_keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Введите полную стоимость образовательной программы', reply_markup=remove_keyboard)
        bot_status[message.chat.id] = 'waiting_for_cost_of_education'
    elif bank_educational_credit[message.chat.id].lower() in banks_educational_credit and type_of_educational_credit[message.chat.id] == 'льготный':
        if bank_educational_credit[message.chat.id].lower() == 'сбербанк' or bank_educational_credit[message.chat.id].lower() == 'банк рнкб':
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton(text='За семестр')
            btn2 = types.KeyboardButton(text='За год')
            keyboard.add(btn1, btn2)
            bot.send_message(message.chat.id, 'За какой период учебное заведение принимает оплату?', reply_markup=keyboard)
            bot_status[message.chat.id] = 'waiting_for_type_of_payment'
        else:
            bot_status[message.chat.id] = 'waiting_for_cost_of_education_lgot'
            bot.send_message(message.chat.id, 'Введите полную стоимость обучения')
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, для выбора воспользуйтесь кнопками ниже')


@bot.message_handler(func=lambda message: bot_status[message.chat.id] == 'waiting_for_type_of_payment')
def get_type_of_payment(message):
    type_of_payment[message.chat.id] = message.text.lower()
    if type_of_payment[message.chat.id].lower() == 'за год':
        remove_keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Введите срок обучения в годах', reply_markup=remove_keyboard)
        bot_status[message.chat.id] = 'waiting_for_duration_of_education_lgot'
    elif type_of_payment[message.chat.id].lower() == 'за семестр':
        remove_keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Введите срок обучения в семестрах', reply_markup=remove_keyboard)
        bot_status[message.chat.id] = 'waiting_for_duration_of_education_lgot'
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, для выбора воспользуйтесь кнопками ниже')

@bot.message_handler(func=lambda message: bot_status[message.chat.id] == 'waiting_for_duration_of_education_lgot')
def get_duration_of_education_lgot(message):
    if message.text.isdigit() and (int(message.text) > 0 and int(message.text) < 8 and type_of_payment[message.chat.id].lower() == 'за год') or (int(message.text) > 0 and int(message.text) < 15 and type_of_payment[message.chat.id].lower() == 'за семестр'):
        duration_of_education_lgot[message.chat.id] = int(message.text)
        bot_status[message.chat.id] = 'waiting_for_cost_of_education_lgot'
        bot.send_message(message.chat.id, 'Введите полную стоимость обучения')
    else:
        bot.send_message(message.chat.id, 'Введите корректные данные (например 4)')

@bot.message_handler(func=lambda message: bot_status[message.chat.id] == 'waiting_for_cost_of_education_lgot')
def get_cost_of_education_lgot(message):
    if normalize_price(message.text):
        if normalize_price(message.text) != 0 and normalize_price(message.text) >= min_educational_credit_size[message.chat.id] and normalize_price(message.text) <= max_educational_credit_size[message.chat.id]:
            if bank_educational_credit[message.chat.id].lower() == 'алмазэргиэнбанк':
                cost_of_education_lgot[message.chat.id] = normalize_price(message.text)
                first_year[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * first_year_god[bank_educational_credit[message.chat.id]], 2)
                second_year[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * second_year_god[bank_educational_credit[message.chat.id]], 2)
                last_years[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * last_years_god[bank_educational_credit[message.chat.id]], 2)
                main_period[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * main_periods_god[bank_educational_credit[message.chat.id]], 2)
                bot.send_message(message.chat.id,f'Ежемесячный платеж:\nВ 1-й год обучения - {first_year[message.chat.id]} руб.\nВо 2-й год обучения - {second_year[message.chat.id]} руб.\nС 3-го года до конца обучения + 9 месяцев после окончания - {last_years[message.chat.id]} руб.\nПосле обучения - {main_period[message.chat.id]} руб.\nСумма всех платежей - {format_price(round(first_year[message.chat.id] * 12 + second_year[message.chat.id] * 12 + last_years[message.chat.id] * 33 + main_period[message.chat.id] * 180, 2))} руб.\nПереплата - {format_price(round((first_year[message.chat.id] * 12 + second_year[message.chat.id] * 12 + last_years[message.chat.id] * 33 + main_period[message.chat.id] * 180) - cost_of_education_lgot[message.chat.id], 2))} руб.')
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton(text='Ипотечный кредит')
                btn2 = types.KeyboardButton(text='Образовательный кредит')
                btn3 = types.KeyboardButton(text='Налоговый вычет')
                keyboard.add(btn1, btn2, btn3)
                bot.send_message(message.chat.id, 'Выберите интересующую Вас тему', parse_mode="Markdown",reply_markup=keyboard)
                bot_status[message.chat.id] = 'waiting_for_theme'
            elif type_of_payment[message.chat.id] == 'за год':
                if bank_educational_credit[message.chat.id].lower() == 'сбербанк':
                    if duration_of_education_lgot[message.chat.id] == 1:
                        cost_of_education_lgot[message.chat.id] = normalize_price(message.text)
                        last_years[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * 0.001, 2)
                        main_period[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * 0.00701, 2)
                        bot.send_message(message.chat.id, f'Ежемесячный платеж:\nВ течение года + 9 месяцев - {last_years[message.chat.id]} руб.\nПосле обучения - {main_period[message.chat.id]} руб.\nСумма всех платежей - {format_price(last_years[message.chat.id] * 21 + main_period[message.chat.id] * 180)} руб.\nПереплата - {format_price(round((last_years[message.chat.id] * 21 + main_period[message.chat.id] * 180) - cost_of_education_lgot[message.chat.id], 2))} руб.')
                        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        btn1 = types.KeyboardButton(text='Ипотечный кредит')
                        btn2 = types.KeyboardButton(text='Образовательный кредит')
                        btn3 = types.KeyboardButton(text='Налоговый вычет')
                        keyboard.add(btn1, btn2, btn3)
                        bot.send_message(message.chat.id, 'Выберите интересующую Вас тему', parse_mode="Markdown", reply_markup=keyboard)
                        bot_status[message.chat.id] = 'waiting_for_theme'
                    if duration_of_education_lgot[message.chat.id] == 2:
                        cost_of_education_lgot[message.chat.id] = normalize_price(message.text)
                        first_year[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * 0.0005, 2)
                        last_years[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * 0.0015, 2)
                        main_period[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * 0.00702, 2)
                        bot.send_message(message.chat.id, f'Ежемесячный платеж:\nВ 1-й год - {first_year[message.chat.id]}\nВо 2-й год + 9 месяцев - {last_years[message.chat.id]} руб.\nПосле обучения - {main_period[message.chat.id]} руб.\nСумма всех платежей - {format_price(round(first_year[message.chat.id] * 12 + last_years[message.chat.id] * 21 + main_period[message.chat.id] * 180, 2))} руб.\nПереплата - {format_price(round((first_year[message.chat.id] * 12 + last_years[message.chat.id] * 21 + main_period[message.chat.id] * 180) - cost_of_education_lgot[message.chat.id], 2))} руб.')
                        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        btn1 = types.KeyboardButton(text='Ипотечный кредит')
                        btn2 = types.KeyboardButton(text='Образовательный кредит')
                        btn3 = types.KeyboardButton(text='Налоговый вычет')
                        keyboard.add(btn1, btn2, btn3)
                        bot.send_message(message.chat.id, 'Выберите интересующую Вас тему', parse_mode="Markdown", reply_markup=keyboard)
                        bot_status[message.chat.id] = 'waiting_for_theme'
                    if duration_of_education_lgot[message.chat.id] >=3:
                        cost_of_education_lgot[message.chat.id] = normalize_price(message.text)
                        first_year[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * first_year_god[(bank_educational_credit[message.chat.id], duration_of_education_lgot[message.chat.id])], 2)
                        second_year[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * second_year_god[(bank_educational_credit[message.chat.id], duration_of_education_lgot[message.chat.id])], 2)
                        last_years[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * last_years_god[(bank_educational_credit[message.chat.id], duration_of_education_lgot[message.chat.id])], 2)
                        main_period[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * main_periods_god[(bank_educational_credit[message.chat.id], duration_of_education_lgot[message.chat.id])], 2)
                        bot.send_message(message.chat.id, f'Ежемесячный платеж:\nВ 1-й год обучения - {first_year[message.chat.id]} руб.\nВо 2-й год обучения - {second_year[message.chat.id]} руб.\nС 3-го года до конца обучения + 9 месяцев после окончания - {last_years[message.chat.id]} руб.\nПосле обучения - {main_period[message.chat.id]} руб.\nСумма всех платежей - {format_price(round(first_year[message.chat.id] * 12 + second_year[message.chat.id] * 12 + last_years[message.chat.id] * (12 * (duration_of_education_lgot[message.chat.id] - 2) + 9) + main_period[message.chat.id] * 180, 2))} руб.\nПереплата - {format_price(round((first_year[message.chat.id] * 12 + second_year[message.chat.id] * 12 + last_years[message.chat.id] * (12 * (duration_of_education_lgot[message.chat.id] - 2) + 9) + main_period[message.chat.id] * 180) - cost_of_education_lgot[message.chat.id], 2))} руб.')
                        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        btn1 = types.KeyboardButton(text='Ипотечный кредит')
                        btn2 = types.KeyboardButton(text='Образовательный кредит')
                        btn3 = types.KeyboardButton(text='Налоговый вычет')
                        keyboard.add(btn1, btn2, btn3)
                        bot.send_message(message.chat.id, 'Выберите интересующую Вас тему', parse_mode="Markdown", reply_markup=keyboard)
                        bot_status[message.chat.id] = 'waiting_for_theme'
                if bank_educational_credit[message.chat.id].lower() == 'банк рнкб':
                    if duration_of_education_lgot[message.chat.id] == 1:
                        cost_of_education_lgot[message.chat.id] = normalize_price(message.text)
                        first_year[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * 0.001, 2)
                        second_year[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * 0.0015, 2)
                        last_years[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * 0.007056, 2)
                        bot.send_message(message.chat.id, f'Ежемесячный платеж:\nВ 1-й год обучения - {first_year[message.chat.id]} руб.\nВо 2-й год обучения - {second_year[message.chat.id]} руб.\nПосле обучения - {main_period[message.chat.id]} руб.\nСумма всех платежей - {format_price(round(first_year[message.chat.id] * 12 + second_year[message.chat.id] * 12 + main_period[message.chat.id] * 180, 2))} руб.\nПереплата - {format_price(round((first_year[message.chat.id] * 12 + second_year[message.chat.id] * 12+ main_period[message.chat.id] * 180) - cost_of_education_lgot[message.chat.id], 2))} руб.')
                        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        btn1 = types.KeyboardButton(text='Ипотечный кредит')
                        btn2 = types.KeyboardButton(text='Образовательный кредит')
                        btn3 = types.KeyboardButton(text='Налоговый вычет')
                        keyboard.add(btn1, btn2, btn3)
                        bot.send_message(message.chat.id, 'Выберите интересующую Вас тему', parse_mode="Markdown", reply_markup=keyboard)
                        bot_status[message.chat.id] = 'waiting_for_theme'
                    if duration_of_education_lgot[message.chat.id] >=2:
                        cost_of_education_lgot[message.chat.id] = normalize_price(message.text)
                        first_year[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * first_year_god[(bank_educational_credit[message.chat.id], duration_of_education_lgot[message.chat.id])], 2)
                        second_year[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * second_year_god[(bank_educational_credit[message.chat.id], duration_of_education_lgot[message.chat.id])], 2)
                        last_years[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * last_years_god[(bank_educational_credit[message.chat.id], duration_of_education_lgot[message.chat.id])], 2)
                        main_period[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * main_periods_god[(bank_educational_credit[message.chat.id], duration_of_education_lgot[message.chat.id])], 2)
                        bot.send_message(message.chat.id, f'Ежемесячный платеж:\nВ 1-й год обучения - {first_year[message.chat.id]} руб.\nВо 2-й год обучения - {second_year[message.chat.id]} руб.\nС 3-го года до конца обучения + 9 месяцев после окончания - {last_years[message.chat.id]} руб.\nПосле обучения - {main_period[message.chat.id]} руб.\nСумма всех платежей - {format_price(round(first_year[message.chat.id] * 12 + second_year[message.chat.id] * 12 + last_years[message.chat.id] * (12 * (duration_of_education_lgot[message.chat.id] - 2) + 9) + main_period[message.chat.id] * 180, 2))} руб.\nПереплата - {format_price(round((first_year[message.chat.id] * 12 + second_year[message.chat.id] * 12 + last_years[message.chat.id] * (12 * (duration_of_education_lgot[message.chat.id] - 2) + 9) + main_period[message.chat.id] * 180) - cost_of_education_lgot[message.chat.id], 2))} руб.')
                        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        btn1 = types.KeyboardButton(text='Ипотечный кредит')
                        btn2 = types.KeyboardButton(text='Образовательный кредит')
                        btn3 = types.KeyboardButton(text='Налоговый вычет')
                        keyboard.add(btn1, btn2, btn3)
                        bot.send_message(message.chat.id, 'Выберите интересующую Вас тему', parse_mode="Markdown", reply_markup=keyboard)
                        bot_status[message.chat.id] = 'waiting_for_theme'
            elif type_of_payment[message.chat.id] == 'за семестр':
                if bank_educational_credit[message.chat.id].lower() == 'сбербанк':
                    if duration_of_education_lgot[message.chat.id] == 1:
                        cost_of_education_lgot[message.chat.id] = normalize_price(message.text)
                        last_years[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * 0.001, 2)
                        main_period[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * 0.00696, 2)
                        bot.send_message(message.chat.id, f'Ежемесячный платеж:\nВ течение полугода - {last_years[message.chat.id]} руб.\nПосле обучения - {main_period[message.chat.id]} руб.\nСумма всех платежей - {format_price(last_years[message.chat.id] * 6 + main_period[message.chat.id] * 180)} руб.\nПереплата - {format_price(round((last_years[message.chat.id] * 6 + main_period[message.chat.id] * 180) - cost_of_education_lgot[message.chat.id], 2))} руб.')
                        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        btn1 = types.KeyboardButton(text='Ипотечный кредит')
                        btn2 = types.KeyboardButton(text='Образовательный кредит')
                        btn3 = types.KeyboardButton(text='Налоговый вычет')
                        keyboard.add(btn1, btn2, btn3)
                        bot.send_message(message.chat.id, 'Выберите интересующую Вас тему', parse_mode="Markdown", reply_markup=keyboard)
                        bot_status[message.chat.id] = 'waiting_for_theme'
                    if duration_of_education_lgot[message.chat.id] == 2:
                        cost_of_education_lgot[message.chat.id] = normalize_price(message.text)
                        last_years[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * 0.00075, 2)
                        main_period[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * 0.00698, 2)
                        bot.send_message(message.chat.id, f'Ежемесячный платеж:\nВ течение года + 9 месяцев - {last_years[message.chat.id]}\nПосле обучения - {main_period[message.chat.id]} руб.\nСумма всех платежей - {format_price(round(last_years[message.chat.id] * 21 + main_period[message.chat.id] * 180, 2))} руб.\nПереплата - {format_price(round((last_years[message.chat.id] * 21 + main_period[message.chat.id] * 180) - cost_of_education_lgot[message.chat.id], 2))} руб.')
                        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        btn1 = types.KeyboardButton(text='Ипотечный кредит')
                        btn2 = types.KeyboardButton(text='Образовательный кредит')
                        btn3 = types.KeyboardButton(text='Налоговый вычет')
                        keyboard.add(btn1, btn2, btn3)
                        bot.send_message(message.chat.id, 'Выберите интересующую Вас тему', parse_mode="Markdown", reply_markup=keyboard)
                        bot_status[message.chat.id] = 'waiting_for_theme'
                    if duration_of_education_lgot[message.chat.id] == 3:
                        cost_of_education_lgot[message.chat.id] = normalize_price(message.text)
                        first_year[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * 0.0005, 2)
                        last_years[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * 0.001, 2)
                        main_period[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * 0.00700667, 2)
                        bot.send_message(message.chat.id, f'Ежемесячный платеж:\nВ 1-й год - {first_year[message.chat.id]}\nВ течение полугода + 9 месяцев - {last_years[message.chat.id]}\nПосле обучения - {main_period[message.chat.id]} руб.\nСумма всех платежей - {format_price(round(first_year[message.chat.id] * 12 + last_years[message.chat.id] * 15 + main_period[message.chat.id] * 180, 2))} руб.\nПереплата - {format_price(round(first_year[message.chat.id] * 12 + last_years[message.chat.id] * 15 + main_period[message.chat.id] * 180 - cost_of_education_lgot[message.chat.id], 2))} руб.')
                        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        btn1 = types.KeyboardButton(text='Ипотечный кредит')
                        btn2 = types.KeyboardButton(text='Образовательный кредит')
                        btn3 = types.KeyboardButton(text='Налоговый вычет')
                        keyboard.add(btn1, btn2, btn3)
                        bot.send_message(message.chat.id, 'Выберите интересующую Вас тему', parse_mode="Markdown", reply_markup=keyboard)
                        bot_status[message.chat.id] = 'waiting_for_theme'
                    if duration_of_education_lgot[message.chat.id] == 4:
                        cost_of_education_lgot[message.chat.id] = normalize_price(message.text)
                        first_year[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * 0.000375, 2)
                        last_years[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * 0.001125, 2)
                        main_period[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * 0.007015, 2)
                        bot.send_message(message.chat.id, f'Ежемесячный платеж:\nВ 1-й год - {first_year[message.chat.id]}\nВо 2-й год + 9 месяцев - {last_years[message.chat.id]}\nПосле обучения - {main_period[message.chat.id]} руб.\nСумма всех платежей - {format_price(round(first_year[message.chat.id] * 12 + last_years[message.chat.id] * 21 + main_period[message.chat.id] * 180, 2))} руб.\nПереплата - {format_price(round(first_year[message.chat.id] * 12 + last_years[message.chat.id] * 21 + main_period[message.chat.id] * 180 - cost_of_education_lgot[message.chat.id], 2))} руб.')
                        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        btn1 = types.KeyboardButton(text='Ипотечный кредит')
                        btn2 = types.KeyboardButton(text='Образовательный кредит')
                        btn3 = types.KeyboardButton(text='Налоговый вычет')
                        keyboard.add(btn1, btn2, btn3)
                        bot.send_message(message.chat.id, 'Выберите интересующую Вас тему', parse_mode="Markdown", reply_markup=keyboard)
                        bot_status[message.chat.id] = 'waiting_for_theme'
                    if duration_of_education_lgot[message.chat.id] >=5:
                        cost_of_education_lgot[message.chat.id] = normalize_price(message.text)
                        first_year[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * first_year_sem[(bank_educational_credit[message.chat.id], duration_of_education_lgot[message.chat.id])], 2)
                        second_year[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * second_year_sem[(bank_educational_credit[message.chat.id], duration_of_education_lgot[message.chat.id])], 2)
                        last_years[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * last_years_sem[(bank_educational_credit[message.chat.id], duration_of_education_lgot[message.chat.id])], 2)
                        main_period[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * main_periods_sem[(bank_educational_credit[message.chat.id], duration_of_education_lgot[message.chat.id])], 2)
                        bot.send_message(message.chat.id, f'Ежемесячный платеж:\nВ 1-й год обучения - {first_year[message.chat.id]} руб.\nВо 2-й год обучения - {second_year[message.chat.id]} руб.\nС 3-го года до конца обучения + 9 месяцев после окончания - {last_years[message.chat.id]} руб.\nПосле обучения - {main_period[message.chat.id]} руб.\nСумма всех платежей - {format_price(round(first_year[message.chat.id] * 12 + second_year[message.chat.id] * 12 + last_years[message.chat.id] * (6 * (duration_of_education_lgot[message.chat.id] - 4) + 9) + main_period[message.chat.id] * 180, 2))} руб.\nПереплата - {format_price(round((first_year[message.chat.id] * 12 + second_year[message.chat.id] * 12 + last_years[message.chat.id] * (6 * (duration_of_education_lgot[message.chat.id] - 4) + 9) + main_period[message.chat.id] * 180) - cost_of_education_lgot[message.chat.id], 2))} руб.')
                        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        btn1 = types.KeyboardButton(text='Ипотечный кредит')
                        btn2 = types.KeyboardButton(text='Образовательный кредит')
                        btn3 = types.KeyboardButton(text='Налоговый вычет')
                        keyboard.add(btn1, btn2, btn3)
                        bot.send_message(message.chat.id, 'Выберите интересующую Вас тему', parse_mode="Markdown", reply_markup=keyboard)
                        bot_status[message.chat.id] = 'waiting_for_theme'
                if bank_educational_credit[message.chat.id].lower() == 'банк рнкб':
                    if duration_of_education_lgot[message.chat.id] == 1:
                        cost_of_education_lgot[message.chat.id] = normalize_price(message.text)
                        first_year[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * 0.001, 2)
                        first_year[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * 0.0015, 2)
                        main_period[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * 0.007022, 2)
                        bot.send_message(message.chat.id, f'Ежемесячный платеж:\nВ 1-й год обучения - {first_year[message.chat.id]} руб.\nВо 2-й год обучения - {second_year[message.chat.id]} руб.\nПосле обучения - {main_period[message.chat.id]} руб.\nСумма всех платежей - {format_price(round(first_year[message.chat.id] * 12 + second_year[message.chat.id] * 12 + main_period[message.chat.id] * 180, 2))} руб.\nПереплата - {format_price(round((first_year[message.chat.id] * 12 + second_year[message.chat.id] * 12 + main_period[message.chat.id] * 180) - cost_of_education_lgot[message.chat.id], 2))} руб.')
                        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        btn1 = types.KeyboardButton(text='Ипотечный кредит')
                        btn2 = types.KeyboardButton(text='Образовательный кредит')
                        btn3 = types.KeyboardButton(text='Налоговый вычет')
                        keyboard.add(btn1, btn2, btn3)
                        bot.send_message(message.chat.id, 'Выберите интересующую Вас тему', parse_mode="Markdown", reply_markup=keyboard)
                        bot_status[message.chat.id] = 'waiting_for_theme'
                    if duration_of_education_lgot[message.chat.id] == 2:
                        cost_of_education_lgot[message.chat.id] = normalize_price(message.text)
                        first_year[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * 0.0005, 2)
                        second_year[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * 0.0015, 2)
                        main_period[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * 0.007056, 2)
                        bot.send_message(message.chat.id, f'Ежемесячный платеж:\nВ 1-й год обучения - {first_year[message.chat.id]} руб.\nВо 2-й год обучения - {second_year[message.chat.id]} руб.\nПосле обучения - {main_period[message.chat.id]} руб.\nСумма всех платежей - {format_price(round(first_year[message.chat.id] * 12 + second_year[message.chat.id] * 12 + main_period[message.chat.id] * 180, 2))} руб.\nПереплата - {format_price(round((first_year[message.chat.id] * 12 + second_year[message.chat.id] * 12 + main_period[message.chat.id] * 180) - cost_of_education_lgot[message.chat.id], 2))} руб.')
                        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        btn1 = types.KeyboardButton(text='Ипотечный кредит')
                        btn2 = types.KeyboardButton(text='Образовательный кредит')
                        btn3 = types.KeyboardButton(text='Налоговый вычет')
                        keyboard.add(btn1, btn2, btn3)
                        bot.send_message(message.chat.id, 'Выберите интересующую Вас тему', parse_mode="Markdown", reply_markup=keyboard)
                        bot_status[message.chat.id] = 'waiting_for_theme'
                    if duration_of_education_lgot[message.chat.id] >=3:
                        cost_of_education_lgot[message.chat.id] = normalize_price(message.text)
                        first_year[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * first_year_sem[(bank_educational_credit[message.chat.id], duration_of_education_lgot[message.chat.id])], 2)
                        second_year[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * second_year_sem[(bank_educational_credit[message.chat.id], duration_of_education_lgot[message.chat.id])], 2)
                        last_years[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * last_years_sem[(bank_educational_credit[message.chat.id], duration_of_education_lgot[message.chat.id])], 2)
                        main_period[message.chat.id] = round(cost_of_education_lgot[message.chat.id] * main_periods_sem[(bank_educational_credit[message.chat.id], duration_of_education_lgot[message.chat.id])], 2)
                        bot.send_message(message.chat.id, f'Ежемесячный платеж:\nВ 1-й год обучения - {first_year[message.chat.id]} руб.\nВо 2-й год обучения - {second_year[message.chat.id]} руб.\nС 3-го года до конца обучения + 9 месяцев после окончания - {last_years[message.chat.id]} руб.\nПосле обучения - {main_period[message.chat.id]} руб.\nСумма всех платежей - {format_price(round(first_year[message.chat.id] * 12 + second_year[message.chat.id] * 12 + last_years[message.chat.id] * (6 * (duration_of_education_lgot[message.chat.id] - 4) + 9) + main_period[message.chat.id] * 180, 2))} руб.\nПереплата - {format_price(round((first_year[message.chat.id] * 12 + second_year[message.chat.id] * 12 + last_years[message.chat.id] * (6 * (duration_of_education_lgot[message.chat.id] - 4) + 9) + main_period[message.chat.id] * 180) - cost_of_education_lgot[message.chat.id], 2))} руб.')
                        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        btn1 = types.KeyboardButton(text='Ипотечный кредит')
                        btn2 = types.KeyboardButton(text='Образовательный кредит')
                        btn3 = types.KeyboardButton(text='Налоговый вычет')
                        keyboard.add(btn1, btn2, btn3)
                        bot.send_message(message.chat.id, 'Выберите интересующую Вас тему', parse_mode="Markdown", reply_markup=keyboard)
                        bot_status[message.chat.id] = 'waiting_for_theme'

        elif normalize_price(message.text) < min_educational_credit_size[message.chat.id] or normalize_price(message.text) > max_educational_credit_size[message.chat.id]:
            bot.send_message(message.chat.id, f'Пожалуйста, введите другую сумму кредита.\nМинимальная сумма для данного банка - {format_price(min_educational_credit_size[message.chat.id])} руб.\nМаксимальная сумма для данного банка - {format_price(max_educational_credit_size[message.chat.id])} руб.')
        else:
            bot.send_message(message.chat.id, 'Введите корректные данные (например 1 000 000)')
    else:
        bot.send_message(message.chat.id, 'Введите корректные данные (например 1 000 000)')


@bot.message_handler(func=lambda message: bot_status[message.chat.id] == 'waiting_for_cost_of_education')
def get_cost_of_education(message):
    if normalize_price(message.text):
        if normalize_price(message.text) != 0 and normalize_price(message.text) >= min_educational_credit_size[message.chat.id] and normalize_price(message.text) <= max_educational_credit_size[message.chat.id]:
            cost_of_education[message.chat.id] = normalize_price(message.text)
            bot_status[message.chat.id] = 'waiting_for_month_or_year'
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton(text='Годы')
            btn2 = types.KeyboardButton(text='Месяцы')
            keyboard.add(btn1, btn2)
            bot.send_message(message.chat.id, 'В каком формате Вы бы хотели ввести срок кредита? Годы или месяцы?',reply_markup=keyboard)
        elif normalize_price(message.text) < min_educational_credit_size[message.chat.id] or normalize_price(message.text) > max_educational_credit_size[message.chat.id]:
            bot.send_message(message.chat.id, f'Пожалуйста, введите другой срок кредита.\nМинимальная сумма для данного банка - {min_educational_credit_size[message.chat.id]} руб.\nМаксимальная сумма для данного банка - {max_educational_credit_size[message.chat.id]} руб.')
        else:
            bot.send_message(message.chat.id, 'Введите корректные данные (например 1 000 000)')
    else:
        bot.send_message(message.chat.id, 'Введите корректные данные (например 1 000 000)')


@bot.message_handler(func=lambda message: bot_status[message.chat.id] == 'waiting_for_month_or_year')
def get_month_or_year(message):
    month_or_year[message.chat.id] = message.text
    if month_or_year[message.chat.id].lower() == 'годы':
        remove_keyboard = types.ReplyKeyboardRemove()
        bot_status[message.chat.id] = 'waiting_for_duration_of_education_credit_years'
        bot.send_message(message.chat.id, 'На сколько лет Вы бы хотели взять кредит?', reply_markup=remove_keyboard)
    elif month_or_year[message.chat.id].lower() == 'месяцы':
        remove_keyboard = types.ReplyKeyboardRemove()
        bot_status[message.chat.id] = 'waiting_for_duration_of_education_credit_months'
        bot.send_message(message.chat.id, 'На сколько месяцев Вы бы хотели взять кредит?', reply_markup=remove_keyboard)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, для ответа воспользуйтесь кнопками ниже')


@bot.message_handler(func=lambda message: bot_status[message.chat.id] == 'waiting_for_duration_of_education_credit_months')
def get_duration_of_education_credit_months(message):
    if message.text.isdigit():
        if int(message.text) != 0 and int(message.text) >= min_educational_credit_duration[message.chat.id] and int(message.text) <= max_educational_credit_duration[message.chat.id]:
            duration_of_education_credit[message.chat.id] = int(message.text)
            if type_of_educational_credit[message.chat.id].lower() == 'нельготный':
                educational_credit_rate[message.chat.id] = educational_credit_rates[bank_educational_credit[message.chat.id]] / 100
                educational_credit_payment[message.chat.id] = round(cost_of_education[message.chat.id] * (educational_credit_rate[message.chat.id] / 12 * (1 + educational_credit_rate[message.chat.id] / 12) ** (duration_of_education_credit[message.chat.id])) / ((1 + educational_credit_rate[message.chat.id] / 12) ** (duration_of_education_credit[message.chat.id]) - 1), 2)
                bot.send_message(message.chat.id, f'Стоимость обучения - {format_price(cost_of_education[message.chat.id])} руб.\nСтавка - {educational_credit_rates[bank_educational_credit[message.chat.id]]} %\nЕжемесячный платеж - {format_price(educational_credit_payment[message.chat.id])} руб.\nОбщая сумма - {format_price(round(educational_credit_payment[message.chat.id] * duration_of_education_credit[message.chat.id], 2))} руб.\nПереплата - {format_price(round(educational_credit_payment[message.chat.id] * duration_of_education_credit[message.chat.id] - cost_of_education[message.chat.id], 2))} руб.')
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton(text='Ипотечный кредит')
                btn2 = types.KeyboardButton(text='Образовательный кредит')
                btn3 = types.KeyboardButton(text='Налоговый вычет')
                keyboard.add(btn1, btn2, btn3)
                bot.send_message(message.chat.id, 'Выберите интересующую Вас тему', parse_mode="Markdown", reply_markup=keyboard)
                bot_status[message.chat.id] = 'waiting_for_theme'
        elif int(message.text) < min_educational_credit_duration[message.chat.id] or int(message.text) > max_educational_credit_duration[message.chat.id]:
            bot.send_message(message.chat.id, f'Пожалуйста, введите другой срок кредита.\nМинимальный срок для данного банка - {min_educational_credit_duration[message.chat.id]} месяцев\nМаксимальный срок для данного банка - {max_educational_credit_duration[message.chat.id]} месяцев')
    else:
        bot.send_message(message.chat.id, 'Введите корректные данные (например 24)')


@bot.message_handler(func=lambda message: bot_status[message.chat.id] == 'waiting_for_duration_of_education_credit_years')
def get_duration_of_education_credit_years(message):
    if message.text.isdigit():
        if int(message.text) != 0 and int(message.text) >= min_educational_credit_duration[message.chat.id] / 12 and int(message.text) <= max_educational_credit_duration[message.chat.id] / 12:
            duration_of_education_credit[message.chat.id] = int(message.text) * 12
            if type_of_educational_credit[message.chat.id].lower() == 'нельготный':
                educational_credit_rate[message.chat.id] = educational_credit_rates[bank_educational_credit[message.chat.id]] / 100
                educational_credit_payment[message.chat.id] = round(cost_of_education[message.chat.id] * (educational_credit_rate[message.chat.id] / 12 * (1 + educational_credit_rate[message.chat.id] / 12) ** (duration_of_education_credit[message.chat.id])) / ((1 + educational_credit_rate[message.chat.id] / 12) ** (duration_of_education_credit[message.chat.id]) - 1), 2)
                bot.send_message(message.chat.id, f'Стоимость обучения - {format_price(cost_of_education[message.chat.id])} руб.\nСтавка - {format_price(educational_credit_rates[bank_educational_credit[message.chat.id]])} %\nЕжемесячный платеж - {format_price(educational_credit_payment[message.chat.id])} руб.\nОбщая сумма - {format_price(round(educational_credit_payment[message.chat.id] * duration_of_education_credit[message.chat.id], 2))} руб.\nПереплата - {format_price(round(educational_credit_payment[message.chat.id] * duration_of_education_credit[message.chat.id] - cost_of_education[message.chat.id], 2))} руб.')
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton(text='Ипотечный кредит')
                btn2 = types.KeyboardButton(text='Образовательный кредит')
                btn3 = types.KeyboardButton(text='Налоговый вычет')
                keyboard.add(btn1, btn2, btn3)
                bot.send_message(message.chat.id, 'Выберите интересующую Вас тему', parse_mode="Markdown", reply_markup=keyboard)
                bot_status[message.chat.id] = 'waiting_for_theme'
        elif int(message.text) < min_educational_credit_duration[message.chat.id] or int(message.text) > max_educational_credit_duration[message.chat.id]:
            bot.send_message(message.chat.id, f'Пожалуйста, введите другой срок кредита.\nМинимальный срок для данного банка - {min_educational_credit_duration[message.chat.id]} месяцев\nМаксимальный срок для данного банка - {max_educational_credit_duration[message.chat.id]} месяцев')
    else:
        bot.send_message(message.chat.id, 'Введите корректные данные (например 2)')

@bot.message_handler(func=lambda message: bot_status[message.chat.id] == 'waiting_for_cost_of_apartment')
def get_cost_of_apartment(message):
    if normalize_price(message.text):
        if normalize_price(message.text) != 0:
            cost_of_apartment[message.chat.id] = normalize_price(message.text)
            bot_status[message.chat.id] = 'waiting_for_data_young_family'
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton(text='Да')
            btn2 = types.KeyboardButton(text='Нет')
            keyboard.add(btn1, btn2)
            bot.send_message(message.chat.id, 'У Вас есть возможность получить субсидию по программе «Молодая семья»?', reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, 'Введите корректные данные (например 5 000 000)')
    else:
        bot.send_message(message.chat.id, 'Введите корректные данные (например 5 000 000)')

@bot.message_handler(func=lambda message: bot_status[message.chat.id] == 'waiting_for_data_young_family')
def get_data_young_family(message):
    data_young_family[message.chat.id] = message.text
    if data_young_family[message.chat.id].lower() == 'да':
        remove_keyboard = types.ReplyKeyboardRemove()
        bot_status[message.chat.id] = 'waiting_for_amount_of_people'
        bot.send_message(message.chat.id, 'Сколько человек в Вашей семье?', reply_markup=remove_keyboard)
    elif data_young_family[message.chat.id].lower() == 'нет':
        amount_of_children[message.chat.id] = 0
        estimated_area[message.chat.id] = 0
        amount_of_subsidy[message.chat.id] = 0
        bot_status[message.chat.id] = 'waiting_for_data_mothers_capital'
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text='Да')
        btn2 = types.KeyboardButton(text='Нет')
        keyboard.add(btn1, btn2)
        bot.send_message(message.chat.id, 'Есть ли у Вас материнский капитал?',reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, ответьте Да или Нет')



@bot.message_handler(func=lambda message: bot_status[message.chat.id] == 'waiting_for_amount_of_people')
def get_amount_of_people(message):
    if message.text.isdigit():
        if int(message.text) > 1:
            amount_of_people[message.chat.id] = int(message.text)
            amount_of_children[message.chat.id] = amount_of_people[message.chat.id] - 2
            bot_status[message.chat.id] = 'waiting_for_data_mothers_capital'
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton(text='Да')
            btn2 = types.KeyboardButton(text='Нет')
            keyboard.add(btn1, btn2)
            bot.send_message(message.chat.id, 'Есть ли у Вас материнский капитал?', reply_markup=keyboard)
            if amount_of_people[message.chat.id] == 2:
                estimated_area[message.chat.id] = 42
            else:
                estimated_area[message.chat.id] = amount_of_people[message.chat.id] * 18

    else:
        bot.send_message(message.chat.id, 'Введите корректные данные (например 2 или больше)')


@bot.message_handler(func=lambda message: bot_status[message.chat.id] == 'waiting_for_data_mothers_capital')
def get_data_mothers_capital(message):
    data_mothers_capital[message.chat.id] = message.text
    if data_mothers_capital[message.chat.id].lower() == 'да':
        remove_keyboard = types.ReplyKeyboardRemove()
        bot_status[message.chat.id] = 'waiting_for_amount_of_mothers_capital'
        bot.send_message(message.chat.id, 'Введите сумму', reply_markup=remove_keyboard)
    elif data_mothers_capital[message.chat.id].lower() == 'нет':
        bot_status[message.chat.id] = 'waiting_for_bank_name'
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton(text=banks[0].upper())
        btn2 = types.KeyboardButton(text=banks[1].upper())
        btn3 = types.KeyboardButton(text=banks[2].upper())
        btn4 = types.KeyboardButton(text=banks[3].upper())
        btn5 = types.KeyboardButton(text=banks[4].upper())
        btn6 = types.KeyboardButton(text=banks[5].upper())
        keyboard.add(btn1, btn2, btn3, btn4, btn5, btn6)
        bot.send_message(message.chat.id, 'В каком банке Вы хотели бы взять ипотеку?', reply_markup=keyboard)
        amount_of_mothers_capital[message.chat.id] = 0
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, ответьте Да или Нет')


@bot.message_handler(func=lambda message: bot_status[message.chat.id] == 'waiting_for_amount_of_mothers_capital')
def get_amount_of_mothers_capital(message):
    if normalize_price(message.text):
        if normalize_price(message.text) != 0:
            amount_of_mothers_capital[message.chat.id] = normalize_price(message.text)
            bot_status[message.chat.id] = 'waiting_for_bank_name'
            bot_status[message.chat.id] = 'waiting_for_bank_name'
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            btn1 = types.KeyboardButton(text=banks[0].upper())
            btn2 = types.KeyboardButton(text=banks[1].upper())
            btn3 = types.KeyboardButton(text=banks[2].upper())
            btn4 = types.KeyboardButton(text=banks[3].upper())
            btn5 = types.KeyboardButton(text=banks[4].upper())
            btn6 = types.KeyboardButton(text=banks[5].upper())
            keyboard.add(btn1, btn2, btn3, btn4, btn5, btn6)
            bot.send_message(message.chat.id, 'В каком банке Вы хотели бы взять ипотеку?', reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, 'Введите корректные данные (например 500 000)')
    else:
        bot.send_message(message.chat.id, 'Введите корректные данные (например 500 000)')


@bot.message_handler(func=lambda message: bot_status[message.chat.id] == 'waiting_for_bank_name')
def get_bank_name(message):
    if message.text.lower() in banks:
        bank_name[message.chat.id] = message.text.lower()
        credit_rate[message.chat.id] = credit_rates[bank_name[message.chat.id]] / 100
        remove_keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'На сколько лет Вы планируете взять кредит?', reply_markup=remove_keyboard)
        bot_status[message.chat.id] = 'waiting_for_credit_duration'
    else:
        bot.send_message(message.chat.id, 'У нас нет информации по данному банку, Для выбора банка Вы можете воспользоваться кнопками ниже')


@bot.message_handler(func=lambda message: bot_status[message.chat.id] == 'waiting_for_credit_duration')
def get_credit_duration(message):
    if message.text.isdigit():
        if int(message.text) != 0:
            credit_duration[message.chat.id] = int(message.text)
            if amount_of_children[message.chat.id] == 0:
                amount_of_subsidy[message.chat.id] = round(0.3 * estimated_area[message.chat.id] * 165312)
            else:
                amount_of_subsidy[message.chat.id] = round(0.35 * estimated_area[message.chat.id] * 165312)
            own_money_for_first_payment[message.chat.id] = round(cost_of_apartment[message.chat.id] * 0.15 - amount_of_mothers_capital[message.chat.id] - amount_of_subsidy[message.chat.id])
            if own_money_for_first_payment[message.chat.id] < 0:
                own_money_for_first_payment[message.chat.id] = 0
            credit_size = cost_of_apartment[message.chat.id] - amount_of_mothers_capital[message.chat.id] - amount_of_subsidy[message.chat.id] - own_money_for_first_payment[message.chat.id]
            month_payment = credit_size * (credit_rate[message.chat.id] / 12 * (1 + credit_rate[message.chat.id] / 12) ** (credit_duration[message.chat.id] * 12)) / ((1 + credit_rate[message.chat.id] / 12) ** (credit_duration[message.chat.id] * 12) - 1)
            bot.send_message(message.chat.id, f'Стоимость квартиры - {format_price(cost_of_apartment[message.chat.id])} руб.\nПервоначальный взнос - {format_price(round(0.15 * cost_of_apartment[message.chat.id]))} руб.\na) За счет маткапитала/господдержки - {format_price(amount_of_mothers_capital[message.chat.id] + amount_of_subsidy[message.chat.id])} руб.\nб) За счет собственных средств - {format_price(own_money_for_first_payment[message.chat.id])} руб.\nСумма кредита - {format_price(credit_size)} руб.\n Ставка - {int(credit_rate[message.chat.id] * 100)} %\nЕжемесячный платеж - {format_price(round(month_payment))} руб.\nОбщая сумма - {format_price(round(month_payment * credit_duration[message.chat.id] * 12))} руб.\nПереплата - {format_price(round(month_payment * credit_duration[message.chat.id] * 12 - credit_size))} руб.')
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton(text='Ипотечный кредит')
            btn2 = types.KeyboardButton(text='Образовательный кредит')
            btn3 = types.KeyboardButton(text='Налоговый вычет')
            keyboard.add(btn1, btn2, btn3)
            bot.send_message(message.chat.id, 'Выберите интересующую Вас тему', parse_mode="Markdown", reply_markup=keyboard)
            bot_status[message.chat.id] = 'waiting_for_theme'
        else:
            bot.send_message(message.chat.id, 'Введите корректные данные (например 20)')
    else:
        bot.send_message(message.chat.id, 'Введите корректные данные (например 20)')



bot.polling()
