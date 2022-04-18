import telebot
from extensions import APIException, Converter
from config import keys, TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start", "help"])
def help(message):
    text = "Чтобы конвертировать евро в другую валюту ИЛИ другую валюту в евро, введите команду боту на русском языке и через пробел:\n\n<количество валюты> \
<имя валюты, из которой переводим>  <имя валюты, в которую переводим>\n\nПример:\n15 доллар евро\n\nЧтобы получить информацию о всех доступных валютах, \
    воспользуйтесь командой /value"
    bot.reply_to(message, text)

@bot.message_handler(commands=["value"])
def value(message):
    text = "Доступные валюты:"
    for i in keys.keys():
        text += '\n' + i
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=["text",])
def convert(message):
    try:
        values = message.text.strip().lower().split(' ')
        converter = Converter()
        answer = converter.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}\nОбратитесь к справке с помощью команды /help')
    except Exception as e:
        bot.reply_to(message, f'Боту не удалось обработать команду\n{e}')
    else:
        bot.send_message(message.chat.id, answer)


bot.polling(non_stop=True)