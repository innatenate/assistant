import math


def checkConditions(week):
    result = ""
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

    if 3 <= clear > 1:
        result['clear'] = "moderate"
    if clear < 3:
        result['clear'] = "high"
    if 3 <= rain > 1:
        result['rain'] = "moderate"
    if rain < 3:
        result['rain'] = "high"
    if 3 <= snow > 1:
        result['snow'] = "moderate"
    if snow < 3:
        result['snow'] = "high"
    if 2 < snow > 0:
        result['snow'] = "chance"
    if 3 <= cloudy > 1:
        result['clouds'] = "moderate"
    if cloudy < 3:
        result['clouds'] = "high"

    return result


def checkPressure(week):
    result = ""
    val = 0
    pressures = []
    for day in week:
        day = day['detail']
        pressures.insert(len(pressures), day['pressure'])
    num = 0
    for pressure in pressures:
        if num > 0:
            num = 0
            val -= pressure
        else:
            num = 1
            val += pressure

    val = round(val)
    compare = round(week[0]['pressure'])
    if (val - 1) > compare or (val + 1) > compare or (val + 2) > compare or (val + 2) > compare:
        result = "rising pressures"
    elif (val - 1) < compare or (val + 1) < compare or (val + 2) < compare or (val + 2) < compare:
        result = "lowering"
    else:
        result = "steady"

    return result


def checkWinds(week):
    result = ""
    val = 0
    windSpeeds = []
    for day in week:
        day = day['winds']
        windSpeeds.insert(len(windSpeeds), day['speed'])
    num = 0
    for wind in windSpeeds:
        if num > 0:
            num = 0
            val -= wind
        else:
            num = 1
            val += wind

    val = round(val)
    compare = round(week[0]['winds']['speed'])
    if (val - 1) > compare or (val + 1) > compare or (val + 2) > compare or (val + 2) > compare:
        result = "rising"
    elif (val - 1) < compare or (val + 1) < compare or (val + 2) < compare or (val + 2) < compare:
        result = "lowering"
    else:
        result = "steady"

    return result


def initTrendFind(week):
    result = ""
    val = 0
    lows = []
    for day in week:
        day = day['temps']
        lows.insert(len(lows), day['low'])
    num = 0
    for low in lows:
        if num > 0:
            num = 0
            val -= low
        else:
            num = 1
            val += low

    val = round(val)
    compare = round(week[0]['temps']['low'])
    if (val - 1) > compare or (val + 1) > compare or (val + 2) > compare or (val + 2) > compare:
        result = "rising temperatures"
    elif (val - 1) < compare or (val + 1) < compare or (val + 2) < compare or (val + 2) < compare:
        result = "lowering"
    else:
        result = "steady"
    results = {'temptrend': {'cond': result, 'type': "temperature"},
               'windtrend': {'cond': checkWinds(week), 'type': "temperature"},
               'pressuretrend': {'cond': checkPressure(week), 'type': "pressure"}, 'conditions': checkConditions(week)}

    return results


def dataConvert(weeks):
    newWeek = []
    for day in weeks:
        val = {
            'detail':
                {'pressure': day[1],
                 'desc': day[2]},
            'temps':
                {'low': day[3],
                 "high": day[4]},
            'winds':
                {'speed': day[5]}
        }

        newWeek.insert(len(newWeek), val)

    return newWeek


def defineResults(results, type):
    takeaway = []
    steady = []
    lowering = []
    rising = []
    if type == "simple":
        for result in results:
            if 'cond' in results:
                if "steady" in result['cond']:
                    steady.insert(0, result['type'])
                elif 'rising' in result['cond']:
                    steady.insert(0, result['type'])
                elif 'lowering' in result['cond']:
                    lowering.insert(0, result['type'])


def parse(parseType, data):
    returnParse = ""


def trendFind(todaysData=False, todaysSecondData=False, weeklyData=False, parseType="simple"):
    if weeklyData:
        weeklyData = dataConvert(weeklyData)
        results = initTrendFind(weeklyData)

    return
