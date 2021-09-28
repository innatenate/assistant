import traceback
import commandprocessor
import universal

phrases = {
    "moderate rain": ["I am expecting a moderate amount of rain throughout the week.",
                      "Prepare for a moderate amount of rain this week.",
                      "I am also detecting a moderate amount of rain."],
    "high rain": ["Expect heavy showers, maybe some thunderstorms. Who knows? I know. Thunderstorms.",
                  "I am anticipating a large amount of rain.",
                  "There are a large amount of showers and thunderstorms in the area. Expect for a couple of days."],
    'moderate clouds': ["Expect a moderate amount of clouds throughout your forecast.",
                        "I am expecting a moderate amount of clouds.",
                        "Clouds, clouds, clouds. Nothing but clouds."],
    "high clouds": ["I am detecting a large amount of clouds. Expect cloudy skies.",
                    "Nothing but clouds. Literally. I am expecting nothing but a predominance of clouds.",
                    "Expect a large amount of clouds this week."],
    'moderate clear': ["I am not expecting any tremendous weather. Seems pacified for now.",
                       "A high pressure system must be in the area. There is a surplus of clear skies.",
                       "Seems like this week is fairly easy. Nothing but clear skies for most of it."],
    "high clear": ["I am calculating a rife of clear skies.",
                   "Expect nothing but clear skies. I don't see anything else but clear skies.",
                   "No rain expected this week, no clouds even. Just clear skies."],
    "chance snow": ["I've noticed a chance of snow or ice in the forecast! How exciting.",
                    "There may be a small amount of snow or ice this week.",
                    "I've found a chance of snow or ice in the forecast."],
    'moderate snow': ["This area is expecting some snow or ice this week",
                      "A moderate amount of snow or ice this week. It more than likely won't last long.",
                      "Expect a moderate amount of snow or ice in your area."],
    "high snow": ["It'll be a winter wonderland this week. Enjoy the rife of snow.",
                  "Nothing but snow and ice in my forecast this week.",
                  "I expect a large amount of snow and ice in your area."],

    'rising': {
        "one": {
            "temperature": ["Expect rising temperatures throughout your forecast.",
                            "I am noticing a trend of rising temperatures.",
                            "Seems like temperatures in your area are rising."],
            "pressure": ["I've noticed a trend of rising barometric pressure in your area.",
                         "I've noticed the pressure is rising this week. Expect a great forecast.",
                         "I've detected that the atmospheric pressure seems to be rising."],
            "winds": ["I'm noticing a lot of strong winds this week.",
                      "Seems like winds will be pretty strong this week.",
                      "I am forecasting some strong winds this week."],
            "wind": ["I'm noticing a lot of strong winds this week.",
                      "Seems like winds will be pretty strong this week.",
                      "I am forecasting some strong winds this week."]},
        "two": {
            "temperature/pressure": [
                "I am forecasting rising temperatures and pressures, that typically means good weather.",
                "I have detected a typical weather pattern. Both temperatures and barometric pressure are rising.",
                "Expect a week of good weather with the temperature and barometric pressure rising."],
            "pressure/wind": ["Seems like there's a lot of fluctuation in your area with high pressures and winds.",
                              "I am detecting a weird pattern of high barometric pressure and heavy winds.",
                              "The forecast shows a trend of high barometric pressure and high wind speeds."]},
        "three": ["I am noticing temperatures, barometric pressure, and wind speeds rising this week.",
                  "There is a trend of rising temperatures, pressure, and wind speeds. There is a commotion in the area.",
                  "Seems like there's a pattern of rising temperatures, pressures, and wind speeds. That may indicate"
                  " interesting weather this week or next."]},
    'lowering': {
        "one": {
            "temperature": ["I am forecasting a decrease in temperatures this week.",
                            "Expect temperatures to get colder as the week progresses.",
                            "Lowering temperatures are present trend in this forecast."],
            "pressure": ["The barometric pressure is decreasing in this area.",
                         "I have also detected a plunge in atmospheric pressure this week.",
                         "Barometric pressures seem to be decreasing."],
            "winds": ["Winds are dying down this week.",
                      "Wind speeds are calming down towards the end of forecast.",
                      "I am detecting a decrease in wind speeds throughout the week."],
            "wind": ["Winds are dying down this week.",
                      "Wind speeds are calming down towards the end of forecast.",
                      "I am detecting a decrease in wind speeds throughout the week."]},
        "two": {
            "temperature/pressure": [
                "Both temperature and barometric pressure are decreasing this week. Expect unpleasant weather.",
                "I've detected a decrease in temperature and barometric pressure. This may indicate unsettled cold fronts or low pressure systems.",
                "Temperatures and barometric pressures are dropping towards the end of my forecast."],
            "wind/temperature": ["Both wind speeds and temperatures are decreasing throughout the forecast.",
                                 "There is a trend of reduction in wind speeds and temperatures throughout the week.",
                                 "I am noticing a decrease in wind speeds and temperatures."]},
        "three": [
            "I've noticed a bizarre pattern of temperatures, pressures and wind speeds lowering throughout the week.",
            "There seems to be a decrease in temperature, pressure, and wind speed through this week.",
            "This forecast shows a decrease in temperatures, pressure, and wind speeds."]},
    "steady": {
        "temperature": ["I am noticing very little change in temperatures.",
                        "This forecast shows temperatures that are fairly stagnant.",
                        "There is very little change in temperatures in my predicted forecast."],
        "winds": ["I see little to no change in wind speeds on the forecast.",
                  "The forecast is showing little to no change in winds.",
                  "I am not detecting a significant change in wind speeds."],
        "wind": ["I see little to no change in wind speeds on the forecast.",
                  "The forecast is showing little to no change in winds.",
                  "I am not detecting a significant change in wind speeds."],
        "pressure": ["The barometric pressure is shown as stagnant on this forecast.",
                     "I don't see much change in the atmospheric pressure.",
                     "This forecast is showing very little change in barometric pressure."],
        "three": ["The weather seems pretty stagnant throughout the week. Nothing to really note.",
                  "I am not noticing any major trends in pressure, temperature, or winds.",
                  "A pretty calm week. Nothing really to note."]
    },
    "continuations": ["  Also, ",
                      "  And, ",
                      "  I also have something else to note,  ",
                      "  On top of that, ",
                      "     ",
                      "     ",
                      "     ",
                      "  Furthermore,   ",
                      "  I also wanted to mention,      "],
    "endings": ["  And to finalize my forecast summary,      ",
                "  And lastly,     ",
                "  To finish my forecast,      ",
                "  And for my last report,     ",
                "   ",
                "    "]
}


