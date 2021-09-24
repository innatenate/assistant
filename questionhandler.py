import datetime
from randfacts import get_fact
from newsapi import NewsApiClient
import traceback

import universal
import commandprocessor
import searchparser

api = NewsApiClient(api_key="efe6facd2ffc41d7b4744391e34ff068")
qb = {}

### Weather: Questionbank
###     'temp' :  Question
###             'keys'  :   ['what is the current temperature', 'what does it feel like outside', 'what is the temperature outside']
###             'function' : def func()
###             'require' : optional, require keys


qb['timecheck'] = {}
qb['timecheck']['keys'] = ["what is the time", "what is the current time", "what time is it"]
qb['timecheck']['require'] = ["time"]
def timeCheck(keywords, data=False, passedValue=False):
    now = datetime.datetime.now()
    phrase = commandprocessor.selectandspeak([f"The current time is {now.strftime('%I:%M %p')}.",
                             f"It's currently {now.strftime('%I:%M %p')}.",
                             f"The time now is {now.strftime('%I:%M %p')}",
                             now.strftime('%I:%M %p'),
                             f"It is currently {now.strftime('%I:%M %p')}"])
    universal.speak(phrase)
    return True
qb['timecheck']['function'] = timeCheck


qb['repeat'] = {}
qb['repeat']['keys'] = ['repeat', 'say again', 'repeat that', 'say that again']
def repeat(keywords, data=False, passedValue=False):
    phrase = commandprocessor.selectandspeak(["I said, ", "No problem, I said", "Alright, "])
    phrase += "             " + universal.lastPhrase

    universal.speak(phrase)
    return True
qb['repeat']['function'] = repeat


qb['wellnesscheck'] = {}
qb['wellnesscheck']['keys'] = ["how are you"]
def wellnessCheck(keywords, data=False, passedValue=False):
    reply = commandprocessor.selectandspeak(["Not too bad for a programmable voice assistant. How about you?",
                            "I'm programmed to have a good day today, how about you?",
                            "I'm having a great day, thank you for asking. How about you?"])
    universal.speak(reply)
    queue = {
        'type': 'specific',
        'keywords': ["good thanks for asking", "great thank you", "doing good thank you", "thank you",
                     "bad", "horrible", "not good", "bad day", "sad today", "doing okay today", "doing ok today",
                     "doing alright",
                     "feeling okay", "feeling good", 'feeling nauseous', "feeling sick"]}

    def queryProcess(keywords):
        if ("good" in keywords or "great" in keywords) and (
                "not" not in keywords and ("good" not in keywords or "great" not in keywords)):
            reply = commandprocessor.selectandspeak(
                ["Glad to hear it.", "Good to hear. If you'd like I could tell you a fun fact. Just ask."])
            universal.speak(reply)
        elif "bad" in keywords or (
                "not" in keywords and ("good" in keywords or "good" in keywords)) or "terrible" in keywords or \
                "horrible" in keywords or "nauseous" in keywords or "sick" in keywords:
            reply = commandprocessor.selectandspeak(["Sorry to hear that. Would you like to hear a fun fact to cheer you up?",
                                    "I bet a fun fact will cheer you up. Would you like to hear one?",
                                    "Fun facts always put me in a better mood. Would you like to hear one?"])
            universal.speak(reply)
            queue2 = {
                'type': 'yesno',
                'keywords': ['sure', 'yes', 'good', 'great', 'no', 'bad', 'stop', 'quit',
                             'thanks', 'please']
            }

            def otherProcess(result):
                if result:
                    universal.speak(get_fact())
                else:
                    universal.speak("Alright then. If you need anything let me know.")

            queue2['process'] = otherProcess
            universal.query(queue2)
        return True

    queue['process'] = queryProcess
    print(queue)
    universal.query(queue)
    print("removing original query")
    if queue in universal.currentQueries:
        universal.currentQueries.remove(queue)
    else:
        print(f"didn't find it in the queries. but i did find {universal.currentQueries}")
    return True
qb['wellnesscheck']['function'] = wellnessCheck


qb['newscheck'] = {}
qb['newscheck']['keys'] = ["what is today's news", "what is the news for today", "what is happening",
                           "what is the daily news", "what's the news"]
