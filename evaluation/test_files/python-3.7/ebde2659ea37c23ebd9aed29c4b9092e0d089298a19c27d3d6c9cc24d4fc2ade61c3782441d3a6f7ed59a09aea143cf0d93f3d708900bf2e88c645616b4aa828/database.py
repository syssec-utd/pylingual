from tinydb import TinyDB, Query
import time
import os
home_dir = os.path.expanduser('~')
chat_history_path = os.path.join(home_dir, '.gpt_chatbot_chat_history.json')
if not os.path.exists(chat_history_path):
    with open(chat_history_path, 'x') as f:
        f.write('')
db = TinyDB(chat_history_path)

def init_chat_history(message, preset, model):
    _id = str(time.time()).replace('.', '')
    db.insert({'_id': _id, 'preset': preset, 'title': 'Untitled' + '_' + _id, 'model': model, 'messages': message})
    return _id

def update_chat_history(id, message):
    db.update({'messages': message}, Query()._id == id)
    return True

def get_all_chat_history():
    return db.all()

def defind_chat_title(id, title):
    db.update({'title': title}, Query()._id == id)