def dailyBreakdown(day, week, last=False):
    dayString = ""
    if last:
        dayString += commandprocessor.selectandspeak(phrases['endings'])

    introduction = commandprocessor.selectandspeak([
        f"The average temperatures are around {day['temps']['day']}°.",
        f"expect an average temperature of {day['temps']['day']}°.",
        f"my forecast shows temperatures around {day['temps']['day']}°.",
        f"temperatures will be reaching around {day['temps']['day']}°.",
        f"the average temperature is forecasted at {day['temps']['day']}°.",
        f"I expect temperatures around {day['temps']['day']}°."])
    dayString += introduction

    if day['detail']['main'] == "Rain" or day['detail']['main'] == "Drizzle" or day['detail']['main'] == "Thunderstorm":
        dayString += commandprocessor.selectandspeak([
            "I am seeing a fairly noticeable chance of rain forecasted.",
            "There is a possibility of rain.",
            "Addtionally; There looks to be a chance of rain expected.",
            "Expect it to be fairly rainy."
        ])
    elif day['detail']['main'] == "Clear":
        dayString += commandprocessor.selectandspeak([
            "Seems like there will be clear skies all day.",
            "My forecast predicts clear skies all day.",
            "I anticipate clear skies, maybe a stray cloud or two.",
            "No rain, or clouds expected that day, just clear skies.",
            f"There's really nothing but clear skies forecasted."])
    elif day['detail']['main'] == "Clouds":
        dayString += commandprocessor.selectandspeak([
            "There will be a decent amount of clouds. Nothing but clouds really.",
            f"It will be fairly cloudy {day['day']} all day.",
            "I really only see clouds in the forecast. Nothing else much to note.",
            "Expect clouds all day. I don't really see any rain forecasted, but check back with me. You never know."])
    elif day['detail']['main'] == "Snow":
        dayString += commandprocessor.selectandspeak([
            f"I see some snow in the forecast for {day['day']}. Prepare your snow shovels.",
            "There is a possibility of some snow or ice on this day. Seems like a fairly decent chance.",
            f"I am forecasting snow or ice for {day['day']}. Don't forget to salt sidewalks or stairs.",
            "You should anticipate a chance of snow or ice. It seems fairly significant."])
    else:
        dayString += "Nothing really to note. Pretty boring day. Alright moving on."

    returnValue = {
         day['day']: dayString,
    }
    return returnValue


def checkConditions(week):
    result = {}
    conditions = []
    clear = 0
    rain = 0
    snow = 0
    cloudy = 0
    for day in week:
        day = day['detail']
        conditions.insert(len(conditions), day['main'])
    for condition in conditions:
        if condition == "Clear":
            clear += 1
        elif condition == "Clouds":
            cloudy += 1
        elif condition == "Rain" or condition == "Drizzle" or condition == "Thunderstorm":
            rain += 1
        elif condition == "Snow":
            snow += 1
    print(f"\nCloudy: {cloudy}" +
          f"\nRain: {rain}" +
          f"\nClear: {clear}" +
          f"\nSnow: {snow}")

    if 3 <= clear > 1:
        result['clear'] = "moderate"
    if clear > 3:
        result['clear'] = "high"
    if 3 <= rain > 1:
        result['rain'] = "moderate"
    if rain > 3:
        result['rain'] = "high"
    if 3 <= snow > 1:
        result['snow'] = "moderate"
    if snow > 3:
        result['snow'] = "high"
    if snow == 1:
        result['snow'] = "chance"
    if 3 <= cloudy > 1:
        result['clouds'] = "moderate"
    if cloudy > 3:
        result['clouds'] = "high"

    print("\nPulled from condition check:      " + str(result))
    return result


def checkPressure(week):
    result = ""
    val = 0
    pressures = []
    for day in week:
        day = day['detail']
        pressures.insert(len(pressures), day['pressure'])
        val += day['pressure']

    val = round(val / 7)
    compare = round(week[0]['detail']['pressure'])

    if (val - 1 > compare) or (val + 1 > compare):
        result = "rising"
    elif (val - 1 < compare) or (val + 1 < compare):
        result = "lowering"
    else:
        result = "steady"

    print("\nPulled from pressure check:      " + result)
    return result


