import json

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
    elif intent_name == "AMAZON.HelpIntent":
        return get_help()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return end_session()
    else:
        return unknown_info()

def get_classes_today():
    # TODO: Timetable API call
    return {
        "version": "1.0",
        "sessionAttributes": {},
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "Class Info" # Filler text
            },
            "card": {
                "type": "Simple",
                "title": "Classes Today",
                "content": "Class Info" # Filler text
            },
            "reprompt": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "Class Info" # Filler text
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
