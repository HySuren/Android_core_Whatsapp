from pydantic import BaseModel
from pydantic.class_validators import root_validator

from services.database import PgDriver


class PropModel(BaseModel):
    id: int | None
    fingerprint: str | None
    brand: str | None
    manufacturer: str | None
    tags: str | None
    model: str | None
    name: str | None
    build_id: str | None
    device: str | None
    display_id: str | None
    incremental: str | None
    date: str | None
    date_utc: str | None
    build_type: str | None
    build_user: str | None
    host: str | None
    flavor: str | None

    @root_validator
    def validate_values(cls, values):
        result = {}
        for value in values.keys():
            if values[value] is not None and value != 'id':
                result[value] = values[value].replace(" ", "_sp_")
            else:
                result[value] = values[value]
        return result


def get_random_props() -> PropModel:
    with PgDriver() as curr:
        curr.execute(
            """
                select *
                from tmp.props
                where is_using = true
                order by random()
                limit 1
            """
        )

        if item := curr.fetchone():
            return PropModel(**item)


def get_props_id_by_fingerprint(fingerprint) -> PropModel:
    with PgDriver() as curr:
        curr.execute(
            """
                select id
                from tmp.props
                where fingerprint = %s
            """, (fingerprint,)
        )

        if item := curr.fetchone():
            return item['id']


def update_device_prop(fingerprint, serial):
    with PgDriver() as curr:
        curr.execute(
            """
                update devices
                set prop = %s
                where serial = %s
            """, (fingerprint, serial)
        )
