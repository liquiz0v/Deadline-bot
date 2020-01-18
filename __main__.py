from json import loads
import os
import webbrowser
from json import loads

from trello import TrelloApi

print("\n")


with open(os.path.join(os.getcwd(), "config_.json"), "rb") as f:
    config_ = loads(f.read())

with open(os.path.join(os.getcwd(), "config.json"), "rb") as f:
    config = loads(f.read())

key = config_["trello"]["key"]  # '"093751fd307b96265f8f948a7afb540d"'
secret = config_["trello"]["secret"]
board_id = config_["trello"]["testBoard"]

req_url = config["trello"]["requestURL"]
acc_url = config["trello"]["accessURL"]
auth_url = config["trello"]["authorizeURL"]
my_token = config["trello"]["my_token"]


trello = TrelloApi(key)

# сгенерить ссыль для авторизации
my_url = trello.get_token_url("Deadline Bot", expires="30days", write_access=True)


# открыть ее в браузере
webbrowser.open(url=my_url)

token = input(">>> ")

# токен авторизационный. приложуха попросит пользователя перейти в браузер и вставить оттуда токен в бота

trello.set_token(token)

# создать новую доску и сразу взять инфу о ней
board_id = trello.boards.new(name="New Board")["id"]

board = trello.boards.get(board_id)

# взять такслисты по уже имеющейся борде. пролистать борды нельзя
task_lists = trello.boards.get_list(board_id)

print("choose tasklist")
[print(i["name"]) for i in task_lists]

usinp = input(">>> ")

task_list_id = 0

for i in task_lists:
    if str(i["name"]) == str(usinp):
        task_list_id = i["id"]
        break

task_list = trello.lists.get(task_list_id)


# пройтись по картам и выбрать их
cards = trello.lists.get_card(task_list_id)

print("choose card")
[print(i["name"]) for i in cards]

usinp = input(">>> ")

card_id = 0

for i in tasklists:
    if str(i["name"]) == str(usinp):
        card_id = i["id"]
        break

print(taskList["taskist_id"])
