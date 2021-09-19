import calendar
import datetime
import random
import time
import traceback

import requests
from newsapi import NewsApiClient
from randfacts import get_fact

import keywordprocessor
import searchparser
import universal
import weathertrendprocessor

weatherApi1 = "https://api.openweathermap.org/data/2.5/onecall?lat=36.052448&lon=-95.790810&exclude=hourly,daily&appid=8f2118090e07640ec49e91a59dedfadd"  # Used for the weather
weatherApi2 = "https://api.openweathermap.org/data/2.5/weather?zip=74012,us&appid=8f2118090e07640ec49e91a59dedfadd"
weatherApi3 = "https://api.openweathermap.org/data/2.5/onecall?lat=36.052448&lon=-95.790810&units=imperial&exclude=hourly,current,minutely&appid=8f2118090e07640ec49e91a59dedfadd"
api = NewsApiClient(api_key="efe6facd2ffc41d7b4744391e34ff068")


def Question(keywords, question):
    question = question.split(" ")
    points = 0
    for word in keywords:
        for words in question:
            if word == words:
                points += 1
    if points > (len(keywords) * .74) or points > (len(question) * .74):
        print("passed with: " + str((len(keywords) * .74)) + " " + (str(len(question) * .74)) + " " + (str(points)))
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


def checkAverages(data, data2):
    print("Checking averages")
    fl = data['main']['feels_like']  # gets the feels like temp
    tempmin = data['main']['temp_min']
    tempmax = data['main']['temp_max']

    fl = round(9 / 5 * (fl - 273) + 32)  # converts the temp (kelvin) into fahrenheit
    tempmin = round(9 / 5 * (tempmin - 273) + 32)  # converts the temp (kelvin) into fahrenheit
    tempmax = round(9 / 5 * (tempmax - 273) + 32)  # converts the temp (kelvin) into fahrenheit

    if fl > 90 or tempmax > 90:
        reply = selectandspeak(
            [f"It looks like it's going to be a hot day today. The high is {str(tempmax)}° fahrenheit.",
             f"It's pretty hot outside. The high is {str(tempmax)}° fahrenheit.",
             f"Prepare yourself for a hot day. The high is {str(tempmax)}° fahrenheit."])

        if round(int(data2['current']['uvi'])) >= 8:
            reply += (selectandspeak(["UV rays are fairly potent. Make sure to wear sunscreen today.",
                                      "The Sun is beaming bright. Make sure you stay protected.",
                                      f"I am forecasting UV rays reaching {round(int(data2['current']['uvi']))} today."]))
        else:
            reply += (
                selectandspeak(["In South Carolina, they would describe today as being hot enough to scald a lizard.",
                                "Make sure you stay hydrated.",
                                "In Wisconsin, Pennsylvania, and New York, it is common for some people to say"
                                "today is hotter than dutch love. Not in reference to the netherlands."]))
    elif fl < 30 or tempmin < 30:
        reply = selectandspeak(
            [f"    It looks like it's going to be fairly cold. The low is {str(tempmin)}° fahrenheit.",
             f"    It's pretty cold outside. The low is {str(tempmin)}° fahrenheit.",
             f"    Get ready for a chilly day. The low  is {str(tempmin)}° fahrenheit."])
        reply += (selectandspeak(["While forecasting this, I discovered a new phrase. It's cold as balls.",
                                  "Now would be an optimal time for chicken noodle soup and hot chocolate.",
                                  "There is always a chance it could randomly snow. Rely on that."]))

    else:
        reply = selectandspeak(["Seems like an average day. Nothing to note.",
                                "I am not forecasting anything other than normal conditions.",
                                "Today's forecast seems mild. Remember to enjoy the nice weather."])

    if int(data["wind"]["speed"]) >= 10:
        reply += selectandspeak(["It looks like it's going to be a windy day today.",
                                 "I am noticing an increase in wind gusts and wind speed.",
                                 "It's fairly windy today. Check the forecast or ask me for more details."])

    if (int(data['main']['pressure']) <= 1015 or int(data['main']['humidity']) > 70) and int(
            data['main']['humidity']) != 100:
        reply += selectandspeak(
            ["It looks like it may rain soon based on the humidity and pressure in the atmosphere.",
             "I am forecasting a chance of rain based on the atmosphere changes.",
             f"I also noticed that the local barometric pressure is at {data['main']['pressure']} hectopascals,"
             " meaning expect unsettled weather.", "I noticed that local atmospheric pressure is low,"
                                                   f" with an average of {data['main']['pressure']} hectopascals.",
             "I am reading a local barometric pressure"
             f" is at {data['main']['pressure']} hectopascals, which is low from the average of 1025 hectopascals."])

    if "alerts" in data2:
        alert = data2['alerts']
        if not alert in universal.alertBank:
            universal.alertBank.insert(0, alert)
        else:
            return reply
        description = str(alert[0]['description'])
        description = description.split("*")
        phrase = selectandspeak([
            f"There is currently a {alert[0]['event']} in your area issued by {alert[0]['sender_name']} It reads as {description[0]} ... and continues with {description[1]}.",
            f"{alert[0]['sender_name']} has issued a {alert[0]['event']} for this area. The description reads {description[0]} .... {description[1]}."])
        reply += phrase

        rando = random.choice([True, False, False])
        if rando:
            reply += selectandspeak([f"I have a fun fact for you. {get_fact()}",
                                     f"And to finish your weather report, I have a fun fact {get_fact()}",
                                     f"Also, I found a fun fact for you. {get_fact()}"])
            print(reply)
    return reply


