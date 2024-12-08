from . import exceptions as activate_exceptions
from .config import ActivatorName

from .sms_hub import SmsHub
from .sms_activate import SmsActivate
from .sms_activate2 import SmsActivate2
from .beeline import SMS_Beeline
from .five_sim import FiveSim
from .online_sim import OnlineSim
from .vak_sms import VakSms
from .sms_activate_like import SmsActivateLike
from .sms_activate_rent import SmsActivateRent
from .drop_sms import DropSms
from .gsm import Gsm
from .drop_sms_getsms import DropSmsGetsms
from .sms_man import SmsMan


ACTIVATORS_NAMES_DICT = {
    ActivatorName.SMS_ACTIVATE: SmsActivate,
    ActivatorName.SMS_ACTIVATE2: SmsActivate2,
    ActivatorName.FIVE_SIM: FiveSim,
    ActivatorName.ONLINE_SIM: OnlineSim,
    ActivatorName.VAK_SMS: VakSms,
    ActivatorName.SMS_ACTIVATE_LIKE: SmsActivateLike,
    ActivatorName.SMS_ACTIVATE_RENT: SmsActivateRent,
    ActivatorName.DROP_SMS: DropSms,
    ActivatorName.GSM: Gsm,
    ActivatorName.DROP_SMS_GETSMS: DropSmsGetsms,
    ActivatorName.SMS_BEELINE: SMS_Beeline,
    ActivatorName.SMS_HUB: SmsHub,
    ActivatorName.SMS_MAN: SmsMan,
}
