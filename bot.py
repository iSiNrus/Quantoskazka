
import time
from datetime import datetime

from jira_connector.JiraConnector import JiraConnector
from tamtam.tamtam import TamTam

TOKEN = 'bAxyci_N4kdPqV73tpQY-LFPJgRE11BasMJQOfpeb1s'
BOT_ID = 587004630026

tt = TamTam(TOKEN)
_chatsCount = 0
chats = tt.get_chats_all()

def hello(chat_id):
    tt.send(chat_id, 'Бот Жора снова с вами!. \n'
            'Для работы мне нужна URL вашей Jira \n'
            'Команда "Жора, URL = <адрес>"')
    print('Бот Жора снова с вами!')

def help(chat_id):
    tt.send(chat_id, 'Меня зовут Жора. \n'
            'Попросить меня о действии в Jira можно через обращение "Жора, <что сделать>" \n'
            'Вот что я уже умею: \n'
            'добавь задачу: project_key#summary#user \n'
            'добавь баг: project_key#summary#user \n'
            'удали задачу \n'
            'выведи задачи из project_key \n'
            'выведи проекты \n'
            )

def task_for_bot(chat_id, project, summary, user):
    jc = JiraConnector('https://quanoskazka.atlassian.net/')
    if jc.createTask(project, summary, user):
        tt.send(chat_id, 'Выполняю, сир...')
    else:
        tt.send(chat_id, "Ошибка")

def bag_for_bot(chat_id, project, summary, user):
    jc = JiraConnector('https://quanoskazka.atlassian.net/')
    if jc.createBag(project, summary, user):
        tt.send(chat_id, 'Выполнено, сир...')
    else:
        tt.send(chat_id, 'Ошибочка вышла')

def print_projects(chat_id):
    jc = JiraConnector('https://quanoskazka.atlassian.net/')
    proj = jc.get_projects()
    out = ''
    out = out + 'Проекты:\n'
    for object in proj:
        out = out + object.__str__() + ' - ' + object.__getattr__('name')
    tt.send(chat_id, out)

def delete_task(chat_id):
    tt.send(chat_id, 'Задача удалена... или нет')

def get_tasks_from(chat_id, project):
    jc = JiraConnector('https://quanoskazka.atlassian.net/')
    issues = jc.getIssues(project)
    if issues:
        out = ''
        for object in issues:
            task = jc.get_task(object.__getattr__('key'))
            out = out + object.__str__()+' - '
            out = out + task.fields.summary + '\n'
        tt.send(chat_id, out)
    else:
        tt.send(chat_id, 'Ошибка')

def CheckNewChats():
    all_chats = tt.get_chats_all()
    all_count_chats = len(all_chats)
#    print(all_count_chats)
    if tt._chatsCount != all_count_chats:
        count_new_chats = all_count_chats - tt._chatsCount
        for i in range (count_new_chats):
            hello(all_chats[i]['chat_id'])
            tt._chatsCount+=1

sender = tt.sender
text_msg = tt.text_msg
user_id_msg = tt.user_id_msg
user_name_msg = tt.user_name_msg

def check_us_msg():
    user_name_msg = sender['name']
    user_id_msg = sender['user_id']
    print('"',text_msg,'"', 'Author: ', user_id_msg, ' ', user_name_msg, ' ', datetime.strftime(datetime.now(), "%H:%M  %Y.%m.%d"))

#print(len(tt.get_chats_all()))

while True:
    try:
        CheckNewChats()
        chats_upd = tt.get_chats_all()
        for chat_count in range (len (chats_upd)):
            msgs = tt.get_messages(chats_upd[chat_count]['chat_id'])
            chatID = chats_upd[chat_count]['chat_id']
            print(chatID)

            sender = msgs[0]['sender']
            message = msgs[0]['message']

            text_msg = message['text']

            if sender['user_id'] != BOT_ID and text_msg.lower().find('жора,') != -1:

                if text_msg.lower().find(' добавь задачу:') != -1:
                    ls = text_msg.lower().replace("жора, добавь задачу:", "").split('#')
                    task_for_bot(chatID, project=ls[0].replace(" ", "").upper(), summary=ls[1], user=ls[2])
                    check_us_msg()

                if text_msg.lower().find(' добавь баг:') != -1:
                    ls = text_msg.lower().replace("жора, добавь баг:", "").split('#')
                    bag_for_bot(chatID, project=ls[0].replace(" ", "").upper(), summary=ls[1], user=ls[2])
                    check_us_msg()

                if text_msg.lower().find(' удали задачу') != -1:
                    delete_task(chatID)
                    check_us_msg()

                if text_msg.lower().find(' выведи задачи из') != -1:
                    ls = text_msg.lower().replace("жора, выведи задачи из", "")
                    text_msg = ls.replace(" ", "")
                    get_tasks_from(chatID, text_msg)
                    check_us_msg()

                if text_msg.lower().find('привет') != -1:
                    check_us_msg()
                    tt.send(chats_upd[chat_count]['chat_id'], 'Привет, ' + sender['name'])

                if text_msg.lower().find('help') != -1:
                    check_us_msg()
                    help(chatID)
                if text_msg.lower().find('помощь') != -1:
                    check_us_msg()
                    help(chatID)
                if text_msg.lower().find('выведи проекты') != -1:
                    print_projects(chatID)
                    check_us_msg()

            if sender['user_id'] != BOT_ID:
                if text_msg.lower().find('help') != -1:
                    check_us_msg()
                    help(chatID)
        time.sleep(1)
    except Exception:
        print('Error')
