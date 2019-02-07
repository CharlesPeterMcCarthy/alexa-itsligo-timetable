from botocore.vendored import requests
import json

def Handler(event, context):
    if event["request"]["type"] == "LaunchRequest":
        return get_started()
    elif event["request"]["type"] == "IntentRequest":
        return get_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return end_session()

def get_started():
    return create_response(
        "Ok, what do you want to know?",
        "College Timetable",
        "Ok, what do you want to know?",
        "What information do you want to know about your timetable?",
        False
    )

def get_intent(request, session):
    intent_name = request["intent"]["name"]

    if intent_name == "TodaysTimetableIntent":
        return get_classes_today()
    elif intent_name == "TomorrowTimetableIntent":
        return get_classes_tomorrow()
    elif intent_name == "TodaysClassCountIntent":
        return get_class_count()
    elif intent_name == "TodaysBreaksIntent":
        return get_breaks_today()
    elif intent_name == "DayTimetableIntent":
        return get_day_classes(request['intent']['slots']['day']['value'])
    elif intent_name == "NextClassIntent":
        return get_next_class()
    elif intent_name == "AMAZON.HelpIntent":
        return get_help()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return end_session()
    else:
        return unknown_info()

def get_class_count():
    response = requests.get(create_url("classesCount"))
    obj = response.json()

    return create_response(
        "You have " + str(obj['count']) + " classes today.",
        "Class Count Today",
        "You have " + str(obj['count']) + " classes today.",
        "You have " + str(obj['count']) + " classes today.",
        True
    )

def get_breaks_today():
    response = requests.get(create_url("breaksToday"))
    breaks = response.json()
    speechText = ""
    cardText = ""

    if breaks:
        for br in breaks:
            speechText += "You have a break for " + br['length'] + ", starting at " + br['times']['start'] + " until " + br['times']['end'] + ". "
            cardText += br['length'] + ": " + br['times']['start'] + " - " + br['times']['end'] + ". "
    else:
        speechText = "You have no breaks today."
        cardText = "You have no breaks today."

    return create_response(
        speechText,
        "Your Breaks Today",
        cardText,
        speechText,
        True
    )

def get_classes_today():
    response = requests.get(create_url("todaysClasses"))
    todaysClasses = response.json()
    speechText = ""
    cardText = ""

    if todaysClasses:
        for cl in todaysClasses:
            speechText += "You have " + cl['module']['name'] + " at " + cl['times']['start'] + " until " + cl['times']['end'] + ". "
            cardText += cl['module']['name'] + ": " + cl['times']['start'] + " - " + cl['times']['end'] + ". "
    else:
        speechText = "You have no classes today."
        cardText = "You have no classes today."

    return create_response(
        speechText,
        "Your Classes Today",
        cardText,
        speechText,
        True
    )

def get_classes_tomorrow():
    response = requests.get(create_url("tomorrowClasses"))
    tomorrowClasses = response.json()
    speechText = ""
    cardText = ""

    if tomorrowClasses:
        for cl in tomorrowClasses:
            speechText += "You have " + cl['module']['name'] + " at " + cl['times']['start'] + " until " + cl['times']['end'] + ". "
            cardText += cl['module']['name'] + ": " + cl['times']['start'] + " - " + cl['times']['end'] + ". "
    else:
        speechText = "You have no classes tomorrow."
        cardText = "You have no classes tomorrow."

    return create_response(
        speechText,
        "Your Classes Tomorrow",
        cardText,
        speechText,
        True
    )

def get_day_classes(day):
    response = requests.get("https://5c0mrrrbfd.execute-api.eu-west-1.amazonaws.com/Beta")
    days = response.json()
    dayClasses = days[get_day_number(day)]['classes']
    speechText = ""
    cardText = ""

    if dayClasses:
        for cl in dayClasses:
            speechText += "You have " + cl['module']['name'] + " at " + cl['times']['start'] + " until " + cl['times']['end'] + ". "
            cardText += cl['module']['name'] + ": " + cl['times']['start'] + " - " + cl['times']['end'] + ". "
    else:
        speechText = "You have no classes on " + day + "."
        cardText = "You have no classes on " + day + "."

    return create_response(
        speechText,
        "Your Classes on " + day,
        cardText,
        speechText,
        True
    )

def get_next_class():
    response = requests.get(create_url("nextClass"))
    nextClass = response.json()
    cl = nextClass['class']
    speechText = "Your next class is " + cl['module']['name'] + (" on " + nextClass['day'] if not nextClass['isToday'] else " today") + " at " + cl['times']['start'] + " until " + cl['times']['end']
    cardText = (nextClass['day'] if not nextClass['isToday'] else "Today") + "- " + cl['module']['name'] + ": " + cl['times']['start'] + " - " + cl['times']['end']

    if nextClass['isToday'] and nextClass['startsIn']:
        speechText += ". This class starts in " + (str(nextClass['startsIn']['hours']) + " hours " if nextClass['startsIn']['hours'] > 0 else "") + str(nextClass['startsIn']['minutes']) + " minutes."

    return create_response(
        speechText,
        "Your Next Class",
        cardText,
        speechText,
        True
    )

def get_help():
    return create_response(
        "Try asking for todays timetable or how many classes you have today.",
        "Help",
        "Try asking for 'todays timetable' or 'how many classes do I have today'",
        "What information do you want to know about your timetable?",
        False
    )

def unknown_info():
    return create_response(
        "Sorry, I don't know what you are looking for. Ask for help if needed.",
        "Invalid Response",
        "Sorry, I don't know what you are looking for. Ask for help if needed.",
        "Ask for help if needed.",
        False
    )

def end_session():
    return create_response("Ok. Goodbye.", "Goodbye", "Ok. Goodbye.", "Goodbye.", True)

def create_response(speech, cardTitle, cardText, reprompt, endSession):
    return {
        "version": "1.0",
        "sessionAttributes": {},
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": speech
            },
            "card": {
                "type": "Simple",
                "title": cardTitle,
                "content": cardText
            },
            "reprompt": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": reprompt
                }
            },
            "shouldEndSession": endSession
        }
    }

def create_url(info):
    return "https://5c0mrrrbfd.execute-api.eu-west-1.amazonaws.com/Beta/-info-?info=" + info

def get_day_number(day):
    day = day.lower()
    return {
        'monday' : 0,
        'tuesday' : 1,
        'wednesday' : 2,
        'thursday' : 3,
        'friday' : 4,
        'saturday' : 5,
        'sunday' : 6
    }.get(day, -1)
