import requests
import random
from randfacts import get_fact
import time
import traceback

import commandprocessor
import universal
import keywordprocessor
import weathertrendprocessor

weatherApi1 = "https://api.openweathermap.org/data/2.5/onecall?lat=36.052448&lon=-95.790810&exclude=hourly,daily&appid=8f2118090e07640ec49e91a59dedfadd"  # Used for the weather
weatherApi2 = "https://api.openweathermap.org/data/2.5/weather?zip=74012,us&appid=8f2118090e07640ec49e91a59dedfadd"
weatherApi3 = "https://api.openweathermap.org/data/2.5/onecall?lat=36.052448&lon=-95.790810&units=imperial&exclude=hourly,current,minutely&appid=8f2118090e07640ec49e91a59dedfadd"
dailyWeatherJSONBasic = ""
dailyWeatherJSONAdvc = ""
weeklyDataJSON = ""

qb = {}

### Weather: Questionbank
###     'temp' :  Question
###             'keys'  :   ['what is the current temperature', 'what does it feel like outside', 'what is the temperature outside']
###             'function' : def func()


def checkAverages(data, data2):
    fl = data['main']['feels_like']  # gets the feels like temp
    tempmin = data['main']['temp_min']
    tempmax = data['main']['temp_max']

    fl = round(9 / 5 * (fl - 273) + 32)  # converts the temp (kelvin) into fahrenheit
    tempmin = round(9 / 5 * (tempmin - 273) + 32)  # converts the temp (kelvin) into fahrenheit
    tempmax = round(9 / 5 * (tempmax - 273) + 32)  # converts the temp (kelvin) into fahrenheit

    if fl > 90 or tempmax > 90:
        reply = commandprocessor.selectandspeak(
            [f"It looks like it's going to be a hot day today. The high is {str(tempmax)}° fahrenheit.",
             f"It's pretty hot outside. The high is {str(tempmax)}° fahrenheit.",
             f"Prepare yourself for a hot day. The high is {str(tempmax)}° fahrenheit."])

        if round(int(data2['current']['uvi'])) >= 8:
            reply += (commandprocessor.selectandspeak(["UV rays are fairly potent. Make sure to wear sunscreen today.",
                                      "The Sun is beaming bright. Make sure you stay protected.",
                                      f"I am forecasting UV rays reaching {round(int(data2['current']['uvi']))} today."]))
        else:
            reply += (
                commandprocessor.selectandspeak(["In South Carolina, they would describe today as being hot enough to scald a lizard.",
                                "Make sure you stay hydrated.",
                                "In Wisconsin, Pennsylvania, and New York, it is common for some people to say"
                                "today is hotter than dutch love. Not in reference to the netherlands."]))
    elif fl < 30 or tempmin < 30:
        reply = commandprocessor.selectandspeak(
            [f"    It looks like it's going to be fairly cold. The low is {str(tempmin)}° fahrenheit.",
             f"    It's pretty cold outside. The low is {str(tempmin)}° fahrenheit.",
             f"    Get ready for a chilly day. The low  is {str(tempmin)}° fahrenheit."])
        reply += commandprocessor.selectandspeak(["While forecasting this, I discovered a new phrase. It's cold as balls.",
                                  "Now would be an optimal time for chicken noodle soup and hot chocolate.",
                                  "There is always a chance it could randomly snow. Rely on that."])

    else:
        reply = commandprocessor.selectandspeak(["Seems like an average day. Nothing to note.",
                                "I am not forecasting anything other than normal conditions.",
                                "Today's forecast seems mild. Remember to enjoy the nice weather."])

    if int(data["wind"]["speed"]) >= 10:
        reply += commandprocessor.selectandspeak(["It looks like it's going to be a windy day today.",
                                 "I am noticing an increase in wind gusts and wind speed.",
                                 "It's fairly windy today. Check the forecast or ask me for more details."])

    if (int(data['main']['pressure']) <= 1015 or int(data['main']['humidity']) > 70) and int(
            data['main']['humidity']) != 100:
        reply += commandprocessor.selectandspeak(
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
        phrase = commandprocessor.selectandspeak([
            f"There is currently a {alert[0]['event']} in your area issued by {alert[0]['sender_name']} It reads as {description[0]} ... and continues with {description[1]}.",
            f"{alert[0]['sender_name']} has issued a {alert[0]['event']} for this area. The description reads {description[0]} .... {description[1]}."])
        reply += phrase

        rando = random.choice([True, False, False])
        if rando:
            reply += commandprocessor.selectandspeak([f"I have a fun fact for you. {get_fact()}",
                                     f"And to finish your weather report, I have a fun fact {get_fact()}",
                                     f"Also, I found a fun fact for you. {get_fact()}"])
    return reply

qb['weatheroutside'] = {}
qb['weatheroutside']['keys'] = ["what weather today", "what weather outside" , "what's the current weather",
                                "what's the weather outside", "what does it feel like outside", "what is the weather today",
                                "What's today's weather", "what is weather outside currently"]
qb["weatheroutside"]['require'] = ["outside", "today", "weather", "today's", "current"]
def weatherOutside(keywords, info, passedValue=False, client=False):
    formatted_data = info[0]
    tempmin = info[1]
    tempmax = info[2]
    feellike = info[3]

    if "rain" in keywords:
        if (int(dailyWeatherJSONAdvc['main']['pressure']) > 1015 or int(dailyWeatherJSONAdvc['main']['humidity']) > 70) and int(
                dailyWeatherJSONAdvc['main']['humidity']) != 100:
            universal.speak(
                f"There is a chance it may rain based on the pressure and humidity changes in the atmosphere." +
                ' Would you like to hear the seven day forecast I have made?', client)
            queue = {
                'type': 'yesno',
                'keywords': ['sure', 'yes', 'good', 'great', 'no', 'bad', 'stop', 'quit',
                             'thanks', 'please']
            }

            def otherProcess(result):
                if result:
                    keywordprocessor.Process("what is the 7-day forecast")
                else:
                    universal.speak("Alright then. If you need anything let me know.", client)

            queue['process'] = otherProcess
            universal.query(queue)
        return True
    else:
        status = checkAverages(dailyWeatherJSONAdvc, dailyWeatherJSONBasic)
        phrase = commandprocessor.selectandspeak(
            [f"Today's weather is {str(formatted_data)} and it currently feels like {str(feellike)}° fahrenheit.",
             f"For today I am forecasting with {str(formatted_data)} and a feels like temperature of {str(feellike)}° fahrenheit.",
             f"It currently feels like {str(feellike)}° fahrenheit outside and you should expect {str(formatted_data)}."])
        universal.speak(phrase + status, client)
    universal.contextulizer(["weatheroutside"])
    return True
qb['weatheroutside']['function'] = weatherOutside

qb['tempoutside'] = {}
qb['tempoutside']['keys'] = ["what is the high today", "what is the low today", "is it going to be hot today",
                             "is it hot outside today", "is it cold outside today", "should i wear a jacket today",
                             "is it going to be hot today", "is it going to be cold today"]
def tempOutside(keywords, info, passedValue=False, client=False):
    formatted_data = info[0]
    tempmin = info[1]
    tempmax = info[2]
    feellike = int(info[3])

    if feellike >= 100:
        context = "very hot"
    elif 80 >= feellike <= 99:
        context = "hot"
    elif 50 >= feellike <= 79:
        context = "fair"
    elif 32 >= feellike <= 49:
        context = "cold"
    elif feellike < 32:
        context = "very cold"

    mainPhraseChoice = [f"It currently feels like {feellike}° fahrenheit. Today's high is {tempmax}° with a low of {tempmin}°.",
                        f"Seems like today will be {context}. I'm reading a feels like of {feellike}.",
                        f"Expect a {context} day today. The current feels like is {feellike}.",
                        f"I'm forecasting some {context} temperatures. The current feels like is {feellike}."]

    contextAddition = {
        "cold": ["It will be pretty chilly today. You should wear a jacket.",
                 "You should consider wearing a jacket today.",
                 "With temperatures being that low, you should dress for the cold."],
        "hot": ["It will be pretty warm today. Make sure to dress appropriately.",
                "That's a fairly warm temperature. Drink plenty of water to prevent dehydration.",
                "Prepare to sweat today. It'll be pretty warm outside."],
        "very cold": ["Temperatures are below freezing, you'll want to dress in layers today.",
                      "It will be very cold outside today. Make sure you dress appropriately.",
                      "Anticipate it being pretty chilly all day. It's cold enough for ice to form."],
        "very hot": ["It will be pretty hot outside today. I'm expecting temperatures out of normal ranges.",
                     "Anticipate it being considerably hot outside today. Ensure you're not dehydrating yourself.",
                     "Temperatures will be out of the normal range today. Check for a heat advisory."]}


    phrase = commandprocessor.selectandspeak(mainPhraseChoice)
    if context in contextAddition:
        phrase += commandprocessor.selectandspeak(contextAddition[context])

    universal.speak(phrase, client)
    return True
qb['tempoutside']['function'] = tempOutside

qb['raincheck'] = {}
qb['raincheck']['keys'] = ["do you think it will rain soon", "will it rain today", "is there a chance of rain today",
                           "will it precipitate today", "could it rain precipitate today", "raining today",
                           "is it going to rain today", "going rain soon today", "what is this precipitation chance"]
qb['raincheck']['require'] = ["rain", "precipitate", "raining"]
def rainCheck(keywords, info, passedValue=False, client=False):
    if (int(dailyWeatherJSONAdvc['main']['pressure']) <= 1015 or (
            70 < int(dailyWeatherJSONAdvc['main']['humidity']) > 50)) and int(
        dailyWeatherJSONAdvc['main']['humidity']) != 100:
        phrase = commandprocessor.selectandspeak(
            [f"There is a chance it may rain soon based on the pressure and humidity changes in the atmosphere.",
             "Based off the local readings of barometric pressure and humidity, it may rain soon."])
    elif int(dailyWeatherJSONAdvc['main']['humidity']) >= 70:
        phrase = commandprocessor.selectandspeak(
            ["Based off the values being reported, it should rain today if it's not already raining.",
             "I would be surprised if it didn't rain today.",
             "The humidity levels in the area are very high, so it is very likely."])
    else:
        phrase = commandprocessor.selectandspeak(["I don't see a chance of rain today based off the reported values.",
                                 "I am not forecasting rain for today, at least not at this moment.",
                                 "There is no precipitation forecasted for today."])

    universal.speak(phrase + " Would you like to hear the daily forecast?", client)

    queue = {
        'type': 'yesno',
        'keywords': ['sure', 'yes', 'good', 'great', 'no', 'bad', 'stop', 'quit',
                     'thanks', 'please']
    }

    def otherProcess(result):
        if result:
            keywordprocessor.Process("what is the weather today")
        else:
            universal.speak("Alright then. If you need anything let me know.", client)
        universal.waitingForQuery = False

    queue['process'] = otherProcess
    universal.query(queue)

    return True
qb['raincheck']['function'] = rainCheck

qb['pressureoutside'] = {}
qb['pressureoutside']['keys'] = ["what atmosphere changes", "what atmosphere pressure", "what barometric pressure",
                                 "what is the atmospheric pressure"]
qb['pressureoutside']['require'] = ["barometric", "atmosphere", "atmospheric", "pressure"]
def pressureOutside(keywords, info, passedValue=False, client=False):
    averagePressure = round((int(weeklyDataJSON['daily'][0]['pressure']) + int(dailyWeatherJSONBasic['current']['pressure']) + int(dailyWeatherJSONAdvc['main']['pressure'])) / 3)
    result = "average"

    phrase = commandprocessor.selectandspeak(
        [f"The current barometric pressure for the area is {str(averagePressure)} hectopascals.",
         f"I am reading {str(averagePressure)} hectopascals of pressure in the local atmosphere.",
         f"Openweathermap reports {str(averagePressure)} hectopascals of pressure in the area."])

    if averagePressure <= 1014:
        result = "low"
        phrase += commandprocessor.selectandspeak(["That is a lower reading for this area. Expect weather changes soon.",
                                  "With a reading on the low end, there is a potential for rain soon.",
                                  "Looks like it may rain soon."])
    elif averagePressure >= 1018:
        result = "high"
        phrase += commandprocessor.selectandspeak(
            ["Seems like a high pressure front is approaching the area. Expect nice weather soon.",
                                "That's a higher level reading for this area.",
                                "Expect nice weather."])

    universal.speak(phrase + "         Would you like to hear the 7-day forecast?", client)

    queue = {
        'type': 'yesno',
        'keywords': ['sure', 'yes', 'good', 'great', 'no', 'bad', 'stop', 'quit',
                     'thanks', 'please']
    }

    def otherProcess(result):
        if result:
            keywordprocessor.Process("what is the 7-day forecast")
        else:
            universal.speak("Alright then. If you need anything let me know.", client)
        universal.waitingForQuery = False

    queue['process'] = otherProcess
    universal.contextulizer(["askedpressurechanges", result])
    universal.query(queue)

    return True
qb['pressureoutside']['function'] = pressureOutside

qb['tomorrowcheck'] = {}
qb['tomorrowcheck']['keys'] = ["what is the weather tomorrow", "what is tomorrow's weather", "what is tomorrows weather"]
qb['tomorrowcheck']['require'] = ['tomorrow', "tomorrow's", "tomorrows"]
def tomorrowCheck(keywords, info, passedValue=False, client=False):

    day1 = [weeklyDataJSON['daily'][0]['dt'], weeklyDataJSON['daily'][0]["feels_like"]['day'], weeklyDataJSON['daily'][0]["weather"][0]["description"]]

    phrase = commandprocessor.selectandspeak([
         f"For tomorrow, I am forecasting an average feels-like temperature of  {str(round(int(day1[1])))}°"
         f" and you should expect {str(day1[2])}.",
         f"Tomorrow I am expecting {str(day1[2])} and temperatures around {str(round(int(day1[1])))}°",
         f"You should expect {str(day1[2])}, with a {str(round(int(day1[1])))}° feels-like temperature."])

    universal.speak(phrase, client)

    return True
qb['tomorrowcheck']['function'] = tomorrowCheck

qb['sevendaycheck'] = {}
qb['sevendaycheck']['keys'] = ["what is the seven day forecast", "what is it like this week", "what the 7-day forecast",
                               "what is the 7-day forecast this week", "what is the weather this week", "what's the weather this week",
                               "what is weekly forecast"]
qb['sevendaycheck']['require'] = ["week", "7-day", "seven", "week's", "weeks", "weekly"]
def sevenDayCheck(keywords, info, passedValue=False, client=False):
  for word in keywords:
    if word in ["detailed", "advanced", 'advance', 'detail', 'details']: passedValue = "basic"
    if word in ['summary', "basic", "simple", "dimple", 'summarize', "summarized"]: passedValue = "simple"
    if not passedValue:
        universal.speak(commandprocessor.selectandspeak([
            "Sorry for the delay, I was processing my forecast. Would you like the summarized or the detailed version?",
            "I can answer that for you, but I first need to know if you want the simple or advanced forecast.",
            "Would you like to hear the basic or advanced forecast?",
            "Alright, would you like to hear the summary or the full advanced forecast?",
            "I'm checking my sources now. Would you prefer the summarized or detailed forecast?"]), client)

        queue = {
            'type': 'specific',
            'keywords': ['summary', "basic", "simple", "dimple", 'summarize', "summarized", "detailed", "advanced", 'advance', 'detail', 'details']}

        def otherProcess(res):
            if res in ['summary', "basic", "simple", "dimple", 'summarize', "summarized"]:
                universal.waitingForQuery = False
                keywordprocessor.Process("what is the 7-day forecast", "simple")
            elif res in ["detailed", "advanced", 'advance', 'detail', 'details']:
                universal.waitingForQuery = False
                keywordprocessor.Process("what is the 7-day forecast", "basic")

        queue['process'] = otherProcess
        universal.query(queue)
        time.sleep(0.1)
        if queue in universal.currentQueries:
            universal.currentQueries.remove(queue)
    else:
        try:
            if passedValue == "simple":
                week = [
                    [1, weeklyDataJSON['daily'][1]["pressure"], weeklyDataJSON['daily'][1]["weather"][0]["main"],
                     weeklyDataJSON['daily'][1]['temp']["min"], weeklyDataJSON['daily'][1]['temp']["max"],
                     weeklyDataJSON['daily'][1]["wind_speed"]],
                    [2, weeklyDataJSON['daily'][2]["pressure"], weeklyDataJSON['daily'][2]["weather"][0]["main"],
                     weeklyDataJSON['daily'][2]['temp']["min"], weeklyDataJSON['daily'][2]['temp']["max"],
                     weeklyDataJSON['daily'][2]["wind_speed"]],
                    [3, weeklyDataJSON['daily'][3]["pressure"], weeklyDataJSON['daily'][3]["weather"][0]["main"],
                     weeklyDataJSON['daily'][3]['temp']["min"], weeklyDataJSON['daily'][3]['temp']["max"],
                     weeklyDataJSON['daily'][3]["wind_speed"]],
                    [4, weeklyDataJSON['daily'][4]["pressure"], weeklyDataJSON['daily'][4]["weather"][0]["main"],
                     weeklyDataJSON['daily'][4]['temp']["min"], weeklyDataJSON['daily'][4]['temp']["max"],
                     weeklyDataJSON['daily'][4]["wind_speed"]],
                    [5, weeklyDataJSON['daily'][5]["pressure"], weeklyDataJSON['daily'][5]["weather"][0]["main"],
                     weeklyDataJSON['daily'][5]['temp']["min"], weeklyDataJSON['daily'][5]['temp']["max"],
                     weeklyDataJSON['daily'][5]["wind_speed"]],
                    [6, weeklyDataJSON['daily'][6]["pressure"], weeklyDataJSON['daily'][6]["weather"][0]["main"],
                     weeklyDataJSON['daily'][6]['temp']["min"], weeklyDataJSON['daily'][6]['temp']["max"],
                     weeklyDataJSON['daily'][6]["wind_speed"]],
                    [7, weeklyDataJSON['daily'][7]["pressure"], weeklyDataJSON['daily'][7]["weather"][0]["main"],
                     weeklyDataJSON['daily'][7]['temp']["min"], weeklyDataJSON['daily'][7]['temp']["max"],
                     weeklyDataJSON['daily'][7]["wind_speed"]]]
                trendPhrase = weathertrendprocessor.trendFind(weeklyData=week, parseType="simple")
                if trendPhrase:
                    pressureContext = universal.contextulizer("askedpressurechanges", method="check")
                    weatherContext = universal.contextulizer("askedweathertrend", method="check")
                    universal.speak(trendPhrase, True, client)
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
                            universal.speak(commandprocessor.selectandspeak(phrase), client)
                    return True
                else:
                    return False
            if passedValue == "basic":
                week = [[1, weeklyDataJSON['daily'][1]], [2, weeklyDataJSON['daily'][2]], [3, weeklyDataJSON['daily'][3]], [4, weeklyDataJSON['daily'][4]], [5, weeklyDataJSON['daily'][5]], [6, weeklyDataJSON['daily'][6]], [7, weeklyDataJSON['daily'][7]]]
                trendPhrase = weathertrendprocessor.trendFind(weeklyData=week, parseType="basic")
                if trendPhrase:
                    pressureContext = universal.contextulizer("askedpressurechanges", method="check")
                    weatherContext = universal.contextulizer("askedweathertrend", method="check")
                    universal.speak(trendPhrase, True, client)
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
                            universal.speak(commandprocessor.selectandspeak(phrase), client)
            return True
        except Exception as err:
            print("[ERRO] " + repr(err))
            traceback.print_tb(err.__traceback__)
            return True
    return False
qb['sevendaycheck']['function'] = sevenDayCheck


qb['valueUpdate'] = {}
qb['valueUpdate']['keys'] = ["VALUEUPDATE", "valueupdate"]
qb['valueUpdate']['require'] = ["VALUEUPDATE", "valueupdate"]
def valueUpdate(keywords, info, passedValue=False, client=False):

    global dailyWeatherJSONBasic
    global dailyWeatherJSONAdvc
    global weeklyDataJSON

    dailyWeatherJSONBasic = requests.get(weatherApi1).json()  # connects to the url
    dailyWeatherJSONAdvc = requests.get(weatherApi2).json()
    weeklyDataJSON = requests.get(weatherApi3).json()
    formatted_data = dailyWeatherJSONAdvc['weather'][0]['description']  # gets the basic data
    temp = dailyWeatherJSONAdvc['main']['feels_like']  # gets the feels like temp

    def convert(value):
        return round(9 / 5 * ((int(value)) - 273) + 32)

    tempmin = convert(dailyWeatherJSONAdvc['main']['temp_min'])
    tempmax = convert(dailyWeatherJSONAdvc['main']['temp_max'])
    feellike = convert(dailyWeatherJSONAdvc['main']['feels_like'])

    weatherResult = {
        'min': tempmin,
        'max': tempmax,
        'feellike': feellike,
        'humidity': dailyWeatherJSONAdvc['main']['humidity'],
        'pressure': dailyWeatherJSONAdvc['main']['pressure'],
        'main': dailyWeatherJSONAdvc['weather'][0]['main'],
        'dt': dailyWeatherJSONAdvc['dt']
    }

    if not universal.hourWeather:
        universal.hourWeather = weatherResult
    else:
        hourTime = universal.hourWeather['dt']
        if (hourTime + 3600) <= weatherResult['dt']:
            universal.hourWeather = weatherResult

    universal.currentWeather = weatherResult
    if passedValue:
        return weatherResult
    else:
        return True
qb['valueUpdate']['function'] = valueUpdate


def process(keywords, passedValue=False, client=False):
    """Process weather commands, needs keywords(list) and can take a passedValue(any)"""

    valueUpdate(keywords, None, None)

    formatted_data = dailyWeatherJSONAdvc['weather'][0]['description']  # gets the basic data
    temp = dailyWeatherJSONAdvc['main']['feels_like']  # gets the feels like temp

    def convert(value):
        return round(9 / 5 * ((int(value)) - 273) + 32)

    tempmin = convert(dailyWeatherJSONAdvc['main']['temp_min'])
    tempmax = convert(dailyWeatherJSONAdvc['main']['temp_max'])
    feellike = convert(dailyWeatherJSONAdvc['main']['feels_like'])

    info = [formatted_data, tempmin, tempmax, feellike]

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
                                print(f"[PROC]  len [X] {question}")
                        else:
                            print(f"[PROC]  TP [X] {question}")
                    else:
                        points += 1

                        if points > (len(keywords) * .74) or points > (len(phrase) * .74):
                            questionChoices.insert(0, [question, points])
                        else:
                            print(f"[PROC]  len [X] {question}")
    if len(questionChoices) > 0:
        largestNumber = 0
        for choice in questionChoices:
            if largestNumber < choice[1]:
                largestNumber = choice[1]
        debounce = False
        for choice in questionChoices:
            if choice[1] == largestNumber and not debounce:
                success = qb[choice[0]]['function'](keywords, info, passedValue, client)
                debounce = True

        if success:
            return True
        else:
            return False
    else:
        return False