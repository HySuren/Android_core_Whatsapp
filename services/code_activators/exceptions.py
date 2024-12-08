class PhoneActivationException(Exception):
    def __init__(self, text=''):
        self.txt = text

class TimeOutExceptionWaitCode(PhoneActivationException): ...


class CancelNumber(PhoneActivationException): ...


class GetNumberTimeoutException(PhoneActivationException): ...


class BuyNumberException(PhoneActivationException): ...


class GetActivationCodeException(PhoneActivationException): ...


class UpdateNumberStatusException(PhoneActivationException): ...


class BanException(PhoneActivationException): ...


class NoCountryInService(Exception):

    def __init__(self, county, activator):
        self.county = county
        self.activator = activator