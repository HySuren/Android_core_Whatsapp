from services.database import PgDriver
from services.phone_payment.models import PaymentsResponse


def get_api_token():
    with PgDriver() as curr:
        curr.execute("select uuid from tmp.api_tokens where username = 'qiwi'")
        token = curr.fetchone()
        return token.get('uuid')


def get_price_by_phone(phone):
    with PgDriver() as curr:
        curr.execute("select price from tmp.white_devices where phone = %s", (phone,))
        item = curr.fetchone()
        return item['price']


def get_price_and_phone_by_serial(serial):
    with PgDriver() as curr:
        curr.execute("select phone, price from tmp.white_devices where serial = %s", (serial,))
        item = curr.fetchone()
        return item['phone'], item['price']


def get_phones_to_pay():
    with PgDriver() as curr:
        curr.execute("select phone, price, operator from tmp.white_devices where payed = false")
        items = curr.fetchall()
        return [(item['phone'], item['price'], item['operator']) for item in items]


def get_phones_to_pay_safe():
    with PgDriver() as curr:
        curr.execute('''
with t as (select distinct d.phone from tmp.white_devices d inner join tmp.white_transaction t on t.phone = d.phone and t.amount >= d.price and t.created_at >= (now() - interval '20 days') where payed is False),
upd as (update tmp.white_devices set payed_comment = 'Не буду этих пополнять', payed = True where payed is false and phone in (select phone from t))
select phone, price, operator from tmp.white_devices where payed is False
        ''')

        items = curr.fetchall()
        return [(item['phone'], item['price'], item['operator']) for item in items]


def insert_transaction(transaction: PaymentsResponse):
    with PgDriver() as curr:
        curr.execute("""
            INSERT INTO tmp.white_transaction
            (transaction_id, transaction_state, operator_code, phone, amount) 
            VALUES %s 
            returning phone
        """, [transaction.prepare_to_insert()]
                     )
        item = curr.fetchone()
        phone = item["phone"]
        curr.execute("update tmp.white_devices set payed = true where phone = %s", (phone,))


def update_status(phone):
    with PgDriver() as curr:
        curr.execute("update tmp.white_devices set payed = true where phone = %s", (phone,))


def update_device_enable_by_phone(phone):
    with PgDriver() as curr:
        curr.execute("update devices set enabled = true where serial in (select serial_number from tmp.white_devices where phone = %s);", (phone,))


def insert_transaction_mobile(phone, amount):
    with PgDriver() as curr:
        curr.execute("""
            INSERT INTO tmp.white_transaction
            (phone, amount) 
            select %s, %s 
        """, (phone, amount)
        )


def mark_phone_as_payed(phone):
    ...
    # with PgDriver() as curr:
    #     curr.execute("update tmp.white_devices set payed = true where phone = %s", (phone,) )
