import calendar
import datetime
import random
import traceback


import universal
import weatherhandler
import questionhandler


def Question(keywords, question):
    question = question.split(" ")
    points = 0
    for word in keywords:
        for words in question:
            if word == words:
                points += 1
    if points > (len(keywords) * .74) or points > (len(question) * .74):
        return True
    else:
        return False

def QueryQuestion(keywords, requiredKeywords):
    for keys in requiredKeywords:
        if keys in keywords:
            return True
    return False

def pseudorandom(phrases):
    phrase = random.choice(phrases)
    phrase2 = random.choice(phrases)
    phrase3 = random.choice(phrases)
    return [phrase, phrase2, phrase3]

def getDay(num):
    currentdate = datetime.date.today()
    currentdate = calendar.day_name[currentdate.weekday()]
    if currentdate == "Monday":
        if num == 1:
            return "Tuesday"
        elif num == 2:
            return "Wednesday"
        elif num == 3:
            return "Thursday"
        elif num == 4:
            return "Friday"
        elif num == 5:
            return "Saturday"
        elif num == 6:
            return "Sunday"
        elif num == 7:
            return "Next Monday"
    elif currentdate == "Tuesday":
        if num == 7:
            return "Next Tuesday"
        elif num == 1:
            return "Wednesday"
        elif num == 2:
            return "Thursday"
        elif num == 3:
            return "Friday"
        elif num == 4:
            return "Saturday"
        elif num == 5:
            return "Sunday"
        elif num == 6:
            return "Monday"
    elif currentdate == "Wednesday":
        if num == 6:
            return "Tuesday"
        elif num == 7:
            return "Next Wednesday"
        elif num == 1:
            return "Thursday"
        elif num == 2:
            return "Friday"
        elif num == 3:
            return "Saturday"
        elif num == 4:
            return "Sunday"
        elif num == 5:
            return "Monday"
    elif currentdate == "Thursday":
        if num == 5:
            return "Tuesday"
        elif num == 6:
            return "Wednesday"
        elif num == 7:
            return "Next Thursday"
        elif num == 1:
            return "Friday"
        elif num == 2:
            return "Saturday"
        elif num == 3:
            return "Sunday"
        elif num == 4:
            return "Monday"
    elif currentdate == "Friday":
        if num == 4:
            return "Tuesday"
        elif num == 5:
            return "Wednesday"
        elif num == 6:
            return "Thursday"
        elif num == 7:
            return "Next Friday"
        elif num == 1:
            return "Saturday"
        elif num == 2:
            return "Sunday"
        elif num == 3:
            return "Monday"
    elif currentdate == "Saturday":
        if num == 3:
            return "Tuesday"
        elif num == 4:
            return "Wednesday"
        elif num == 5:
            return "Thursday"
        elif num == 6:
            return "Friday"
        elif num == 7:
            return "Next Saturday"
        elif num == 1:
            return "Sunday"
        elif num == 2:
            return "Monday"
    elif currentdate == "Sunday":
        if num == 2:
            return "Tuesday"
        elif num == 3:
            return "Wednesday"
        elif num == 4:
            return "Thursday"
        elif num == 5:
            return "Friday"
        elif num == 6:
            return "Saturday"
        elif num == 7:
            return "Next Sunday"
        elif num == 1:
            return "Monday"

def selectandspeak(phrases):
    phrases = pseudorandom(phrases)
    phrases = pseudorandom(phrases)
    phrase = random.choice(phrases)
    return "      " + phrase

def ProcessQuery(keywords, query):
    print("[PROC] Processing query")
    status = query['process'](keywords)
    if not status:
        return False
    universal.waitingForQuery = False
    universal.currentQueries.remove(universal.currentQueries.index(query))
    print['[SUCC] Processed query']
    return True

def process(keywords, scores=False, originaltext=False, passedValue=False, client=False):
    if scores:
        plantscore = scores[0]
        questionscore = scores[1]
        weatherscore = scores[2]
    else:
        plantscore = questionscore = weatherscore = 0

    if weatherscore > plantscore and weatherscore > questionscore:
        result = weatherhandler.process(keywords, passedValue, client)
        if result:
            return True
        else:
            return False
    elif questionscore > weatherscore and questionscore > plantscore:
        result = questionhandler.process(keywords, originaltext, passedValue, client)
        if result:
            return True
        else:
            return False
    else:
        result = weatherhandler.process(keywords, passedValue, client)
        if not result:
            result = questionhandler.process(keywords, originaltext, passedValue, client)
        if not result:
            print("[ERRO] Failure to find result in processing")
        else:
            return True

