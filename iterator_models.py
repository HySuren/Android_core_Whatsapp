from pydantic import BaseModel

from core.activity import ActivityMethodDict
from services.code_activators.base_activator import BaseActivator
from datetime import datetime

# parameters Example:
# {"min_cnt_calls": 0, "max_cnt_calls": 20, "reg_seconds_timeout":300,"reg_phones_entry_limit": 5, "two_step_auth_code": "111111", "photo": "NONE_PHOTO", "about": "NONE_ABOUT", "randomize_contacts_date": true, "reload_backup": false, "night_mode": false, "grant_wa_permissions": false}


class RegAggregator(BaseModel):
    name: str
    operators: tuple[str] = ('any',)
    country: str = 'russia'


class Config(BaseModel):
    enable_new_iters: bool = False
    test_mode: bool = False
    reinstall_wa: bool = False

    app: str = None

    links_domain: str = None

    reg_aggregators: list[RegAggregator] = None
    reg_bad_phones_retries: int = None

    messages_limit: int = None
    messages_breaktime_min: int = None
    messages_breaktime_rand: int = None
    contacts_send: int = None
    contacts_reg: int = None
    one_country_iter: bool = None
    parameters: dict | None
    serial_binding: dict | None  # Example {"default": true, "farm_name": false}
    proxy_status: dict | None  # Example {"default": {"reg": false, "send": false, "scan": false}}
    wa_version: str | None = 'wa2.23.25.83.apk'
    campaign_test: dict | None  # Example {"default": {"reg": false, "send": false}}
    bad_devices: list | None = []
    iteration_timeout_min: int = 20  # Lifetime of iteration process


class DeviceInfo(BaseModel):
    serial: str
    ip: str = None
    params: dict = {}


class Contact(BaseModel):
    phone: str
    name: str


class Account(BaseModel):
    id: int = None
    registered: bool = False
    phone: str = None
    activate_service_id: str = None
    code: str = None
    name: str = None
    photo: str = None
    about: str = None
    two_step_auth_code: str = None
    backup: str = None
    banned: bool = False
    web_backup: str = None
    app: str = None
    linked_info: int = None
    country: str = None


class Campaign(BaseModel):
    id: int
    script_ids: list = []
    messages_limit: int = None
    read_messages: bool = True
    messages_breaktime_min: int = None
    messages_breaktime_rand: int = None
    without_internet: bool = False
    reg_aggregators: list[RegAggregator] = None
    contacts_send: int = None
    contacts_reg: int = None
    one_country_iter: bool = None
    parameters: dict | None


class Messages(BaseModel):
    messages_to_send: list = []
    messages_sent: list = []
    messages_not_valid: list = []
    messages_income: list = []
    images: list = []

    def __add__(self, other: "Messages"):
        self.messages_to_send += other.messages_to_send
        self.messages_sent += other.messages_sent
        self.messages_not_valid += other.messages_not_valid
        self.messages_income += other.messages_income
        return self

    def __bool__(self):
        if self.messages_to_send == [] and self.messages_sent == [] and self.messages_not_valid == [] and self.messages_income == []:
            return False
        return True


class GeneratedAccountInfo(BaseModel):
    id: int
    name: str
    photo_url: str


class Contacts(BaseModel):
    phones: list[str] = []


class Options(BaseModel):
    activities_methods: ActivityMethodDict
    reg_aggregators: list[RegAggregator]
    code_activator: BaseActivator = BaseActivator(operators=None, region=None)
    reinstall_wa: bool
    retry_bad_phone: int
    timeout_new_iter: int = 5
    timeout_new_iter_loading: int = 60
    timeout_getting_code: int = 60
    timeout_getting_code_calls: int = 150
    proceed: bool = False
    stop_unknown: bool = False
    read_messages: bool
    messages_breaktime_min: int
    messages_breaktime_rand: int
    make_web_backup: bool
    just_connected: bool = False
    data_for_account: GeneratedAccountInfo | None
    contacts: Contacts
    contacts_send: int = None
    contacts_reg: int = None
    one_country_iter: bool = None
    parameters: dict | None


class IteratorAnswer(BaseModel):
    id: int = None
    task: str
    device_info: DeviceInfo
    account: Account
    campaign: Campaign
    messages: Messages
    options: Options
    is_process_active: bool = True
    start_time: datetime = datetime.now()


class Proxy(BaseModel):
    host: str = None
    port: int = None
    username: str = None
    password: str = None
    type: int = None
    link: str = None
    country: str = None
    change: bool = None


class DbInfo(BaseModel):
    jid: int | None
    chat_id: int | None
    message_id: int | None
    phone: int | None
    receipt_device_jid_row_id: int | None
    hidden: int | None
    key_id: str | None
    unix_time: int | None
    author_device_jid: int | None


class WarmStatus(BaseModel):
    warm_enabled: bool | None