def Weather(keywords, passedValue=False):
    json_data1 = requests.get(weatherApi1).json()  # connects to the url
    json_data2 = requests.get(weatherApi2).json()
    json_data3 = requests.get(weatherApi3).json()
    formatted_data = json_data2['weather'][0]['description']  # gets the basic data
    temp = json_data2['main']['feels_like']  # gets the feels like temp

    def convert(value):
        return round(9 / 5 * ((int(value)) - 273) + 32)

    tempmin = convert(json_data2['main']['temp_min'])
    tempmax = convert(json_data2['main']['temp_max'])
    feellike = convert(json_data2['main']['feels_like'])

    if Question(keywords, "what weather today") or \
            Question(keywords, "what weather outside"):
        if "rain" in keywords:
            if (int(json_data2['main']['pressure']) > 1015 or int(json_data2['main']['humidity']) > 70) and int(
                    json_data2['main']['humidity']) != 100:
                universal.speak(
                    f"There is a chance it may rain based on the pressure and humidity changes in the atmosphere." +
                    ' Would you like to hear the seven day forecast I have made?')
                queue = {
                    'type': 'yesno',
                    'keywords': ['sure', 'yes', 'good', 'great', 'no', 'bad', 'stop', 'quit',
                                 'thanks', 'please']
                }

                def otherProcess(result):
                    if result:
                        keywordprocessor.Process("what is the 7-day forecast")
                    else:
                        universal.speak("Alright then. If you need anything let me know.")

                queue['process'] = otherProcess
                universal.query(queue)
            return True
        else:

            status = checkAverages(json_data2, json_data1)
            phrase = selectandspeak(
                [f"Today's weather is {str(formatted_data)} and it currently feels like {str(feellike)}° fahrenheit.",
                 f"For today I am forecasting with {str(formatted_data)} and a feels like temperature of {str(feellike)}° fahrenheit.",
                 f"It currently feels like {str(feellike)}° fahrenheit outside and you should expect {str(formatted_data)}."])
            if type(status) == bool:
                universal.speak(phrase)
                return True
            else:
                universal.speak(phrase + status)
        return True

    elif Question(keywords, "what is the high today") or \
            Question(keywords, "what is the low today") or \
            Question(keywords, "is it going to be hot today") or \
            Question(keywords, "is it hot outside today") or \
            Question(keywords, "is it cold outside today") or \
            Question(keywords, "should i wear a jacket today") or \
            Question(keywords, "is it going to be hot today") or \
            Question(keywords, "is it going to be cold today"):

        phrase = f"It currently feels like {feellike}° fahrenheit. Today's high is {tempmax}° with a low of {tempmin}°."
        if ("jacket" in keywords or "cold" in keywords) and tempmin <= 32:
            phrase += "       You should wear a jacket today. It's going to be fairly cold outside."
        elif ("high" in keywords or "hot" in keywords) and tempmax > 90:
            phrase += "       It's going to be a pretty hot day today. It's hot enough to scald a lizard"
        elif ("high" in keywords or "cold" in keywords) and (tempmin > 60 and tempmax < 90):
            phrase += "   It seems like it's fairly mild today. I wouldn't worry about the temperature."

        universal.speak(phrase)

        return True

    elif Question(keywords, "do you think it will rain soon") or \
            Question(keywords, "will it rain today") or \
            Question(keywords, "is there a chance of rain today") or \
            Question(keywords, "will it precipitate today") or \
            Question(keywords, "could it rain precipitate today") or \
            Question(keywords, "raining today") or \
            Question(keywords, "is it going to rain today") or \
            Question(keywords, "going rain soon today") or \
            Question(keywords, "what is this precipitation chance"):
        if (int(json_data2['main']['pressure']) <= 1015 or (
                70 < int(json_data2['main']['humidity']) < 50)) and int(
            json_data2['main']['humidity']) != 100:
            phrase = selectandspeak(
                [f"There is a chance it may rain soon based on the pressure and humidity changes in the atmosphere.",
                 "Based off the local readings of barometric pressure and humidity, it may rain soon."])
        elif int(json_data2['main']['humidity']) >= 85:
            phrase = selectandspeak(
                ["Based off the values being reported, it should rain today if it's not already raining.",
                 "I would be surprised if it didn't rain today.",
                 "The humidity levels in the area are very high, so it is very likely."])
        else:
            phrase = selectandspeak(["I don't see a chance of rain today based off the reported values.",
                                     "I am not forecasting rain for today, atleast not at this moment.",
                                     "There is no precipitation forecasted for today."])

        universal.speak(phrase + " Would you like to hear the daily forecast?")
        queue = {
            'type': 'yesno',
            'keywords': ['sure', 'yes', 'good', 'great', 'no', 'bad', 'stop', 'quit',
                         'thanks', 'please']
        }

        def otherProcess(result):
            if result:
                universal.waitingForQuery = False
                keywordprocessor.Process("what is the weather today")
            else:
                universal.speak("Alright then. If you need anything let me know.")

        queue['process'] = otherProcess
        universal.query(queue)
        return True

    elif Question(keywords, "atmosphere changes") or \
            Question(keywords, "atmosphere pressure") or \
            Question(keywords, "barometric pressure") or \
            Question(keywords, "what is the atmospheric pressure"):

        averagePressure = round((int(json_data3['daily'][0]['pressure']) + int(json_data1['current']['pressure']) + int(
            json_data2['main']['pressure'])) / 3)
        result = "average"
        print(averagePressure)
        phrase = selectandspeak(
            [f"The current barometric pressure for the area is {str(averagePressure)} hectopascals.",
             f"I am reading {str(averagePressure)} hectopascals of pressure in the local atmosphere.",
             f"Openweathermap reports {str(averagePressure)} hectopascals of pressure in the area."])
        if averagePressure <= 1015:
            result = "low"
            phrase += selectandspeak(["That is a low reading for this area. Expect weather changes soon.",
                                      "With a reading that low, there is a potential for rain soon.",
                                      "Looks like it may rain soon."])
        elif averagePressure >= 1018:
            result = "high"
            phrase += selectandspeak(
                ["Seems like a high pressure front is approaching the area. Expect nice weather soon.",
                 "That's a higher level reading for this area.",
                 "Expect nice weather."])
        universal.speak((phrase + "         Would you like to hear the 7-day forecast?"))
        queue = {
            'type': 'yesno',
            'keywords': ['sure', 'yes', 'good', 'great', 'no', 'bad', 'stop', 'quit',
                         'thanks', 'please']
        }

        def otherProcess(result):
            if result:
                universal.waitingForQuery = False
                keywordprocessor.Process("what is the 7-day forecast")
            else:
                universal.speak("Alright then. If you need anything let me know.")

        queue['process'] = otherProcess
        universal.contextulizer(["askedpressurechanges", result])
        universal.query(queue)

        return True

    elif Question(keywords, "what is the weather tomorrow") or \
            Question(keywords, "what is tomorrow's weather") or \
            Question(keywords, "what is tomorrows weather"):

        day1 = [json_data3['daily'][0]['dt'], json_data3['daily'][0]["feels_like"]['day'],
                json_data3['daily'][0]["weather"][0]["description"]]
        phrase = selectandspeak(
            [f"For tomorrow, I am forecasting an average feels-like temperature of  {str(round(int(day1[1])))}°"
             f" and you should expect {str(day1[2])}.",
             f"Tomorrow I am expecting {str(day1[2])} and temperatures around {str(round(int(day1[1])))}°",
             f"You should expect {str(day1[2])}, with a {str(round(int(day1[1])))}° feels-like temperature."])

        universal.speak(phrase)
        return True

    elif (Question(keywords, "what is the seven day forecast") or \
          Question(keywords, "what is it like this week outside") or \
          Question(keywords, "what the 7-day forecast") or \
          Question(keywords, "what is the 7-day forecast this week") or \
          Question(keywords, "what is the weather this week") or \
          Question(keywords, "what's the weather this week") or \
          Question(keywords, "what is weekly forecast")):

        for word in keywords:
            if word in ["detailed", "advanced", 'advance', 'detail', 'details']: passedValue = "basic"
            if word in ['summary', "basic", "simple", "dimple", 'summarize', "summarized"]: passedValue = "simple"

        if not passedValue:
            universal.speak(selectandspeak([
                "Sorry for the delay, I was processing my forecast. Would you like the summarized or the detailed version?",
                "I can answer that for you, but I first need to know if you want the simple or advanced forecast.",
                "Would you like to hear the basic or advanced forecast?",
                "Alright, would you like to hear the summary or the full advanced forecast?",
                "I'm checking my sources now. Would you prefer the summarized or detailed forecast?"
            ]))

            queue = {
                'type': 'specific',
                'keywords': ['summary', "basic", "simple", "dimple", 'summarize', "summarized", "detailed", "advanced", 'advance', 'detail', 'details']}

            def otherProcess(res):
                print("returned query result    " + res)
                if res in ['summary', "basic", "simple", "dimple", 'summarize', "summarized"]:
                    print("determined summary")
                    universal.waitingForQuery = False
                    keywordprocessor.Process("what is the 7-day forecast", "simple")
                elif res in ["detailed", "advanced", 'advance', 'detail', 'details']:
                    print("determined basic")
                    universal.waitingForQuery = False
                    keywordprocessor.Process("what is the 7-day forecast", "basic")

            queue['process'] = otherProcess
            universal.query(queue)
            time.sleep(0.1)
            if queue in universal.currentQueries:
                universal.currentQueries.remove(queue)
            else:
                print(f"didn't find it in the queries. but i did find {universal.currentQueries}")

        else:
            try:
                if passedValue == "simple":
                    print("detected a simple search")
                    week = [
                        [1, json_data3['daily'][1]["pressure"], json_data3['daily'][1]["weather"][0]["main"],
                         json_data3['daily'][1]['temp']["min"], json_data3['daily'][1]['temp']["max"],
                         json_data3['daily'][1]["wind_speed"]],
                        [2, json_data3['daily'][2]["pressure"], json_data3['daily'][2]["weather"][0]["main"],
                         json_data3['daily'][2]['temp']["min"], json_data3['daily'][2]['temp']["max"],
                         json_data3['daily'][2]["wind_speed"]],
                        [3, json_data3['daily'][3]["pressure"], json_data3['daily'][3]["weather"][0]["main"],
                         json_data3['daily'][3]['temp']["min"], json_data3['daily'][3]['temp']["max"],
                         json_data3['daily'][3]["wind_speed"]],
                        [4, json_data3['daily'][4]["pressure"], json_data3['daily'][4]["weather"][0]["main"],
                         json_data3['daily'][4]['temp']["min"], json_data3['daily'][4]['temp']["max"],
                         json_data3['daily'][4]["wind_speed"]],
                        [5, json_data3['daily'][5]["pressure"], json_data3['daily'][5]["weather"][0]["main"],
                         json_data3['daily'][5]['temp']["min"], json_data3['daily'][5]['temp']["max"],
                         json_data3['daily'][5]["wind_speed"]],
                        [6, json_data3['daily'][6]["pressure"], json_data3['daily'][6]["weather"][0]["main"],
                         json_data3['daily'][6]['temp']["min"], json_data3['daily'][6]['temp']["max"],
                         json_data3['daily'][6]["wind_speed"]],
                        [7, json_data3['daily'][7]["pressure"], json_data3['daily'][7]["weather"][0]["main"],
                         json_data3['daily'][7]['temp']["min"], json_data3['daily'][7]['temp']["max"],
                         json_data3['daily'][7]["wind_speed"]]]
                    trendPhrase = weathertrendprocessor.trendFind(weeklyData=week, parseType="simple")
                    if trendPhrase:
                        pressureContext = universal.contextulizer("askedpressurechanges", method="check")
                        weatherContext = universal.contextulizer("askedweathertrend", method="check")
                        print(pressureContext, weatherContext)
                        universal.speak(trendPhrase)
                        if pressureContext and weatherContext:
                            phrase = []
                            if pressureContext[1] == "high" and (weatherContext[1] == "good" or weatherContext[1] == "fair"):
                                phrase = ["The fair forecast would be result of the high pressure changes. How interesting the atmosphere is.",
                                          "And the decent weather this week would be result of the high atmosphere pressure you asked about earlier.",
                                          "High pressure systems can cause calm, and relaxed weather. There must be one in the area, like we talked about earlier."]
                            elif pressureContext[1] == "low" and (weatherContext[1] == "fair" or weatherContext[1] == "poor"):
                                phrase = ["The low barometric pressure we talked about earlier may be a cause of the poor weather this week. I can keep you updated.",
                                          "Low pressure systems are notorious for cause chaotic weather. Keep an eye out and ask me for weather alerts often.",
                                          "I believe their may be a low pressure system in our area, like we discussed earlier. Be ready for chaotic weather conditions."]
                            elif (pressureContext[1] == "high" or pressureContext[1] == "low") and (weatherContext[1] == "poor" or weatherContext[1] == "windy"):
                                phrase = ["I am noticing some strange weather patterns in this area. My forecast may not be accurate.",
                                          "There seems to be a lot of fluctuation in the atmosphere. I can keep you informed on any major changes.",
                                          "A bit of a strange weather pattern in this area. I don't know what to entirely make of it yet. I can keep you updated."]
                            elif pressureContext[1] == "average" and (weatherContext[1] == "good" or weatherContext[1] == "fair"):
                                phrase = ["It doesn't really seem like much is happening in the atmosphere. Try asking me about barometric pressure again later for updates.",
                                          "Like I mentioned earlier, the barometric pressure is a pretty standard reading. Average pressure is more-than-likely the reason the forecast is passive.",
                                          "With an average barometric pressure like the one I mentioned earlier, I'm not surprised at the predicted pacified forecast."]

                            if len(phrase) > 0:
                                universal.speak(selectandspeak(phrase))
                        return True
                    else:
                        return False
                if passedValue == "basic":
                    print("detected advanced in command processor")
                    week = [[1, json_data3['daily'][1]], [2, json_data3['daily'][2]], [3, json_data3['daily'][3]], [4, json_data3['daily'][4]], [5, json_data3['daily'][5]], [6, json_data3['daily'][6]], [7, json_data3['daily'][7]]]
                    trendPhrase = weathertrendprocessor.trendFind(weeklyData=week, parseType="basic")
                    if trendPhrase:
                        pressureContext = universal.contextulizer("askedpressurechanges", method="check")
                        weatherContext = universal.contextulizer("askedweathertrend", method="check")
                        print(pressureContext, weatherContext)
                        universal.speak(trendPhrase)
                        if pressureContext and weatherContext:
                            phrase = []
                            if pressureContext[1] == "high" and (weatherContext[1] == "good" or weatherContext[1] == "fair"):
                                phrase = ["The fair forecast would be result of the high pressure changes. How interesting the atmosphere is.",
                                          "And the decent weather this week would be result of the high atmosphere pressure you asked about earlier.",
                                          "High pressure systems can cause calm, and relaxed weather. There must be one in the area, like we talked about earlier."]
                            elif pressureContext[1] == "low" and (weatherContext[1] == "fair" or weatherContext[1] == "poor"):
                                phrase = ["The low barometric pressure we talked about earlier may be a cause of the poor weather this week. I can keep you updated.",
                                          "Low pressure systems are notorious for cause chaotic weather. Keep an eye out and ask me for weather alerts often.",
                                          "I believe their may be a low pressure system in our area, like we discussed earlier. Be ready for chaotic weather conditions."]
                            elif (pressureContext[1] == "high" or pressureContext[1] == "low") and (weatherContext[1] == "poor" or weatherContext[1] == "windy"):
                                phrase = ["I am noticing some strange weather patterns in this area. My forecast may not be accurate.",
                                          "There seems to be a lot of fluctuation in the atmosphere. I can keep you informed on any major changes.",
                                          "A bit of a strange weather pattern in this area. I don't know what to entirely make of it yet. I can keep you updated."]
                            elif pressureContext[1] == "average" and (weatherContext[1] == "good" or weatherContext[1] == "fair"):
                                phrase = ["It doesn't really seem like much is happening in the atmosphere. Try asking me about barometric pressure again later for updates.",
                                          "Like I mentioned earlier, the barometric pressure is a pretty standard reading. Average pressure is more-than-likely the reason the forecast is passive.",
                                          "With an average barometric pressure like the one I mentioned earlier, I'm not surprised at the predicted pacified forecast."]

                            if len(phrase) > 0:
                                universal.speak(selectandspeak(phrase))
                return True
            except Exception as err:
                print(repr(err))
                traceback.print_tb(err.__traceback__)
                return True
    return False


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


