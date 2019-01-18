from botocore.vendored import requests
import json
import datetime

def lambda_handler(event, context):
    if event["request"]["type"] == "LaunchRequest":
        return get_started()
    elif event["request"]["type"] == "IntentRequest":
        return get_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return end_session()

def get_started():
    return {
        "version": "1.0",
        "sessionAttributes": {},
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "Ok, what do you want to know?"
            },
            "card": {
                "type": "Simple",
                "title": "College Timetable",
                "content": "Ok, what do you want to know?"
            },
            "reprompt": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "What information do you want to know about your timetable?"
                }
            },
            "shouldEndSession": False
        }
    }

def get_intent(request, session):
    intent_name = request["intent"]["name"]

    if intent_name == "TodaysTimetableIntent":
        return get_classes_today()
    elif intent_name == "TodaysClassCount":
        return get_class_count()
    elif intent_name == "AMAZON.HelpIntent":
        return get_help()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return end_session()
    else:
        return unknown_info()

def get_class_count():
    response = requests.get("{{URL_CLASS_COUNT}}")
    obj = response.json()

    return {
        "version": "1.0",
        "sessionAttributes": {},
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "You have " + str(obj['count']) + " classes today."
            },
            "card": {
                "type": "Simple",
                "title": "Class Count Today",
                "content": "You have " + str(obj['count']) + " classes today."
            },
            "reprompt": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "You have " + str(obj['count']) + " classes today."
                }
            },
            "shouldEndSession": True
        }
    }

def get_classes_today():
    response = requests.get("{{URL_CLASSES_TODAY}}")
    obj = response.json()

    todaysClass = obj[0]
    return {
        "version": "1.0",
        "sessionAttributes": {},
        "response": {
            "outputSpeech": {
                "type": "PlainText",    # Just test data - To be updated
                "text": "On " + todaysClass['day'] + " - You have " + todaysClass['classes'][0]['module']['name'] + " at " + todaysClass['classes'][0]['times']['start'] + " until " + todaysClass['classes'][0]['times']['end'] + " with " + todaysClass['classes'][0]['lecturers'][0]
            },
            "card": {
                "type": "Simple",
                "title": "Your Classes Today",
                "content": "On " + todaysClass['day'] + " - You have " + todaysClass['classes'][0]['module']['name'] + " at " + todaysClass['classes'][0]['times']['start'] + " until " + todaysClass['classes'][0]['times']['end'] + " with " + todaysClass['classes'][0]['lecturers'][0]
            },
            "reprompt": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "On " + todaysClass['day'] + " - You have " + todaysClass['classes'][0]['module']['name'] + " at " + todaysClass['classes'][0]['times']['start'] + " until " + todaysClass['classes'][0]['times']['end'] + " with " + todaysClass['classes'][0]['lecturers'][0]
                }
            },
            "shouldEndSession": True
        }
    }

def get_help():
    return {
        "version": "1.0",
        "sessionAttributes": {},
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "At the moment you can only choose to hear your classes for today. Try asking for todays timetable."
            },
            "card": {
                "type": "Simple",
                "title": "Help",
                "content": "At the moment you can only choose to hear your classes for today. Try asking for 'todays timetable'."
            },
            "reprompt": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "What information do you want to know about your timetable?"
                }
            },
            "shouldEndSession": False
        }
    }

def unknown_info():
    return {
        "version": "1.0",
        "sessionAttributes": {},
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "Sorry, I don't know what you are looking for. Ask for help if needed."
            },
            "card": {
                "type": "Simple",
                "title": "Invalid Response",
                "content": "Sorry, I don't know what you are looking for. Ask for help if needed."
            },
            "reprompt": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "Ask for help if needed."
                }
            },
            "shouldEndSession": False
        }
    }

def end_session():
    return {
        "version": "1.0",
        "sessionAttributes": {},
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "Ok. Goodbye."
            },
            "card": {
                "type": "Simple",
                "title": "Goodbye",
                "content": "Ok, Goodbye."
            },
            "reprompt": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "Goodbye."
                }
            },
            "shouldEndSession": True
        }
    }
