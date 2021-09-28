import requests
import commandprocessor
import datetime
import universal

weeklyData = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/2205%20West%20Canton%20Pl?unitGroup=us&key=BHFCCKY362XGLDYMK3FRKYZHB&include=obs%2Cfcst%2Cstats%2Chistfcst"



def degreeTranslate(degree):
    if (degree>337.5): return 'N'
    if (degree>292.5): return 'NW'
    if(degree>247.5): return 'W'
    if(degree>202.5): return 'SW'
    if(degree>157.5): return 'S'
    if(degree>122.5): return 'SE'
    if(degree>67.5): return 'E'
    if(degree>22.5): return 'NE'
    return 'N'


def data7Process():
    weeklyDataJSON = requests.get(weeklyData).json()
    day1 = weeklyDataJSON['days'][1]
    day2 = weeklyDataJSON['days'][2]
    day3 = weeklyDataJSON['days'][3]
    day4 = weeklyDataJSON['days'][4]
    day5 = weeklyDataJSON['days'][5]
    day6 = weeklyDataJSON['days'][6]
    day7 = weeklyDataJSON['days'][7]
    week = [day1, day2, day3, day4, day5, day6, day7]
    for day in week:
        if type(day) is not list:
            dayName = commandprocessor.getDay(week.index(day))
            trueDegree = degreeTranslate(day['winddir'])
            returnDay = {
                "day": dayName,
                "daynum": week.index(day),
                "temps": {
                    "day": round(day['temp']),
                    "fl": round(day['feelslike'])},
                "details": {
                    "pressure": round(day['pressure']),
                    'humidity': round(day['humidity']),
                    'dp': round(day['dew']),
                    'uvi': round(day['uvindex']),
                    'clouds': day["cloudcover"],
                    'pop': day['precipprob'],
                    'snow': day['snow'],
                    'sv': day['severerisk'],
                    'poptype': day['preciptype'],
                    'windspeed': day['windspeed'],
                    'winddir': trueDegree},
                "forecast": {
                    "basic": day['conditions'],
                    "detail": day["description"],
                    "icon": day["icon"]}}

            week.append(returnDay)
            week.remove(day)

    return week


# noinspection PyUnboundLocalVariable
def phrase7Build(day):

    beginPhrase = ""                                                                                                    ## BEGIN PHRASE ASSIGNMENT
    if day["daynum"] == 0:
        beginPhrase = commandprocessor.selectandspeak(
            [f"For {day['day']}, expect temperatures ranging around {day['temps']['day']}° with a feels like of {day['temps']['fl']}°.",
             f"On {day['day']}, plan for temperatures around {day['temps']['day']}° and a feels like of {day['temps']['fl']}°.",
             f"To begin my forecast, on {day['day']} I am predicting temps around {day['temps']['day']}° and feels like temps around {day['temps']['fl']}°."])
    elif 0 < day["daynum"] < 7:
        if day["daynum"] == 1:
            dayPhrase = "Secondly"
        elif day["daynum"] == 2:
            dayPhrase = "Thirdly"
        elif day["daynum"] == 3:
            dayPhrase = "Fourthly"
        elif day["daynum"] == 4:
            dayPhrase = "Fifthly"
        elif day["daynum"] == 5:
            dayPhrase = "Sixthly"
        beginPhrase = commandprocessor.selectandspeak([
            f"<break time = '2s'/> In addition, on {day['day']}, anticipate temperatures to average at {day['temps']['day']}° and feels like temperatures around {day['temps']['fl']}°.",
            f"<break time = '2s'/> {dayPhrase}, for {day['day']}, plan on temperatures being around {day['temps']['day']}° with feels like temperatures at {day['temps']['fl']}°.",
            f"<break time = '2s'/> As for {day['day']}, expect temperatures to linger at {day['temps']['day']}° with feels like doing the same at {day['temps']['fl']}°.",
            f"<break time = '2s'/> On {day['day']}, I'm seeing temperatures at {day['temps']['day']}° and feels like temperatures at {day['temps']['fl']}°.",
            f"<break time = '2s'/> And as for {day['day']}, I am forecasting temperatures around {day['temps']['day']}° and feels like temperatures at {day['temps']['fl']}°."])
    elif day["daynum"] == 7:
        beginPhrase = commandprocessor.selectandspeak([
            f"<break time = '3s'/> And lastly, {day['day']}, expect temperatures to range around {day['temps']['day']}° with feels like doing the same at {day['temps']['fl']}°.",
            f"<break time = '3s'/> And as for {day['day']}, I forecast temperatures to be averaging {day['temps']['day']}° with feels like averaging {day['temps']['fl']}°.",
            f"<break time = '3s'/> And for our last day, On {day['day']}, I predict temperatures at {day['temps']['day']}° with feels like following at {day['temps']['fl']}°."])

    importantPhrase = ""
    if "ice" in day["important"]:
        importantPhrase += commandprocessor.selectandspeak([
            "<break time = '2s'/> Additionally, there will be a pretty high chance of ice. Drive safe",
            "<break time = '2s'/>I want to warn you of the ice danger. Please drive safe.",
            "<break time = '2s'/>There seems to be an ice danger. Please drive safe."])
    if "snow" in day["important"]:
        if day["important"]["snow"] == "expected" or day["important"]["snow"] == "probable":
            importantPhrase += commandprocessor.selectandspeak([
                "<break time = '2s'/> Enjoy the expected snow.",
                "<break time = '2s'/> Drive safe in the snow.",
                "<break time = '2s'/> I anticipate snow-men and snow-women in your future.",
                "<break time = '2s'/> I wonder how fast the snow will melt this time."])
        elif day["important"]["snow"] == "chance":
            importantPhrase += commandprocessor.selectandspeak([
                "<break time = '2s'/> There seems to be a chance of snow in the forecast.",
                "<break time = '2s'/> I see a small chance of snow in the forecast.",
                "<break time = '2s'/> I anticipate small snow-men and snow-women in your future.",
                "<break time = '2s'/> I see a small chance of snow. I wonder how fast the snow will melt this time."])
    if "severe" in day["important"]:
        if day["important"]["severe"] == "severe":
            importantPhrase += commandprocessor.selectandspeak([
                "There is a very high chance of severe weather forecasted.",
                "I am noticing a very high chance of severe weather.",
                "The forecast shows a very high chance of severe weather.",
            ])

