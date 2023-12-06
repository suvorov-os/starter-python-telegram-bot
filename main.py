# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Depends
from telegram import Update, Bot,InlineKeyboardButton, InlineKeyboardMarkup
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
    chat_id = update.message["chat"]["id"]
    text = update.message["text"]
    #usname = update.message.from_user.username
    # print("Received message:", update.message)

    if text == "/start":
        quest_state=STATE_NAME
        #with open('hello.gif', 'rb') as photo:
            #await bot.send_photo(chat_id=chat_id, photo=photo)
        await bot.send_message(chat_id=chat_id, text="2 аттестация. Пересдача.\n Введите фамилию.")
    else:
        quest_state==quest_state+1
        if quest_state==STATE_GROUP:
            student_name=text
            await bot.send_message(chat_id=chat_id, reply_to_message_id=update.message["message_id"], text=student_name)
        else:
            await bot.send_message(chat_id=chat_id, text="Some problem")

    return {"ok": True}
