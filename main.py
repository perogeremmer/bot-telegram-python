from telegram import *
from telegram.ext import * 
from requests import *
import random
from constant import EventState

updater = Updater(token="")
dispatcher = updater.dispatcher

x = 0
y = 0
result = 0

state = ""

allowed_usernames = ['perogeremmer']
data = [1,2,3,4,5,6,7,8,9]

def reset():
    global state, x, y, result
    
    x = 0
    y = 0
    result = 0
    state = ""

def start_command(update: Update, context: CallbackContext):
    buttons = [[KeyboardButton(EventState.QUIZ_MATH.value)]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to Hudya bot!", reply_markup=ReplyKeyboardMarkup(buttons))

def message_handler(update: Update, context: CallbackContext):
    global state, x, y, result
    
    if update.effective_chat.username not in allowed_usernames:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You are not allowed to use this bot")
        return
    
    answer = update.message.text
    if state == EventState.QUIZ_MATH.value:
        answer = int(answer)
        
        if answer == result:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Correct!")
            reset()
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Wrong!")
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"What is the result of {x} + {y}?")
            
        return
    
    if EventState.QUIZ_MATH.value in answer:
        state = EventState.QUIZ_MATH.value
        get_new_question()
        
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"What is the result of {x} + {y}?")
        
        return True
        
def get_new_question():
    global x, y, result
    
    x = random.choice(data)
    y = random.choice(data)
    result = x + y
    
    return True

def query_handler(update: Update, context: CallbackContext):
    query = update.callback_query.data
    update.callback_query.answer()


dispatcher.add_handler(CommandHandler("start", start_command))
dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
dispatcher.add_handler(CallbackQueryHandler(query_handler))

print("The program is running...")
updater.start_polling()