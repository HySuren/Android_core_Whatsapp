import time

import uiautomator2

from services import utils
from services.phone_payment import manangers, qiwi_payment


black_list = ('9777260736','9777259681','9777259834','9777259082','9777260693','9777260570','9777259561','9777259501',
'9777258947','9777258986','9777259037','9777259735','9777260598','9777258593','9777258654','9777258944','9777259023',
'9777259143','9777259975','9777259917','9777260373','9777259601','9777258607','9777258858','9777259088','9777259209',
'9777258940','9777259783','9777258837','9777259027','9777259502','9777258683','9777258733','9777259443','9777260449',
'9777260710','9777260674','9777258592','9777259459','9777258539','9999110164','9777258552','9777258938','9777259268',
'9777259173','9777260384'
)

def pay_by_phone(phone, price=None):
    if price is None:
        price = manangers.get_price_by_phone(phone)
        if not price:
            price('CANT FIND PRICE FOR THIS PHONE IN DB, PLEASE SET PRICE MANUAL')
    qiwi_payment.pay(phone, int(price))


def pay_by_serial(serial, price=None):
    db_res = manangers.get_price_and_phone_by_serial(serial)

    if not db_res:
        price('UNKNOWN SERIAL')
        return

    phone, price_from_db = db_res

    if price is None:
        price = price_from_db

    qiwi_payment.pay(phone, int(price))
    manangers.mark_phone_as_payed(phone)


def pay_all():
    phones = manangers.get_phones_to_pay()
    for phone, price, operator in phones:
        qiwi_payment.pay(phone, int(price))
        manangers.mark_phone_as_payed(phone)


def pay_all_safe():
    phones = manangers.get_phones_to_pay_safe()
    for phone, price, operator in phones:
        qiwi_payment.pay(phone, int(price))
        manangers.mark_phone_as_payed(phone)


def pay_mobile():
    corporate_phone = []
    d = uiautomator2.connect()
    print('Запускаю оплату')
    phones = manangers.get_phones_to_pay_safe()

    filtered_phones = []
    for phone in phones:
        if phone[0] in black_list:
            corporate_phone.append(phone[0])
        else:
            filtered_phones.append(phone)
    phones = filtered_phones

    print(f'Получил номера {phones}')
    if corporate_phone:
        print(f'Номера которые попали в black_list:\n{corporate_phone}')

    for phone, price, operator in phones:
        if phone is None:
            continue
        print(f'Взял в работу телефон {phone}')
        try:
            d.reset_uiautomator()
            tinkoff_pay(phone=phone, price=int(price), d=d)
            manangers.update_status(phone)
            manangers.update_device_enable_by_phone(phone)
            manangers.insert_transaction_mobile(phone=phone, amount=price)
            print(f'телефон {phone} пополнен')
        except Exception as e:
            print(phone)
            print(e)


def tinkoff_pay(phone:str, price:int, d):
    d(resourceId="com.idamob.tinkoff.android:id/bottom_navigation_item_title", text="Платежи").click()

    d.swipe_ext("up", 1)
    d.swipe_ext("up", 1)
    time.sleep(2)
    d(resourceId="com.idamob.tinkoff.android:id/titleView", text="Мобильная связь").click()

    d(resourceId="com.idamob.tinkoff.android:id/phone_number").set_text(phone)
    d(resourceId="com.idamob.tinkoff.android:id/contactName").click()

    d(resourceId="com.idamob.tinkoff.android:id/edit_text", text="0").set_text(str(price))
    time.sleep(3)
    # d(text="Далее").click()
    d(text="Next").click()
    time.sleep(3)
    d(resourceId="com.idamob.tinkoff.android:id/pay_button").click()
    print(f'ПОПОЛНИЛ {phone}')
    time.sleep(7)

    display = utils.get_display(d)
    description = display.get('resource-id', f'com.idamob.tinkoff.android:id/receipt_apply')
    if description.exists:
        d(text="Готово").click()
        time.sleep(2)
        display = utils.get_display(d)
        description = display.get('resource-id', f'com.idamob.tinkoff.android:id/closeButton')
        if description.exists:
            d(resourceId="com.idamob.tinkoff.android:id/closeButton").click()
    else:
        print('Введите 2 любых символа для продолжения')
        while True:
            x = input()
            if len(x) > 1:
                break
            elif x == 'err':
                raise Exception


    # d(resourceId="com.idamob.tinkoff.android:id/receipt_apply").click()
    # time.sleep(3)
    # d(resourceId="com.idamob.tinkoff.android:id/closeButton").click()
