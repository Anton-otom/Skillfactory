import telebot

from config import keys, TOKEN
from extensions import APIException, CurrencyConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = "Чтобы начать работу введите комманду боту в следующем формате:\n" \
           "<валюта, которую нужно конвертировать>\n<пробел>\n" \
           "<валюта, в которую нужно конвертировать первую валюту>\n<пробел>\n" \
           "<количество первой валюты>\n\n" \
           "Пример запроса:\nдоллар рубль 100\n\n" \
           "Для вывода списка доступных валют введите команду /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values', ])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text += f'\n{key} - {keys[key]}'
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Неверное количество параметров')

        # quote, base, amount = values
        base, quote, amount = values
        total_base = CurrencyConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя. \n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду\n{e}")
    else:
        text = f'Цена {amount} "{base}" = {total_base:.2f} "{quote}"'
        bot.send_message(message.chat.id, text)


bot.polling()