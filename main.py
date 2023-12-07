# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Depends
from telegram import Update, Bot,ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from pydantic import BaseModel
import base64
#import boto3
#dynamodb = boto3.resource('dynamodb')
#db = dynamodb.Table('motionless-clam-giletCyclicDB')

class TelegramUpdate(BaseModel):
    update_id: int
    message: dict

app = FastAPI()

quest_state=-2
quest_answers=["","","","","","","","","","","",""]
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

quest_questions=["1) Листовой узел - \nA) Узел с наименьшим значением.\n\
B) Узел с наибольшим значением.\n\
C) Узел, не имеющий поддеревьев.\n\
D) Узел, имеющий степень 0.\n",
"2) Сколько ячеек памяти соответствующего размера потребуется для записи данного\
двоичного дерева в массив?\n\
A) 9\n\
B) 16\n\
C) 15\n\
D) 8",
"3) Бинарное дерево поиска содержит узел x с ключом k. При добавлении новый узел с\
ключом k-1...\n\
A) будет включён в левое поддерево узла x;\n\
B) будет включён в правое поддерево x;\n\
C) может быть включён как в правое, так и в левое поддерево узла x;\n\
D) не может быть включён в дерево.",
"4) Для дерева из вопроса два последовательность 4,2,8,1,6,3,9,7 соответствует:\n\
A) обходу в ширину;\n\
B) обходу в порядке: вершина, левое поддерево, правое поддерево\n\
C) обходу в порядке: левое поддерево, вершина, правое поддерево\n\
D) ни один вариант не верен",
"5) На рисунке приведено \n\
A) сбалансированное дерево высотой 5\n\
B) несбалансированное дерево высотой 5\n\
C) сбалансированное дерево высотой 4\n\
D) несбалансированное дерево высотой 4",
"6) Для красно-черного дерева из утверждений\n\
- корневой узел дерева черный\n\
- у красного узла «потомки» черные\n\
- всякий путь от корня дерева к произвольному узлу имеет одно и то же количество узлов\n\
- Новый узел окрашивается в красный цвет\n\
A) первое неверно\n\
B) второе неверно\n\
C) третье неверно\n\
D) четвертое неверно",
"7) Из двух приведённых \n\
A) двоичной кучей является только левое дерево\n\
B) двоичной кучей является только правое дерево\n\
C) двоичной кучей являются оба дерева\n\
D) ни одно дерево не является двоичной кучей",
"8) За какое время добавляется элемент в двоичную кучу?\n\
A) O(n)\n\
B) O(log n)\n\
C) O(n log n)\n\
D) O(1)",
"9) За какое время удаляется элемент и двоичной кучи?\n\
A) O(n)\n\
B) O(log n)\n\
C) O(n log n)\n\
D) O(1)",
"10) От чего при заполнении хеш-таблицы не зависит вероятность возникновения коллизии?\n\
A) от хеш-функции\n\
B) от отношения размера таблицы к количеству размещаемых элементов\n\
C) от размера конкретного размещаемого элемента\n\
D) зависит от всех трёх факторов",
"11) Каким будет количество красных узлов в красно-чёрном дереве при добавлении в\n\
приведённое дерево нового элемента «5000»?\n\
A)5\n\
B)4\n\
C)6\n\
D)7",
"12) При использовании хеш-функции, основанной на последовательном применении к\n\
каждому символу входного слова операции исключающего ИЛИ, для хеш-таблицы с 256\n\
адресами каким будет количество коллизий для набора слов: hair, thoughtful, necessary, ritzy,\
aquatic, happen, furniture, chicken, swanky, dare, tacit, risk, cloth, voracious, nifty, rest,\
responsible, goofy, romantic, allow, painful, like, lie, godly?\n\
A) 0\n\
B) 3\n\
C) 5\n\
D) 2",""
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
    print (quest_answers)
    usname = update.message
    print (usname)
    # print("Received message:", update.message)
    group_keyboard = [['ОС-27', 'ОС-28'],['СИ-25', 'СИ-26']]
    group_reply_markup = ReplyKeyboardMarkup(group_keyboard, one_time_keyboard=True,resize_keyboard=True)
    answer_keyboard = [['A', 'B'],['C', 'D']]
    answer_reply_markup = ReplyKeyboardMarkup(answer_keyboard, one_time_keyboard=True,resize_keyboard=True)
    if text == "/start":
        quest_state=STATE_NAME
        #with open('hello.gif', 'rb') as photo:
            #await bot.send_photo(chat_id=chat_id, photo=photo)
        await bot.send_message(chat_id=chat_id, text="2 аттестация. Пересдача.\n Введите фамилию.")
    else:
        if quest_state in (0,3,5,9):
            with open(str(quest_state+2)+'qpic.jpg', 'rb') as photo:
                await bot.send_photo(chat_id=chat_id, photo=photo)
			
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
            #await bot.send_message(chat_id=chat_id, text=quest_answers[quest_state])
            
            await bot.send_message(chat_id=chat_id, text=quest_questions[quest_state], reply_markup=answer_reply_markup)            
            
			
        else:
            
            print ("all_finished")
            print (quest_answers)
            result_string=student_name+","+student_group+","
            for rslt_x in range(12):
                result_string=result_string+quest_answers[rslt_x]+","
            result_string=result_string+usname
            await bot.send_message(chat_id=chat_id, text=base64.b64encode(result_string))

    return {"ok": True}
