from serpapi import GoogleSearch
import traceback

apikey = "612709437bff2aee019293a885e03f8b8931d11244bf995c8ff9f5dac25e97bd"


def search(information):
    search = GoogleSearch({
        'q': information,
        "location": "Broken Arrow, Oklahoma",
        "api_key": apikey})
    result = search.get_dict()
    try:
        answer_box = result['answer_box']
        if answer_box['type'] == 'organic_result':
            if 'snippet' not in answer_box and 'answer' in answer_box:
                return {'answer': answer_box['answer']}
            elif 'answer' not in answer_box and 'snippet' in answer_box:
                return {'answer': answer_box['snippet']}
            elif 'answer' in answer_box and 'snippet' in answer_box:
                return {'snippet': answer_box['snippet'], 'answer': answer_box['answer']}
            else:
                if 'organic_results' in result:
                    return {'answer': "The result I have for you is a bit crude. ['organic_results'][0]['snippet']"}
                else:
                    return {'error': "This seems like something you're going to want to search on your own. "
                                     "I can't contextualize enough information."}
        else:
            return False
    except Exception as err:
        print(repr(err))
        traceback.print_tb(err.__traceback__)
        return False