def init7Forecast(forecastUpdate):
    procweek = data7Process()
    week = {
        "dt": datetime.datetime.now(),
        "weather": procweek}                                ## Convert to dict with weather = procweek and dt = now

    if forecastUpdate:                          ## Universal Variable Hour Weather Update
        if not universal.hourWeather:
            universal.hourWeather = week
        else:
            hourTime = universal.hourWeather['dt']
            if (hourTime + 3600) <= week['dt']:
                universal.hourWeather = week
        universal.currentWeather = week
    windDirections = []
    for day in procweek:
        if procweek[procweek.index(day)-1]:
            ref = procweek[procweek.index(day)-1]
            main = procweek[day]
            main['trend'] = {}
            main['important'] = {}
            main['notes'] = {}

            if (main['details']['pressure']-2) > ref['details']['pressure']:          # Pressure Trend Check
                main['trend']['pressure'] = "rising"
            elif (ref['details']['pressure']-2) > main['details']['pressure']:
                main['trend']['pressure'] = "lowering"
            if (main['details']['humidity']-10) > ref['details']['pressure']:          # Humidity Trend Check
                main['trend']['humidity'] = "rising"
            elif (ref['details']['humidity']-10) > main['details']['pressure']:
                main['trend']['humidity'] = "lowering"
            if main['details']['sv'] > 30:                                # Severe Weather Important Check
                main['important']['severe'] = "moderate"
            if main['details']['sv'] > 60:
                main['important']['severe'] = 'high'
            if main['details']['sv'] > 80:
                main['important']['severe'] = 'severe'
            if main['details']['uvi'] > 8:                               # High UV Index Important Check
                main['important']['uvi'] = 'high'

            windDirections.append(main['details']['winddir'])            # Wind direction and Front Notes Check
            n = 0
            s = 0
            w = 0
            e = 0
            for direction in windDirections:
                if direction == "N" or direction == "NW" or direction == "NE":
                    n+=1
                if direction == "S" or direction == "SE" or direction == "SW":
                    s+=1
                if direction == "E" or direction == "SE" or direction == "NE":
                    e+=1
                if direction == "W" or direction == "NW" or direction == "SW":
                    w+=1
            if len(windDirections) > 3 and "firstcheck" not in windDirections:
                if (w > 2 and n > 2) or (e > 2 and n > 2) or n > 3:
                    main["notes"]["fronts"] = "cold front"
                elif (w > 2 and s > 2) or (e > 2 and s > 2) or s > 3:
                    main["notes"]["fronts"] = "warm front"
                windDirections.append("firstcheck")
            elif len(windDirections) > 7:
                if (w > 5 and n > 5) or (e > 5 and n > 5) or n > 5:
                    main["notes"]["fronts"] = "cold front"
                elif (w > 5 and s > 5) or (e > 5 and s > 5) or s > 5:
                    main["notes"]["fronts"] = "warm front"
                else:
                    main["notes"]["fronts"] = "sporadic"

                                                                         # Snow and Ice Important Check

            if main["details"]["snow"] > 0 and type(main['details']['poptype']) is list and "snow" in main['details']['poptype']:
                main['important']['snow'] = "chance"
            if main["details"]["snow"] > 50 and type(main['details']['poptype']) is list and "snow" in main['details']['poptype']:
                main['important']['snow'] = "probable"
            if main["details"]["snow"] > 70 and type(main['details']['poptype']) is list and "snow" in main['details']['poptype']:
                main['important']['snow'] = "expected"

            if type(main['details']['poptype']) is list and ("freezingrain" in main['details']['poptype'] or "ice" in main['details']['poptype']):
                main['important']['ice'] = "expected"

        phrase = phrase7Build(procweek[day])



def forecast(forecastType="day", forecastUpdate=True):
    pass








