import telebot
import random
import asyncio
from telebot import types
from telebot.async_telebot import AsyncTeleBot
from importlib.resources import contents
import openpyxl

wb = openpyxl.load_workbook("dataBase.xlsx")
sheet = wb.active

bot = AsyncTeleBot(open("token.txt", "r").readline())
botScore = 0
userScore = 0
pongUrl = 'https://earnest-snickerdoodle-349510.netlify.app'

#обработчик команды для запуска понга
@bot.message_handler(commands=["pong"])
async def sendPongLink(message):
    global pongUrl
    keyboard = types.InlineKeyboardMarkup()
    buttonPlayPong = types.InlineKeyboardButton(text="Play pong", callback_game=True)
    keyboard.add(buttonPlayPong)
    sheet.append([message.from_user.id, message.from_user.username, message.text])
    wb.save('dataBase.xlsx')
    await bot.send_game(message.chat.id, "pong", reply_markup=keyboard)

#обработчик команды для запуска камень ножницы бумага
@bot.message_handler(commands=["rps"])
async def rps(message):
    keyboard = types.InlineKeyboardMarkup()
    buttonRock = types.InlineKeyboardButton(text="Камень", callback_data="rock")
    buttonPaper = types.InlineKeyboardButton(text="Бумага", callback_data="paper")
    buttonScissors = types.InlineKeyboardButton(text="Ножницы", callback_data="scissors")
    keyboard.add(buttonRock)
    keyboard.add(buttonPaper)
    keyboard.add(buttonScissors)
    sheet.append([message.from_user.id, message.from_user.username, message.text])
    wb.save('dataBase.xlsx')
    await bot.reply_to(message, f"Играем до 3-х побед, вы ходите первым.", reply_markup=keyboard)

#обраточик команды help
@bot.message_handler(commands=["help"])
async def help(message):
    sheet.append([message.from_user.id, message.from_user.username, message.text])
    wb.save('dataBase.xlsx')
    await bot.reply_to(message, "/start - Выводит приветственное сообщение\n/help - Выводит данное сообщение\n/rps - Запускает игру камень ножницы бумага\n/pong - запуск классической игры pong")

#обраточик команды start
@bot.message_handler(commands=["start"])
async def send_welcome(message):
    sheet.append([message.from_user.id, message.from_user.username, message.text])
    wb.save('dataBase.xlsx')
    await bot.reply_to(message, "Привет! Я PlayGameBot. Со мной ты можешь играть в разные игры." )

#обработчик нажатия кнопки запуска понга
@bot.callback_query_handler(func=lambda call: call.message.content_type == "game")
async def launch(call):
    global pongUrl
    wb.save('dataBase.xlsx')
    await bot.answer_callback_query(call.id, url=pongUrl)

#обработчик нажатий кнопок с вариантами выбора в игре камень ножницы бумага
@bot.callback_query_handler(func=lambda call: call.message.content_type != "game")
async def rps(call):
    wb.save('dataBase.xlsx')
    global botScore
    global userScore
    keyboard = types.InlineKeyboardMarkup()
    buttonRock = types.InlineKeyboardButton(text="Камень", callback_data="rock")
    buttonPaper = types.InlineKeyboardButton(text="Бумага", callback_data="paper")
    buttonScissors = types.InlineKeyboardButton(text="Ножницы", callback_data="scissors")
    keyboard.add(buttonRock)
    keyboard.add(buttonPaper)
    keyboard.add(buttonScissors)

    if call.message:
            choice_option = ["rock","scissors","paper"]
            choice = random.choice(choice_option)

            if choice == call.data:
                await bot.send_message(call.message.chat.id, "Ничья")
            else:
                if choice == 'rock' :
                    await bot.send_message(call.message.chat.id, "Камень")
                    if  call.data == "scissors":
                        botScore += 1
                    elif  call.data == "paper":
                        userScore += 1
                elif  choice == 'paper':
                    await bot.send_message(call.message.chat.id, "Бумага")
                    if call.data == "rock":
                        botScore += 1
                    elif  call.data == "scissors":
                        userScore += 1
                elif choice == 'scissors':
                    await bot.send_message(call.message.chat.id, "Ножницы")
                    if call.data == "paper":
                        botScore += 1
                    elif  call.data == "rock":
                        userScore += 1
            if botScore == 3 or userScore == 3:
                if botScore == 3:
                    await bot.send_message(call.message.chat.id, f"текущий счёт: {botScore}:{userScore}")
                    await bot.send_message(call.message.chat.id, "Я выйграл")
                    botScore = 0
                    userScore = 0
                else:
                    await bot.send_message(call.message.chat.id, f"текущий счёт: {botScore}:{userScore}")
                    await bot.send_message(call.message.chat.id, "Я проиграл")
                    botScore = 0
                    userScore = 0
            else:
                await bot.send_message(call.message.chat.id, f"текущий счёт {botScore}:{userScore}", reply_markup=keyboard)

asyncio.run(bot.polling(none_stop="True"))

