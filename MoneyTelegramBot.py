#токен бота в файле qwer.py
#классы хранятся в файле extensions.py
#адрес бота  https://t.me/moneyinfo34_bot
import telebot
from config import keys, TOKEN
from extensions import ConvertionException, ValueConvertor

bot = telebot.TeleBot(TOKEN)


# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Введите следующие данные :\n<имя валюты, цену которой он хочет узнать> \
<имя валюты, в которой надо узнать цену первой валюты> \
<количество первой валюты> \nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys(): # каждая новая будет переноситься на новую строку
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Слишком много параметров')

        quote, base, amount = values
        total_base = ValueConvertor.convert(quote, base, amount)

    except ConvertionException as e:\
        bot.reply_to(message, f'Ошибка пользователя\n{e}')

    except Exception as e:\
        bot.reply_to(message, f'Не удалось выполнить команду\n{e}')

    else:
        ds = total_base['result']
        text = f'Цена {amount} {quote} в {base} - {ds}'
        bot.send_message(message.chat.id, text)


bot.polling()