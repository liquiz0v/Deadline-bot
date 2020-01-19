import telebot
from . import config
from ics import ics
from ics import event
from datetime import datetime


state_calndar = 0
_ics = None
event_info_calendar = []

bot = telebot.TeleBot('1038237138:AAGUuXh8ku1wVpCoZJFR6_TozbJbSYxUOQc') #deadlinebot HTTP API


markup = telebot.types.ReplyKeyboardMarkup(True)
markup.row('/calendar')

markup_calendar = telebot.types.ReplyKeyboardMarkup(True)
markup_calendar.row('/add_event', '/delete_all_events')

markup_reset_calendar = telebot.types.ReplyKeyboardMarkup(True)
markup_reset_calendar.row('/reset_calendar')


@bot.message_handler(commands=["start"])
def cmd_start(message):
    # Start point for bot
    bot.send_message(message.chat.id, "What do you want?", reply_markup=markup)

@bot.message_handler(commands=["reset_calendar"])
def cmd_reset(message):
    # Go back to first step for create event
    bot.send_message(message.chat.id, "Clear old data. Enter start time:", reply_markup=markup_reset_calendar)
    global state_calndar
    state_calndar = config.CalendarStates.S_START_TIME.value

@bot.message_handler(commands=["home"])
def cmd_home(message):
    # Go to start point
    bot.send_message(message.chat.id, "What do you want?", reply_markup=markup)
    global state_calndar
    state_calndar = config.CalendarStates.S_START_TIME.value

@bot.message_handler(commands=["add_event"])
def add_new_event(message):
    # Add new event to calendar
    bot.send_message(message.chat.id, "Enter start time:", reply_markup=markup_reset_calendar)
    global state_calndar
    state_calndar = config.CalendarStates.S_START_TIME.value

@bot.message_handler(commands=["delete_all_events"])
def del_all_events(message):
    # Delete all events from calendar
    global _ics
    _ics.delete_all()
    _ics = ics.ICS([])
    bot.send_message(message.chat.id, "All events have been removed")

@bot.message_handler(commands=["calendar"])
def cmd_calendar(message):
    global state_calndar
    if state_calndar == config.CalendarStates.S_START_TIME.value:
        bot.send_message(message.chat.id, "Waiting for start time")
    elif state_calndar == config.CalendarStates.S_DUE_TIME.value:
        bot.send_message(message.chat.id, "Waiting for due time")
    elif state_calndar == config.CalendarStates.S_SUMMARY.value:
        bot.send_message(message.chat.id, "Waiting for summary")
    elif state_calndar == config.CalendarStates.S_DESCRIPTION.value:
        bot.send_message(message.chat.id, "Waiting for description")
    else:  # Start position for event
        bot.send_message(message.chat.id, "Enter start time:", reply_markup=markup_reset_calendar)
        state_calndar = config.CalendarStates.S_START_TIME.value
        global _ics
        _ics = ics.ICS([])
        print(_ics)

@bot.message_handler(func=lambda message: state_calndar == config.CalendarStates.S_START_TIME.value) 
def event_start_time(message):
    # Se step for new event
    bot.send_message(message.chat.id, "Due time:")
    event_info_calendar.append(message.text)
    global state_calndar
    state_calndar = config.CalendarStates.S_DUE_TIME.value

@bot.message_handler(func=lambda message: state_calndar == config.CalendarStates.S_DUE_TIME.value) 
def event_due_time(message):
    # Second step for new event
    bot.send_message(message.chat.id, "Summary:")
    event_info_calendar.append(message.text)
    global state_calndar
    state_calndar = config.CalendarStates.S_SUMMARY.value

@bot.message_handler(func=lambda message: state_calndar == config.CalendarStates.S_SUMMARY.value) 
def event_summary(message):
    # Third step for new event
    bot.send_message(message.chat.id, "Description:")
    event_info_calendar.append(message.text)
    global state_calndar
    state_calndar = config.CalendarStates.S_DESCRIPTION.value

@bot.message_handler(func=lambda message: state_calndar == config.CalendarStates.S_DESCRIPTION.value) 
def event_description(message):
    # Fourth step for new event
    bot.send_message(message.chat.id, "Done!", reply_markup=markup_calendar)
    event_info_calendar.append(message.text)

    global state_calndar
    state_calndar = config.CalendarStates.S_START_TIME.value

    e = event.Event(event_info_calendar[0], event_info_calendar[1], event_info_calendar[2], event_info_calendar[3])
    event_info_calendar.clear()
    
    global _ics
    _ics.add(e)
    ics_bytes = _ics.to_bytes()
    f = open('file', 'wb')
    f.write(_ics.to_bytes())
    bot.send_message(message.chat.id, "Bytes: " + ics_bytes)


bot.polling(none_stop=True, interval=0)