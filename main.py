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

quest_questions=["1) Листовой узел - \nа) Узел с наименьшим значением.\n\
б) Узел с наибольшим значением.\n\
в) Узел, не имеющий поддеревьев.\n\
г) Узел, имеющий степень 0.\n",
"2) Сколько ячеек памяти соответствующего размера потребуется для записи данного\
двоичного дерева в массив?\n\
а) 9\n\
б) 16\n\
в) 15\n\
г) 8",
"3) Бинарное дерево поиска содержит узел x с ключом k. При добавлении новый узел с\
ключом k-1...\n\
а) будет включён в левое поддерево узла x;\n\
б) будет включён в правое поддерево x;\n\
в) может быть включён как в правое, так и в левое поддерево узла x;\n\
г) не может быть включён в дерево.",
"4) Для дерева из вопроса два последовательность 4,2,8,1,6,3,9,7 соответствует:\n\
а) обходу в ширину;\n\
б) обходу в порядке: вершина, левое поддерево, правое поддерево\n\
в) обходу в порядке: левое поддерево, вершина, правое поддерево\n\
г) ни один вариант не верен",
"5) На рисунке приведено \n\
а) сбалансированное дерево высотой 5\n\
б) несбалансированное дерево высотой 5\n\
в) сбалансированное дерево высотой 4\n\
г) несбалансированное дерево высотой 4",
"6) Для красно-черного дерева из утверждений\n\
- корневой узел дерева черный\n\
- у красного узла «потомки» черные\n\
- всякий путь от корня дерева к произвольному узлу имеет одно и то же количество узлов\n\
- Новый узел окрашивается в красный цвет\n\
а) первое неверно\n\
б) второе неверно\n\
в) третье неверно\n\
г) четвертое неверно",
"7) Из двух приведённых \n\
а) двоичной кучей является только левое дерево\n\
б) двоичной кучей является только правое дерево\n\
в) двоичной кучей являются оба дерева\n\
г) ни одно дерево не является двоичной кучей",
"8) За какое время добавляется элемент в двоичную кучу?\n\
а) O(n)\n\
б) O(log n)\n\
в) O(n log n)\n\
г) O(1)",
"9) За какое время удаляется элемент и двоичной кучи?\n\
а) O(n)\n\
б) O(log n)\n\
в) O(n log n)\n\
г) O(1)",
"10) От чего при заполнении хеш-таблицы не зависит вероятность возникновения коллизии?\n\
а) от хеш-функции\n\
б) от отношения размера таблицы к количеству размещаемых элементов\n\
в) от размера конкретного размещаемого элемента\n\
г) зависит от всех трёх факторов",
"11) Каким будет количество красных узлов в красно-чёрном дереве при добавлении в\n\
приведённое дерево нового элемента «5000»?\n\
а)5\n\
б)4\n\
в)6\n\
г)7",
"12) При использовании хеш-функции, основанной на последовательном применении к\n\
каждому символу входного слова операции исключающего ИЛИ, для хеш-таблицы с 256\n\
адресами каким будет количество коллизий для набора слов: hair, thoughtful, necessary, ritzy,\
aquatic, happen, furniture, chicken, swanky, dare, tacit, risk, cloth, voracious, nifty, rest,\
responsible, goofy, romantic, allow, painful, like, lie, godly?\n\
а) 0\n\
б) 3\n\
в) 5\n\
г) 2",""
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
    #usname = update.message.from_user.username
    # print("Received message:", update.message)
    group_keyboard = [['ОС-27', 'ОС-28'],['СИ-25', 'СИ-26']]
    group_reply_markup = ReplyKeyboardMarkup(group_keyboard, one_time_keyboard=True,resize_keyboard=True)
    answer_keyboard = [['А', 'Б'],['В', 'Г']]
    answer_reply_markup = ReplyKeyboardMarkup(answer_keyboard, one_time_keyboard=True,resize_keyboard=True)
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
