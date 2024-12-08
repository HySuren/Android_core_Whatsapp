import time

import requests

from services.phone_payment import manangers, models


TOKEN_QIWI = '1a6b1b34114f10cea46cad27cba1d5e4'


def check_mobile_operator(phone_number: str) -> dict:
    """ Получение мобильного оператора """

    response = requests.post(
        'https://qiwi.com/mobile/detect.action',
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        data={'phone': "7" + phone_number}
    )
    return response.json()["message"]


def pay(phone, price):

    print("PAY", f"Пополнение телефона {phone}")
    response = requests.post(
        url=f'https://edge.qiwi.com/sinap/api/v2/terms/{check_mobile_operator(phone)}/payments',
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'authorization': 'Bearer ' + TOKEN_QIWI
        },
        json={
            'id': str(int(time.time() * 1000)),
            'sum': {
                'amount': price,
                'currency': '643'
            },
            'paymentMethod': {
                'type': 'Account',
                'accountId': '643',
            },
            'fields': {
                'account': phone
            }
        }
    )
    match code := response.status_code:
        case _ if 200 <= code < 300:
            manangers.insert_transaction(models.PaymentsResponse(**response.json()))
            print("PAY: COMPLETE", f"Телефон пополнен: {response.json()}")

        case 401:
            print("PAY: FAIL", f"Телефон не пополнен: status_code - 401")
        case _:
            print(f"PAY: FAIL Телефон не пополнен: status_code - {response.status_code} response_json = {response.json()}")
