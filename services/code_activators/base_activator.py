import random
from typing import Sequence

import pydantic

from services.code_activators.exceptions import NoCountryInService


class ActivatorID:

    def __init__(self, name, country_id):
        self.name: str = name
        self.country_id: str = country_id


class Region:

    def __init__(self, name, code, activators_ids):
        self.name: str = name
        self.code: int = code
        self.activators_ids: list[ActivatorID] = activators_ids

    def get_activator_id(self, activator_name):
        for activator_id in self.activators_ids:
            if activator_id.name == activator_name:
                if activator_id.country_id:
                    return activator_id.country_id
        raise NoCountryInService(self.name, activator_name)

    def get_country(self):
        return self.code


class RegionsList(list):

    def __getitem__(self, country_name: str) -> Region:
        for region in self:
            if region.name == country_name:
                return region

    def get_code(self, country_name, activator_name):
        return self[country_name].get_activator_id(activator_name)

    def get_country_code(self, country_name):
        return self[country_name].get_country()


@pydantic.dataclasses.dataclass
class BaseActivator:

    NAME: str = None

    def __init__(self, operators: Sequence[str] | None, region):
        if operators:
            self.operator = random.choice(operators)
        else:
            self.operator = None
        self.region = region

    def get_phone(self, srvice='wa') -> tuple[int, str, str]: ...

    def get_code(self, id: int, timeout=60): ...

    def phone_confirm(self, id: int): ...

    def sms_confirm(self, id: int): ...

    def phone_cancel(self, id: int): ...

    def phone_ban(self, id: int): ...

    def _update_number_status(self, id: int, status: int | str): ...

    @classmethod
    def check_balance(cls): ...