def ProcessQuery(keywords, query):
    print("processing query")
    status = query['process'](keywords)
    if not status:
        return False
    universal.waitingForQuery = False
    universal.currentQueries.remove(universal.currentQueries.index(query))
    print("processed")
    return True


def Questions(keywords, originaltext, passedValue=False):
    if Question(keywords, "what is the time") or \
            Question(keywords, "what is the current time"):
        now = datetime.datetime.now()
        phrase = selectandspeak([f"The current time is {now.strftime('%I:%M %p')}.",
                                 f"It's currently {now.strftime('%I:%M %p')}.",
                                 f"The time now is {now.strftime('%I:%M %p')}",
                                 now.strftime('%I:%M %p'),
                                 f"It is currently {now.strftime('%I:%M %p')}"])
        universal.speak(phrase)
        return True
    elif Question(keywords, "repeat that"):
        phrase = selectandspeak(["I said, ", "No problem, I said", "Alright, "])
        phrase += "             " + universal.lastPhrase

        universal.speak(phrase)
        return True
    elif Question(keywords, "how are you") or \
            Question(keywords, "how are you today") or \
            Question(keywords, "what's up"):
        reply = selectandspeak(["Not too bad for a programmable voice assistant. How about you?",
                                "I'm programmed to have a good day today, how about you?",
                                "I'm having a great day, thank you for asking. How about you?"])
        universal.speak(reply)
        queue = {
            'type': 'specific',
            'keywords': ["good thanks for asking", "great thank you", "doing good thank you", "thank you",
                         "bad", "horrible", "not good", "bad day", "sad today", "doing okay today", "doing ok today",
                         "doing alright",
                         "feeling okay", "feeling good", 'feeling nauseous', "feeling sick"]}

        def process(keywords):
            if ("good" in keywords or "great" in keywords) and (
                    "not" not in keywords and ("good" not in keywords or "great" not in keywords)):
                reply = selectandspeak(
                    ["Glad to hear it.", "Good to hear. If you'd like I could tell you a fun fact. Just ask."])
                universal.speak(reply)
            elif "bad" in keywords or (
                    "not" in keywords and ("good" in keywords or "good" in keywords)) or "terrible" in keywords or \
                    "horrible" in keywords or "nauseous" in keywords or "sick" in keywords:
                reply = selectandspeak(["Sorry to hear that. Would you like to hear a fun fact to cheer you up?",
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

        queue['process'] = process
        print(queue)
        universal.query(queue)
        print("removing original query")
        if queue in universal.currentQueries:
            universal.currentQueries.remove(queue)
        else:
            print(f"didn't find it in the queries. but i did find {universal.currentQueries}")
        return True
    elif Question(keywords, "what is today's news") or \
            Question(keywords, "what is the news for today") or \
            Question(keywords, "what is happening") or \
            Question(keywords, "what is the daily news"):
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
    elif Question(keywords, "what is today numerical") or \
            Question(keywords, "what is today's date") or \
            Question(keywords, "what is the date today"):

        now = datetime.datetime.now()
        universal.speak(f"Today is {now.strftime('%A    , %B %d     %Y')}")

        return True

    elif ("what" in keywords or "what's" in keywords) and mathCheck(keywords):
        answer, problem = calculate(keywords)
        if not answer:
            phrase = selectandspeak(["I couldn't seem to find an answer to that math problem.",
                                     "I couldn't calculate the correct answer.",
                                     "Something didn't process correctly with that equation."])
        else:
            phrase = selectandspeak([f"The answer to {problem} is {answer}.",
                                     f"When I processed {problem}, I concluded {answer}.",
                                     f"I calculated {problem} with the end result of {answer}."])

        universal.speak(phrase)
        return True
    else:
        #answer = searchparser.search(originaltext)
        #if answer:
            #if 'snippet' in answer:
                #universal.speak(f"I searched that for you. {answer['answer']}. I also have more information, "
                                #f"{answer['snippet']}")
            #elif 'answer' in answer:
                #universal.speak(f"I searched that for you.  {answer['answer']}.")
            #elif 'error' in answer:
                #universal.speak(answer['error'])
            #return True
        return Exception("No result")


def process(keywords, scores=False, originaltext=False, passedValue=False):
    if scores:
        plantscore = scores[0]
        questionscore = scores[1]
        weatherscore = scores[2]
    else:
        plantscore = questionscore = weatherscore = 0

    if weatherscore > plantscore and weatherscore > questionscore:
        if passedValue:
            result = Weather(keywords, passedValue)
        else:
            result = Weather(keywords)
        if result:
            return True
        else:
            return False
    elif questionscore > weatherscore and questionscore > plantscore:
        if passedValue:
            result = Questions(keywords, originaltext, passedValue)
        else:
            result = Questions(keywords, originaltext)
        if result:
            return True
        else:
            return False
    else:
        result = Weather(keywords, passedValue)
        if not result: result = Questions(keywords, originaltext, passedValue)
        if not result: print("Failure to find result")
        if result:
            return True
        else:
            print("Could not find a solution to \n      KW:" + keywords + "\n      OT:" + originaltext)