def checkWinds(week):
    result = ""
    val = 0
    windSpeeds = []
    for day in week:
        day = day['winds']
        windSpeeds.insert(len(windSpeeds), day['speed'])
        val += day['speed']

    val = round(val / 7)
    compare = round(week[0]['winds']['speed'])

    if (val - 1 > compare) or (val + 1 > compare):
        result = "rising"
    elif (val - 1 < compare) or (val + 1 < compare):
        result = "lowering"
    else:
        result = "steady"

    print("\nPulled from wind check:      " + result)
    return result


def initTrendFind(week):
    result = ""
    val = 0
    lows = []
    compare = False

    for day in week:
        day = day['temps']
        if 'low' in day:
            lows.insert(len(lows), day['low'])
            val += day['low']
        elif 'day' in day:
            lows.insert(len(lows), day['day'])
            val += day['day']
            compare = round(week[0]['temps']['day'])

    val = round(val / 7)

    if not compare:
        compare = round(week[0]['temps']['low'])

    if (val + 2 > compare) or (val - 2 > compare) or (val - 1 > compare) or (val + 1 > compare):
        result = "rising"
    elif (val + 2 < compare) or (val - 2 < compare) or (val - 1 < compare) or (val + 1 < compare):
        result = "lowering"
    else:
        result = "steady"

    print("\n\n\n\n\nInitiating Trend Search\nPulled from temperature check:      " + result)

    results = {'temptrend': {'cond': result, 'type': "temperature"},
               'windtrend': {'cond': checkWinds(week), 'type': "wind"},
               'pressuretrend': {'cond': checkPressure(week), 'type': "pressure"},
               'conditions': checkConditions(week)}

    return results


def dataConvert(weeks, type=False):
    newWeek = []
    high = 0
    low = 0
    wind = 0
    if type == "basic":
        for day in weeks:
            correctDay = day[1]
            literalDay = commandprocessor.getDay(day[0])
            val = {
                'day': literalDay,
                'detail': {
                    'pressure': round(int(correctDay['pressure'])),
                    'humidity': round(int(correctDay['humidity'])),
                    'main': correctDay['weather'][0]["main"],
                    'dewpoint': round(int(correctDay['dew_point'])),
                    'uvi': round(int(correctDay['uvi']))},
                'temps': {
                    "day": round(int(correctDay["temp"]["day"])),
                    "feelslike": round(int(correctDay["feels_like"]["day"]))},
                'winds': {
                    'speed': round(int(correctDay["wind_speed"]))}}

            low += val['temps']['day']
            high += val['temps']['feelslike']
            wind += val['winds']['speed']

            newWeek.insert(len(newWeek), val)

        dayTemp = round(low / 7)
        feelTemp = round(high / 7)
        wind = round(wind / 7)

        return newWeek, [dayTemp, feelTemp, wind]
    else:
        for day in weeks:
            val = {
                'detail':
                    {'pressure': day[1],
                     'main': day[2]},
                'temps':
                    {'low': day[3],
                     "high": day[4]},
                'winds':
                    {'speed': day[5]}
            }
            low += round(int(day[3]))
            high += round(int(day[4]))
            wind += round(int(day[5]))
            newWeek.insert(len(newWeek), val)

        averageHigh = round(high / 7)
        averageLow = round(low / 7)
        averageWind = round(wind / 7)

        return newWeek, [averageHigh, averageLow, averageWind]


def defineResults(results, type):
    takeaway = []
    steady = []
    lowering = []
    rising = []
    beginningnotes = ""

    for result in results['conditions']:
        if 'rain' in result:
            takeaway.insert(0, f"{results['conditions']['rain']} rain")
        if 'clear' in result:
            takeaway.insert(0, f"{results['conditions']['clear']} clear")
        if 'clouds' in result:
            takeaway.insert(0, f"{results['conditions']['clouds']} clouds")
        if 'snow' in result:
            takeaway.insert(0, f"{results['conditions']['snow']} snow")
        for extra in result:
            if extra == "high":
                beginningnotes += (((str(result)).replace(" ", "")) + " ")
            if extra == "chance":
                beginningnotes += (((str(result)).replace(" ", "")) + " ")

    if results['temptrend']['cond'] == "steady":
        steady.insert(0, results['temptrend']['type'])
    elif results['temptrend']['cond'] == "rising":
        rising.insert(0, results['temptrend']['type'])
    elif results['temptrend']['cond'] == "lowering":
        lowering.insert(0, results['temptrend']['type'])

    if results['windtrend']['cond'] == "steady":
        steady.insert(0, results['windtrend']['type'])
    elif results['windtrend']['cond'] == "rising":
        rising.insert(0, results['windtrend']['type'])
        beginningnotes += "heavywinds "
    elif results['windtrend']['cond'] == "lowering":
        lowering.insert(0, results['windtrend']['type'])

    if results['pressuretrend']['cond'] == "steady":
        steady.insert(0, results['pressuretrend']['type'])
    elif results['pressuretrend']['cond'] == "rising":
        rising.insert(0, results['pressuretrend']['type'])
    elif results['pressuretrend']['cond'] == "lowering":
        lowering.insert(0, results['pressuretrend']['type'])

    if len(beginningnotes) > 0:
        if len(steady) >= 2:
            beginningnotes += "steady "
        elif len(rising) >= 2:
            beginningnotes += "rising "
        elif len(lowering) >= 2:
            beginningnotes += "lowering "
    if len(beginningnotes) > 0:
        beginningnotes = "boring"

    print(takeaway, rising, lowering, steady, beginningnotes)
    return takeaway, rising, lowering, steady, beginningnotes


