# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Depends
from telegram import Update, Bot,ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from pydantic import BaseModel

class TelegramUpdate(BaseModel):
    update_id: int
    message: dict

app = FastAPI()

quest_state=-2
quest_answers=[5,5,5,5,5,5,5,5,5,5,5,5]
STATE_NAME=-2
STATE_GROUP=-1
STATE_Q1=0
STATE_Q2=1
STATE_Q3=2
STATE_Q4=3
STATE_Q5=4
STATE_Q6=5
STATE_Q7=6
STATE_Q8=7
STATE_Q9=8
STATE_Q10=9
STATE_Q11=10
STATE_Q12=11
student_name=""
student_group=""

quest_questions=["Листовой узел - а) Узел с наименьшим значением.\n\
б) Узел с наибольшим значением.\n\
в) Узел, не имеющий поддеревьев.\n\
г) Узел, имеющий степень 0.\n",
"Сколько ячеек памяти соответствующего размера потребуется для записи данного\
двоичного дерева в массив?\n\
а) 9\n\
б) 16\n\
в) 15\n\
г) 8",
"",
"",
"","","","","","","","","","","","","","","","",""
]


# Load variables from .env file if present
load_dotenv()

# Read the variable from the environment (or .env file)
bot_token = os.getenv('BOT_TOKEN')
secret_token = os.getenv("SECRET_TOKEN")
# webhook_url = os.getenv('CYCLIC_URL', 'http://localhost:8181') + "/webhook/"

bot = Bot(token=bot_token)
# bot.set_webhook(url=webhook_url)
# webhook_info = bot.get_webhook_info()
# print(webhook_info)

def auth_telegram_token(x_telegram_bot_api_secret_token: str = Header(None)) -> str:
    # return true # uncomment to disable authentication
    if x_telegram_bot_api_secret_token != secret_token:
        raise HTTPException(status_code=403, detail="Not authenticated")
    return x_telegram_bot_api_secret_token

@app.post("/webhook/")
async def handle_webhook(update: TelegramUpdate, token: str = Depends(auth_telegram_token)):
    global quest_state
    global student_name
    global student_group
    global quest_answers
    chat_id = update.message["chat"]["id"]
    text = update.message["text"]
    #usname = update.message.from_user.username
    # print("Received message:", update.message)
    group_keyboard = [['ОС-27', 'ОС-28'],['СИ-25', 'СИ-26']]
    group_reply_markup = ReplyKeyboardMarkup(group_keyboard, one_time_keyboard=True,resize_keyboard=True)
    answer_keyboard = [['А', 'Б'],['В', 'Г']]
    if text == "/start":
        quest_state=STATE_NAME
        #with open('hello.gif', 'rb') as photo:
            #await bot.send_photo(chat_id=chat_id, photo=photo)
        await bot.send_message(chat_id=chat_id, text="2 аттестация. Пересдача.\n Введите фамилию.")
    else:
        print ("state "+ str(quest_state))
        if quest_state>-1:
            print (quest_questions[quest_state])
        if quest_state==STATE_NAME:
            student_name=text
            quest_state=quest_state+1
            await bot.send_message(chat_id=chat_id, text=student_name+", введите группу", reply_markup=group_reply_markup)
        elif quest_state==STATE_GROUP:
            student_group=text            
            quest_state=quest_state+1
           
            await bot.send_message(chat_id=chat_id, text=quest_questions[quest_state], reply_markup=answer_reply_markup)            
        elif quest_state<12:
            quest_answers[quest_state]=text
            quest_state=quest_state+1
            await bot.send_message(chat_id=chat_id, text=quest_answers[quest_state])
            
            await bot.send_message(chat_id=chat_id, text=quest_questions[quest_state], reply_markup=answer_reply_markup)            
            
			
        else:
            await bot.send_message(chat_id=chat_id, text="Some problem"+str(quest_state))

    return {"ok": True}
