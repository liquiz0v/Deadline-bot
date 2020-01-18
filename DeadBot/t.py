import telebot
import config
from ics import ics
from ics import event
from datetime import datetime


state = 0
_ics = None
event_info = []

bot = telebot.TeleBot('1038237138:AAGUuXh8ku1wVpCoZJFR6_TozbJbSYxUOQc') #deadlinebot HTTP API


markup = telebot.types.ReplyKeyboardMarkup(True)
markup.row('/calendar')

markup_calendar = telebot.types.ReplyKeyboardMarkup(True)
markup_calendar.row('/add_event', '/delete_all_events', '/home')

markup_reset = telebot.types.ReplyKeyboardMarkup(True)
markup_reset.row('/reset')


@bot.message_handler(commands=["start"])
def cmd_start(message):
    # Start point for bot
    bot.send_message(message.chat.id, "What do you want?", reply_markup=markup)

@bot.message_handler(commands=["reset"])
def cmd_reset(message):
    # Go back to first step for create event
    bot.send_message(message.chat.id, "Clear old data. Enter start time:", reply_markup=markup_reset)
    global state
    state = config.CalendarStates.S_START_TIME.value

@bot.message_handler(commands=["home"])
def cmd_home(message):
    # Go to start point
    bot.send_message(message.chat.id, "What do you want?", reply_markup=markup)
    global state
    state = config.CalendarStates.S_START_TIME.value

@bot.message_handler(commands=["add_event"])
def add_new_event(message):
    # Add new event to calendar
    bot.send_message(message.chat.id, "Enter start time:", reply_markup=markup_reset)
    global state
    state = config.CalendarStates.S_START_TIME.value

@bot.message_handler(commands=["delete_all_events"])
def del_all_events(message):
    # Delete all events from calendar
    global _ics
    _ics.delete_all()
    _ics = ics.ICS([])
    bot.send_message(message.chat.id, "All events have been removed")

@bot.message_handler(commands=["calendar"])
def cmd_calendar(message):
    global state
    if state == config.CalendarStates.S_START_TIME.value:
        bot.send_message(message.chat.id, "Waiting for start time")
    elif state == config.CalendarStates.S_DUE_TIME.value:
        bot.send_message(message.chat.id, "Waiting for due time")
    elif state == config.CalendarStates.S_SUMMARY.value:
        bot.send_message(message.chat.id, "Waiting for summary")
    elif state == config.CalendarStates.S_DESCRIPTION.value:
        bot.send_message(message.chat.id, "Waiting for description")
    else:  # Start position for event
        bot.send_message(message.chat.id, "Enter start time:", reply_markup=markup_reset)
        state = config.CalendarStates.S_START_TIME.value
        global _ics
        _ics = ics.ICS([])
        print(_ics)

@bot.message_handler(func=lambda message: state == config.CalendarStates.S_START_TIME.value) 
def event_start_time(message):
    # Se step for new event
    bot.send_message(message.chat.id, "Due time:")
    event_info.append(message.text)
    global state
    state = config.CalendarStates.S_DUE_TIME.value

@bot.message_handler(func=lambda message: state == config.CalendarStates.S_DUE_TIME.value) 
def event_due_time(message):
    # Second step for new event
    bot.send_message(message.chat.id, "Summary:")
    event_info.append(message.text)
    global state
    state = config.CalendarStates.S_SUMMARY.value

@bot.message_handler(func=lambda message: state == config.CalendarStates.S_SUMMARY.value) 
def event_summary(message):
    # Third step for new event
    bot.send_message(message.chat.id, "Description:")
    event_info.append(message.text)
    global state
    state = config.CalendarStates.S_DESCRIPTION.value

@bot.message_handler(func=lambda message: state == config.CalendarStates.S_DESCRIPTION.value) 
def event_description(message):
    # Fourth step for new event
    bot.send_message(message.chat.id, "Done!", reply_markup=markup_calendar)
    event_info.append(message.text)

    global state
    state = config.CalendarStates.S_START_TIME.value

    e = event.Event(event_info[0], event_info[1], event_info[2], event_info[3])
    event_info.clear()
    
    global _ics
    _ics.add(e)
    ics_bytes = _ics.to_bytes()
    
    bot.send_message(message.chat.id, "Bytes: " + ics_bytes)


bot.polling(none_stop=True, interval=0)