def addto(phrase, count, maxi):
    if count <= 2:
        endingAdded = False
    if count > 1 and not count >= maxi:
        phrase += commandprocessor.selectandspeak(phrases["continuations"])
    elif count >= maxi and not endingAdded:
        phrase += commandprocessor.selectandspeak(phrases["endings"])
        endingAdded = True
    return phrase


def parse(parseType, data, secondary, weeklyData=False, newWeeklyData=False):
    print("attempting")
    main, rising, lowering, steady, important = defineResults(data, parseType)
    maxi = len(main) + len(rising) + len(lowering) + len(steady)
    count = 0
    parsePhrase = ""
    notes = {
        "high": {
            "rain": ["This week is a rainy one.",
                     "I am really only forecasting rain this week.",
                     "I see a lot of rain in the next coming days."],
            "clouds": ["Seems like this week will be cloudy one.",
                       "This week will be mostly cloudy.",
                       "I am forecasting a rife of cloudy days."],
            "snow": ["Seems like it's probably pretty cold with all the snow and ice on the forecast.",
                     "I see a lot of snow and ice heading our way.",
                     "Nothing but snow and ice this week."],
            "clear": ["A lot of clear skies this week.",
                      "Seems like nothing but clear skies for the week.",
                      "No clouds in sight this week."]},
        "chance": ["I see a chance of snow or ice in the forecast for this week.",
                   "I am forecasting a chance of snow or ice this week. Get ready!",
                   "There is a chance of snow or ice on the forecast, how exciting."],
        "rising": ["I'm seeing a lot of rising values this week. Maybe a warm front is entering our area.",
                   "Seems like there's some high pressure system coming towards us, a lot of rising values.",
                   "I notice that there is some warming temperatures coming in this week."],
        "lowering": [
            "Seems like temperatures are dropping this week. A low pressure system is more than likely approaching.",
            "Seems like colder weather is coming this week.",
            "I believe there is a low pressure system entering the area."],
        "steady": ["Seems like a typical week.",
                   "Nothing really to note this week.",
                   "I am forecasting a calm week this week."],
        "boring": ["Seems like a pretty stagnant week.",
                   "Nothing out of the normal this week.",
                   "I am forecasting basic conditions."],
        "wind": [f"Seems like it's going to be a windy week with an average wind speed of {secondary[2]}.",
                 f"I am forecasting a fairly windy week with an average speed of {secondary[2]}.",
                 f"There will be fairly high winds with an average of {secondary[2]}."]
    }
    usedPhrases = []
    extraNotes = {}

    if parseType == "simple":
        for condition in main:
            if not (condition in usedPhrases or not (condition in phrases)):
                count += 1
                usedPhrases.insert(0, condition)
                parsePhrase = addto(parsePhrase, count, maxi)
                parsePhrase += commandprocessor.selectandspeak(phrases[condition])

        if 3 < len(rising) > 1:
            if "temperature" in rising and "pressure" in rising:
                count += 1
                parsePhrase = addto(parsePhrase, count, maxi)
                parsePhrase += commandprocessor.selectandspeak(phrases["rising"]["two"]["temperature/pressure"])
            if "wind" in rising and "pressure" in rising:
                count += 1
                parsePhrase = addto(parsePhrase, count, maxi)
                parsePhrase += commandprocessor.selectandspeak(phrases["rising"]["two"]["pressure/wind"])
            else:
                count += 1
                parsePhrase = addto(parsePhrase, count, maxi)
                parsePhrase += commandprocessor.selectandspeak(phrases["rising"]['one'][rising[0]])
                count += 1
                parsePhrase = addto(parsePhrase, count, maxi)
                parsePhrase += commandprocessor.selectandspeak(phrases["rising"]['one'][rising[1]])
        elif 2 < len(rising) > 0:
            count += 1
            parsePhrase = addto(parsePhrase, count, maxi)
            parsePhrase += commandprocessor.selectandspeak(phrases["rising"]['one'][rising[0]])
        elif len(rising) == 3:
            count += 1
            parsePhrase += addto(parsePhrase, count, maxi)
            parsePhrase += commandprocessor.selectandspeak(phrases["rising"]["three"])

        if 3 < len(lowering) > 1:
            if "temperature" in lowering and "pressure" in lowering:
                count += 1
                parsePhrase += addto(parsePhrase, count, maxi)
                parsePhrase += commandprocessor.selectandspeak(phrases["lowering"]["two"]["temperature/pressure"])
            if "wind" in lowering and "pressure" in lowering:
                count += 1
                parsePhrase += addto(parsePhrase, count, maxi)
                parsePhrase += commandprocessor.selectandspeak(phrases["lowering"]["two"]["wind/temperature"])
            else:
                count += 1
                parsePhrase += addto(parsePhrase, count, maxi)
                parsePhrase += commandprocessor.selectandspeak(phrases["lowering"]['one'][lowering[0]])
                count += 1
                parsePhrase += addto(parsePhrase, count, maxi)
                parsePhrase += commandprocessor.selectandspeak(phrases["lowering"]['one'][lowering[1]])
        elif 2 < len(lowering) > 0:
            count += 1
            parsePhrase += addto(parsePhrase, count, maxi)
            parsePhrase += commandprocessor.selectandspeak(phrases["lowering"]['one'][lowering[0]])
        elif len(lowering) == 3:
            count += 1
            parsePhrase += addto(parsePhrase, count, maxi)
            parsePhrase += commandprocessor.selectandspeak(phrases["lowering"]["three"])

        if 3 < len(steady) > 1:
            count += 1
            parsePhrase += addto(parsePhrase, count, maxi)
            parsePhrase += commandprocessor.selectandspeak(phrases["steady"]['one'][steady[0]])
            count += 1
            parsePhrase += addto(parsePhrase, count, maxi)
            parsePhrase += commandprocessor.selectandspeak(phrases["steady"]['one'][steady[1]])
        elif 2 < len(steady) > 0:
            count += 1
            parsePhrase += addto(parsePhrase, count, maxi)
            parsePhrase += commandprocessor.selectandspeak(phrases["steady"]['one'][lowering[0]])
        elif len(steady) == 3:
            count += 1
            parsePhrase += addto(parsePhrase, count, maxi)
            parsePhrase += commandprocessor.selectandspeak(phrases["steady"]["three"])

        secondarysentence = [
            f"For this week, I am forecasting an average high of {round(secondary[0])}° and a low of {round(secondary[1])}°.",
            f"I am forecasting a general high of {round(secondary[0])}° and a low of {round(secondary[1])}°.",
            f"Daily temperatures will be around {round(secondary[1])}° to {round(secondary[0])}°.",
            f"I've calculated an average high of {round(secondary[0])}° and a low of {round(secondary[1])}°.",
            f"Seems like temperatures will stick between {round(secondary[0])}° and {round(secondary[1])}°.",
            f"{round(secondary[0])}° is the average high this week with {round(secondary[1])}° being the average low."]

        addition = ""
        context = "fair"
        additionAdded = False
        important = important.split(" ")
        print(important)
        if "highrain" in important:
            context = "poor"
            addition += commandprocessor.selectandspeak(notes["high"]["rain"])
        elif "highclouds" in important:
            context = "fair"
            addition += commandprocessor.selectandspeak(notes["high"]["clouds"])
        elif "highsnow" in important:
            context = "poor"
            addition += commandprocessor.selectandspeak(notes["high"]["snow"])
        elif "highclear" in important:
            context = "good"
            addition += commandprocessor.selectandspeak(notes["high"]["clear"])
        if "chancesnow" in important:
            context = "fair"
            addition += commandprocessor.selectandspeak(notes["chance"])
        if "rising" in important:
            addition += commandprocessor.selectandspeak(notes["rising"])
        if "steady" in important:
            addition += commandprocessor.selectandspeak(notes["steady"])
        if "lowering" in important:
            addition += commandprocessor.selectandspeak(notes["lowering"])
        if "boring" in important:
            context = "fair"
            addition += commandprocessor.selectandspeak(notes["boring"])
        if "heavywinds" in important:
            context = "windy"
            addition += commandprocessor.selectandspeak(notes["wind"])

        if not additionAdded:
            addition += commandprocessor.selectandspeak(secondarysentence)
            additionAdded = True

        parsePhrase = addition + '    ' + parsePhrase

        universal.contextulizer(["askedweathertrend", context])

        return parsePhrase
    elif parseType == "basic":

        temps = []
        humidity = []
        pressure = []
        winds = []
        dewpoint = []
        uvi = []

        for day in newWeeklyData:
            temps.insert(0, day['temps']['day'])
            humidity.insert(0, day['detail']['humidity'])
            pressure.insert(0, day['detail']['pressure'])
            dewpoint.insert(0, day['detail']['dewpoint'])
            uvi.insert(0, day['detail']['uvi'])
            winds.insert(0, day['winds']['speed'])

            print(day['temps']['day'], day['detail']['humidity'], day['detail']['pressure'], day['detail']['dewpoint'], day['detail']['uvi'], day['winds']['speed'])

        maxs = {
            'temp': max(temps),
            'wind': max(winds),
            'pressure': max(pressure),
            'dewpoint': max(dewpoint),
            'uvi': max(uvi),
            'humidity': max(humidity)}
        mins = {
            'temp': min(temps),
            'wind': min(winds),
            'pressure': min(pressure),
            'dewpoint': min(dewpoint),
            'uvi': min(uvi),
            'humidity': min(humidity)}

        weeklyTakeaway = {}

        for day in newWeeklyData:
            compareValues = {
                'temp': day['temps']['day'],
                'wind': day['winds']['speed'],
                'pressure': day['detail']['pressure'],
                'dewpoint': day['detail']['dewpoint'],
                'uvi': day['detail']['uvi'],
                "humidity": day['detail']['humidity']}

            daytakeaway = []

            if 'temp' in maxs and compareValues['temp'] == maxs['temp']:
                daytakeaway.insert(0, commandprocessor.selectandspeak([
                    f"{day['day']} is the hottest day this week.",
                    f"{day['day']} marks the point of the hottest temperatures of the week.",
                    f"The warmest part of the week is around {day['day']}."]))
                maxs.pop('temp')
            if 'humidity' in maxs and compareValues['humidity'] == maxs['humidity']:
                if len(daytakeaway) > 0:
                    daytakeaway.insert(len(daytakeaway), commandprocessor.selectandspeak([
                        f"This day also shows the highest humidity levels, reporting at {day['detail']['humidity']}%.",
                        f"{day['day']} also holds the weekly high for humidity levels. Expect a humidity level of {day['detail']['humidity']}%.",
                        f"I am additionally noticed some the highest humidity readings of the week, reaching up to {day['detail']['humidity']}%."]))
                else:
                    daytakeaway.insert(0, commandprocessor.selectandspeak([
                        f"My forecast for {day['day']} shows the highest humidity levels of the week, reporting at {day['detail']['humidity']}%.",
                        f"{day['day']} holds the weekly high for humidity levels. Expect a humidity level of {day['detail']['humidity']}%.",
                        f"For {day['day']}, I am seeing some rather high humidity readings, reaching up to {day['detail']['humidity']}%."]))
                maxs.pop('humidity')
            if 'wind' in maxs and compareValues['wind'] == maxs['wind']:
                if len(daytakeaway) > 0:
                    daytakeaway.insert(len(daytakeaway), commandprocessor.selectandspeak([
                        f"Additionally; Wind speeds will be at their highest,  reaching speeds of {day['winds']['speed']} miles per hour.",
                        f"Furthermore, I am anticipating fairly high wind speeds, possibly reaching upwards of {day['winds']['speed']} miles per hour.",
                        f"The forecast also shows wind speeds around {day['winds']['speed']} miles per hour. That's the highest of the week."]))
                else:
                    daytakeaway.insert(0, commandprocessor.selectandspeak([
                        f"Wind speeds will be the highest on {day['day']}, reaching {day['winds']['speed']} miles per hour.",
                        f"On {day['day']}, I am anticipating fairly high wind speeds, possibly reaching upwards of {day['winds']['speed']} miles per hour.",
                        f"For {day['day']}, the forecast shows winds around {day['winds']['speed']} miles per hour. That's the highest of the week."]))

                maxs.pop('wind')
            if 'pressure' in maxs and compareValues['pressure'] == maxs['pressure']:
                if len(daytakeaway) > 0:
                    daytakeaway.insert(len(daytakeaway), commandprocessor.selectandspeak([
                        f"Another note; The barometric pressure will be at it's highest of the week at {compareValues['pressure']} hectopascals",
                        f"Additionally; The atmospheric pressure is at it's highest point, reading {compareValues['pressure']} hectopascals.",
                        f"I also see the barometric pressure at it's highest point of the week. I'm seeing values around {compareValues['pressure']} hectopascals."]))
                else:
                    daytakeaway.insert(0, commandprocessor.selectandspeak([
                        f"The barometric pressure is at it's highest on {day['day']} with readings around {compareValues['pressure']} hectopascals.",
                        f"Barometric pressure seems to rise to it's highest point on {day['day']}, with a pressure of {compareValues['pressure']} hectopascals.",
                        f"{day['day']} is crown champion of highest barometric reading of the week, forecasted at {compareValues['pressure']} hectopascals."]))
                maxs.pop('pressure')
            if 'dewpoint' in maxs and compareValues['dewpoint'] == maxs['dewpoint']:
                if len(daytakeaway) > 0:
                    daytakeaway.insert(len(daytakeaway), commandprocessor.selectandspeak([
                        f"Also, this day marks the highest dew point of the week.",
                        f"My forecast also shows the highest dew point of the week.",
                        f"Another thing to note, the dew point is at it's highest all week."]))
                else:
                    daytakeaway.insert(0, commandprocessor.selectandspeak([
                        f"I am noticing the highest dew point on {day['day']}.",
                        f"{day['day']} has the highest dew point of the week.",
                        f"{day['day']} shows the weekly high dew point at {day['detail']['dewpoint']}."]))
                maxs.pop('dewpoint')
            if 'uvi' in maxs and compareValues['uvi'] == maxs['uvi']:
                if len(daytakeaway) > 0:
                    daytakeaway.insert(len(daytakeaway), commandprocessor.selectandspeak([
                        f"You should also prepare for fairly high UVI readings, some reaching {day['detail']['uvi']}.",
                        f"It may be the brightest day this week, with a UVI reading of {day['detail']['uvi']}.",
                        f"UV rays are at weekly high of {day['detail']['uvi']}."]))
                else:
                    daytakeaway.insert(0, commandprocessor.selectandspeak([
                        f"The Sun is shining the brightest {day['day']}, with UVI readings reaching {day['detail']['uvi']}.",
                        f"Seems like the Sun will be shining pretty brightly {day['day']}, reaching a UVI reading of {day['detail']['uvi']}.",
                        f"UV rays are at weekly high {day['day']}. UVI is expected to be {day['detail']['uvi']}."]))
                maxs.pop('uvi')
            if 'temp' in mins and compareValues['temp'] == mins['temp']:
                if len(daytakeaway) > 0:
                    daytakeaway.insert(len(daytakeaway), commandprocessor.selectandspeak([
                        f"It should also be the coolest part of the week.",
                        f"Temperatures are at their lowest at this part of the week.",
                        f"There is a noticeable decrease in temperatures at this point in the forecast."]))
                else:
                    daytakeaway.insert(0, commandprocessor.selectandspeak([
                        f"{day['day']} will be the coolest day all week. .",
                        f"{day['day']} holds the spot for coolest day of the week.",
                        f"For {day['day']}, I am calculating the lowest temperatures of the week."]))
                mins.pop('temp')
            if 'humidity' in mins and compareValues['humidity'] == mins['humidity']:
                if len(daytakeaway) > 0:
                    daytakeaway.insert(len(daytakeaway), commandprocessor.selectandspeak([
                        f"I am also noticing the lowest humidity level reading of the week, at just {day['detail']['humidity']}%.",
                        f"Humidity will also be at it's lowest of the week, plummeting to {day['detail']['humidity']}%.",
                        f"The humidity reading for today is {day['detail']['humidity']}%, the lowest of the week."]))
                else:
                    daytakeaway.insert(0, commandprocessor.selectandspeak([
                        f"{day['day']} has the lowest humidity level, reading at only {day['detail']['humidity']}%.",
                        f"Expect humidity to decrease on {day['day']}, reaching a weekly low of {day['detail']['humidity']}%.",
                        f"I noticed some rather low humidity readings on {day['day']}, the lowest of the week actually."]))
                mins.pop('humidity')
            if 'wind' in mins and compareValues['wind'] == mins['wind']:
                if len(daytakeaway) > 0:
                    daytakeaway.insert(len(daytakeaway), commandprocessor.selectandspeak([
                        f"Wind speeds will be at their lowest, with speeds of {day['winds']['speed']} miles per hour.",
                        f"I also noticed a decrease in wind speeds, declining to {day['winds']['speed']} miles per hour, the lowest of the week.",
                        f"The forecast also shows wind speeds around {day['winds']['speed']} miles per hour. That's the lowest of the week."]))
                else:
                    daytakeaway.insert(0, commandprocessor.selectandspeak([
                        f"Seems like {day['day']} holds the spot for the lowest wind speeds, with an average speed of {day['winds']['speed']} miles per hour.",
                        f"{day['day']} seems to be the day with the lowest wind speeds, with the forecast showing speeds around {day['winds']['speed']} miles per hour.",
                        f"On {day['day']}, this area will be experiencing  the lowest wind speeds of the week, with an average of {day['winds']['speed']} miles per hour."]))
                mins.pop('wind')
            if 'pressure' in mins and compareValues['pressure'] == mins['pressure']:
                if len(daytakeaway) > 0:
                    daytakeaway.insert(len(daytakeaway), commandprocessor.selectandspeak([
                        f"Barometric pressure also seems to be dropping. It will be at it's lowest pressure of {compareValues['pressure']} hectopascals.",
                        f"The forecast also shows the the lowest barometric pressure of {compareValues['pressure']} hectopascals.",
                        f"I also see the barometric pressure at it's lowest point of the week. I'm seeing values around {compareValues['pressure']} hectopascals."]))
                else:
                    daytakeaway.insert(0, commandprocessor.selectandspeak([
                        f"{day['day']} has the lowest barometric reading of the week, hitting only {compareValues['pressure']} hectopascals.",
                        f"Prepare for the lowest atmospheric pressure on {day['day']}, with readings only reaching {compareValues['pressure']} hectopascals.",
                        f"{day['day']} is crown champion of the lowest barometric reading, forecasted at {compareValues['pressure']} hectopascals."]))
                mins.pop('pressure')
            if 'dewpoint' in mins and compareValues['dewpoint'] == mins['dewpoint']:
                if len(daytakeaway) > 0:
                    daytakeaway.insert(len(daytakeaway), commandprocessor.selectandspeak([
                        f"Also, expect the lowest dew point of the week.",
                        f"My forecast also shows the lowest dew point of the week.",
                        f"Another thing to note, the dew point is at it's lowest all week."]))
                else:
                    daytakeaway.insert(0, commandprocessor.selectandspeak([
                        f"I am noticing the lowest dew point on {day['day']}.",
                        f"{day['day']} has the lowest dew point of the week.",
                        f"{day['day']} shows the weekly low dew point at {day['detail']['dewpoint']}."]))
                mins.pop('dewpoint')
            if 'uvi' in mins and compareValues['uvi'] == mins['uvi']:
                if len(daytakeaway) > 0:
                    daytakeaway.insert(len(daytakeaway), commandprocessor.selectandspeak([
                        f"Expect low UV readings, some barely reaching {day['detail']['uvi']}.",
                        f"Seems like I'm finding the lowest UV readings in the forecast. Expect around a {day['detail']['uvi']}.",
                        f"Also, UV rays are at weekly low of {day['detail']['uvi']}."]))
                else:
                    daytakeaway.insert(0, commandprocessor.selectandspeak([
                        f"{day['day']}  seems to have the lowest UVI readings of the week, reading in at only {day['detail']['uvi']}.",
                        f"Seems like the Sun is probably hiding on {day['day']}, with the week's lowest UVI reading of {day['detail']['uvi']}.",
                        f"For {day['day']}, the UVI readings will be the lowest this week, reading in at only {day['detail']['uvi']}."]))
                mins.pop('uvi')

            for data in weeklyData:
                if str(day['day']) in data:
                    daytakeaway.insert(len(daytakeaway), weeklyData[weeklyData.index(data)][str(day['day'])])

            weeklyTakeaway[day['day']] = "  ".join(daytakeaway)

        beginForecastPhrase = ""
        context = "fair"

        if "highrain" in important:
            context = "poor"
            beginForecastPhrase += commandprocessor.selectandspeak([
                "This week seems like a fairly rainy one. I am forecasting rain almost every day.",
                "I am forecasting  a large amount of rain in the area this week. Almost every day actually.",
                "Seems like it's going to rain a lot this week."])
        elif "highclouds" in important:
            context = "fair"
            beginForecastPhrase += commandprocessor.selectandspeak([
                "I am forecasting nothing but clouds. Maybe a little bit of rain, but mostly clouds.",
                "I am really only seeing clouds on my forecast. A bit boring, but I am sure there's more at work.",
                "The forecast predicts a fairly cloudy week ahead of us."])
        elif "highsnow" in important:
            context = "poor"
            beginForecastPhrase += commandprocessor.selectandspeak([
                "A whole lot of snow and ice this week. Get ready for it.",
                "The forecast is showing me nothing but snow and ice this week.",
                "Get ready for an ice storm, or something of the sorts. Seem like it's going to snow or ice every day."])
        elif "highclear" in important:
            context = "good"
            beginForecastPhrase += commandprocessor.selectandspeak([
                "Nothing but clear skies this week.",
                "Whole lot of clear skies in the weekly forecast. No clouds in sight.",
                "Seems like it's really just clear skies this week.",
                "I am forecasting a predominance of clear skies this week."])
        if "chancesnow" in important:
            context = "fair"
            beginForecastPhrase += commandprocessor.selectandspeak([
                "Seems like there's a possibility of snow this week.",
                "I see a small chance of snow or ice in the forecast.",
                "Looks like there's a chance we may get snow or ice this week, nothing major though.",
                "I am forecasting a small chance of ice or snow this week."])
        if "boring" in important:
            context = "fair"
            beginForecastPhrase += commandprocessor.selectandspeak(notes["boring"])
        if "heavywinds" in important:
            context = "windy"
            beginForecastPhrase += commandprocessor.selectandspeak(notes["wind"])

        if len(rising) == 2:
            if "temperature" in rising and "pressure" in rising:
                beginForecastPhrase += commandprocessor.selectandspeak(phrases["rising"]["two"]["temperature/pressure"])
            if "wind" in rising and "pressure" in rising:
                beginForecastPhrase += commandprocessor.selectandspeak(phrases["rising"]["two"]["pressure/wind"])
            else:
                beginForecastPhrase += commandprocessor.selectandspeak(phrases["rising"]['one'][rising[0]])
                beginForecastPhrase += commandprocessor.selectandspeak(phrases["rising"]['one'][rising[1]])
        elif len(rising) == 1:
            beginForecastPhrase += commandprocessor.selectandspeak(phrases["rising"]['one'][rising[0]])
        elif len(rising) == 3:
            beginForecastPhrase += commandprocessor.selectandspeak(phrases["rising"]["three"])

        if len(lowering) == 2:
            if "temperature" in lowering and "pressure" in lowering:
                beginForecastPhrase += commandprocessor.selectandspeak(phrases["lowering"]["two"]["temperature/pressure"])
            if "wind" in lowering and "pressure" in lowering:
                beginForecastPhrase += commandprocessor.selectandspeak(phrases["lowering"]["two"]["wind/temperature"])
            else:
                beginForecastPhrase += commandprocessor.selectandspeak(phrases["lowering"]['one'][lowering[0]])
                beginForecastPhrase += commandprocessor.selectandspeak(phrases["lowering"]['one'][lowering[1]])
        elif len(lowering) == 1:
            beginForecastPhrase += commandprocessor.selectandspeak(phrases["lowering"]['one'][lowering[0]])
        elif len(lowering) == 3:
            beginForecastPhrase += commandprocessor.selectandspeak(phrases["lowering"]["three"])

        if len(steady) == 2:
            beginForecastPhrase += commandprocessor.selectandspeak(phrases["steady"]['one'][steady[0]])
            beginForecastPhrase += commandprocessor.selectandspeak(phrases["steady"]['one'][steady[1]])
        elif len(steady) == 1:
            beginForecastPhrase += commandprocessor.selectandspeak(phrases["steady"]['one'][lowering[0]])
        elif len(steady) == 3:
            beginForecastPhrase += commandprocessor.selectandspeak(phrases["steady"]["three"])

        finalTakeaway = ""
        for day in weeklyTakeaway:
            finalTakeaway += '<p>' + weeklyTakeaway[day] + '</p>'

        parsePhrase = "<amazon:domain name='news'> " + beginForecastPhrase + "</amazon:domain>  <break strength = 'x-strong'/>" + finalTakeaway +  f'<amazon:domain name="news"> Looks like this forecast is predicting a week of {context} weather conditions. </amazon:domain>'

        if context:
            universal.contextulizer(["askedweathertrend", context])
            return parsePhrase
        else:
            return Exception("No context for contextualizer")


def trendFind(todaysData=False, todaysSecondData=False, weeklyData=False, parseType="simple"):
    try:
        if weeklyData:
            newWeeklyData, secondary = dataConvert(weeklyData, parseType)
            results = initTrendFind(newWeeklyData)
            if parseType == "basic":
                weeklyData = []
                for day in newWeeklyData:
                    weeklyData.insert(len(weeklyData), dailyBreakdown(day, newWeeklyData))
                parseResult = parse(parseType, results, secondary, weeklyData, newWeeklyData)
            else:
                parseResult = parse(parseType, results, secondary)

        fakeParse = parseResult.split("  ")
        fakeParse = "   \n  ".join(fakeParse)

        return parseResult

    except Exception as err:
        print("[ERRO] " + repr(err))
        print(repr(err.__context__))
        print(repr(err.__cause__))
        print(traceback.print_tb(err.__traceback__))
        return False