def newsCheck(keywords, data=False, passedValue=False):
    results = api.get_top_headlines(country="us", page_size=5)
    results = [
        {
            'author': results['articles'][0]['author'],
            'desc': results['articles'][0]['description']
        },
        {
            'author': results['articles'][1]['author'],
            'desc': results['articles'][1]['description']
        },
        {
            'author': results['articles'][2]['author'],
            'desc': results['articles'][2]['description']
        },
        {
            'author': results['articles'][3]['author'],
            'desc': results['articles'][3]['description']
        },
        {
            'author': results['articles'][4]['author'],
            'desc': results['articles'][4]['description']
        },
    ]
    universal.speak("Today's top news. \n" +
                    f"{results[0]['author']} reports {results[0]['desc']} \n \n" +
                    f"I also found {results[1]['author']} reporting on {results[1]['desc']} \n" +
                    f"On {results[2]['author']} I found an article on {results[2]['desc']} \n \n \n" +
                    f"{results[3]['author']} reports {results[3]['desc']} \n \n" +
                    f"And lastly, {results[4]['author']} wrote an article recently on {results[4]['desc']}")
    return True
qb['newscheck']['function'] = newsCheck

qb['datecheck'] = {}
qb['datecheck']['keys'] = ["what is today numerical", "what is today's date", "what is the date today"]
def dateCheck(keywords, data=False, passedValue=False):
    now = datetime.datetime.now()
    universal.speak(f"Today is {now.strftime('%A    , %B %d     %Y')}")

    return True
qb['datecheck']['function'] = dateCheck


def mathCheck(keywords):
    for word in keywords:
        if len(word) == 1:
            return True
    return False


def calculate(keywords):
    for word in keywords:
        if len(word) > 1:
            keywords.remove(word)

    try:
        keywords = ''.join(keywords)
        answer = eval(keywords)
        return answer, keywords
    except Exception as e:
        print(repr(e))
        traceback.print_tb(e.__traceback__)
        return False, False


def process(keywords, info, passedValue=False):
    """Process question commands, needs keywords(list) and can take a passedValue(any)"""

    questionChoices = []

    for question in qb:
        phrases = qb[question]['keys']
        for phrase in phrases:
            points = 0
            truePass = False
            phrase = phrase.split(" ")
            for pword in phrase:
                if pword in keywords:
                    if 'require' in qb[question]:
                        for word in keywords:
                            if word in qb[question]['require']:
                                truePass = True
                        if truePass:
                            points += 1
                            if points > (len(keywords) * .74) or points > (len(phrase) * .74):
                                questionChoices.insert(0, [question, points])
                    else:
                        points += 1
                        if points > (len(keywords) * .74) or points > (len(phrase) * .74):
                            questionChoices.insert(0, [question, points])

    if len(questionChoices) > 0:
        largestNumber = 0
        for choice in questionChoices:
            if largestNumber < choice[1]:
                largestNumber = choice[1]
        debounce = False
        for choice in questionChoices:
            if choice[1] == largestNumber and not debounce:
                success = qb[choice[0]]['function'](keywords, info, passedValue)
                debounce = True

        if success:
            return True
        else:
            return False
    else:
        if ("what" in keywords or "what's" in keywords) and mathCheck(keywords):
            answer, problem = calculate(keywords)
            if not answer:
                phrase = commandprocessor.selectandspeak(["I couldn't seem to find an answer to that math problem.",
                                         "I couldn't calculate the correct answer.",
                                         "Something didn't process correctly with that equation."])
            else:
                phrase = commandprocessor.selectandspeak([f"The answer to {problem} is {answer}.",
                                         f"When I processed {problem}, I concluded {answer}.",
                                         f"I calculated {problem} with the end result of {answer}."])

            universal.speak(phrase)
            return True
        else:
            return Exception("No result")
            # answer = searchparser.search(originaltext)
            # if answer:
            # if 'snippet' in answer:
            # universal.speak(f"I searched that for you. {answer['answer']}. I also have more information, "
            # f"{answer['snippet']}")
            # elif 'answer' in answer:
            # universal.speak(f"I searched that for you.  {answer['answer']}.")
            # elif 'error' in answer:
            # universal.speak(answer['error'])
            # return True
