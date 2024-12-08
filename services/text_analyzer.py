import json

import requests

from services import utils


ANALYZER_API_URL = 'http://api.sntq.ru:404/ask'
ANALYZER_API_URL_V2 = 'http://api.sntq.ru:404/ask2'


class ANSWER_TYPES:
    YES                     = 'yes'
    QUESTION                = 'question'
    NO                      = 'no'
    STOP                    = 'stop'


ANSWERS_CLASSES_DICT = {
    ANSWER_TYPES.YES        : 1,
    ANSWER_TYPES.QUESTION   : 1,
    ANSWER_TYPES.NO         : 0,
    ANSWER_TYPES.STOP       : 0
}


@utils.try_times(10, catch_exceptions=(json.JSONDecodeError,), default_result=ANSWERS_CLASSES_DICT[ANSWER_TYPES.YES])
def analyze(text: str):
    response = requests.post(ANALYZER_API_URL_V2, json={"msg": text})
    answer = response.json()['answer']
    return ANSWERS_CLASSES_DICT[answer]
