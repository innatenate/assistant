import universal
import commandprocessor

plants = ['plant', 'plants', "plant's", "flower", "flowers", "garden", "flower's", "daisy", "shasta", "ph", "ec", "tds"]
question = ["what", "when", "how", "who", "where", "why", 'date']
weather = ["today", "tomorrow", "seven", "day", "rain", "high", "low", "cold", "hot", "sunny", "weather", "forecast",
           "today's", "todays", "outside", "barometric", "atmospheric", "atmosphere", "pressure"]


def Process(text, secondary=False, client=False):
    originaltext = text
    text = str.lower(text)
    text = text.split(" ")
    plantscore = 0
    questionscore = 0
    weatherscore = 0
    keywords = []

    if universal.waitingForQuery:
        if len(universal.currentQueries) > 0:
            for query in universal.currentQueries:
                if query['type'] == 'specific':
                    if commandprocessor.QueryQuestion(text, query['keywords']):
                        commandprocessor.ProcessQuery("".join(text), query)
                    else:
                        universal.speak("I don't think I heard you right. Let's try that again.", client)
                        universal.speak(universal.lastPhrase, client)
                        return False
                elif query['type'] == 'yesno':
                    if 'sure' in text or  'yes' in text or  'good' in text or 'great' in text or "please" in text or "thanks" in text:
                        commandprocessor.ProcessQuery(True, query)
                    else:
                        commandprocessor.ProcessQuery(False, query)
                    return True

    for word in text:
        if word in plants:
            plantscore += 1
            keywords.insert(len(keywords), word)
        elif word in question:
            questionscore += 1
            keywords.insert(len(keywords), word)
        elif word in weather:
            weatherscore += 1
            keywords.insert(len(keywords), word)

    for word in keywords:
        if word in text:
            text.remove(word)

    def numCheck(num):
        try:
            int(num)
            return True
        except Exception:
            return False

    for word in text:
        if numCheck(word) or word == "+" or word == "-" or word == "*" or word == "/":
            keywords.insert(len(keywords), word)
        elif len(word) > 2:  # cutoff limit for sub-keywords  2
            keywords.insert(len(keywords), word)

    if len(keywords) < 2:
        return Exception("Keyword Error", "Not enough information to work off of")
    else:
        status = commandprocessor.process(keywords, [plantscore, questionscore, weatherscore], originaltext, secondary, client)
        if not status:
            raise ReferenceError(f"Could not process command given. Command: {originaltext}")

    return True
