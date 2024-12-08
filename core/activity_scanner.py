import uiautomator2 as u2
from core.activity import AppActivity
from core.app_page_parser import AppPageElement
from core.frame_types import LOADING_TYPES, EXCLUDE_FRAMES, CALL_TYPES
from services import utils


class ActivityScanner:

    def __init__(self, device: u2.Device):
        self.device = device
        app_current = utils.app_current(self.device)
        self.package = app_current['package']
        self.activity = app_current['activity']
        self.display = self._get_display()

    def _get_display(self) -> AppPageElement:
        display = utils.get_display(self.device)
        display = display.get('package', self.package)
        return display

    def _check_frame(self) -> bool:
        if self.display.width != self.device.info['displayWidth'] or self.display.height != self.device.info['displayHeight']:
            return True

    def _get_frame_text(self, is_frame) -> str:
        if is_frame and self.display.get('class', 'android.widget.TextView').attributes.get('resource-id') not in EXCLUDE_FRAMES:
            # if not self.display.get('class', 'android.widget.TextView').text:
            #     print('@ WARNING: Empty frame!')
            return utils.replace_phone(self.display.get('class', 'android.widget.TextView').text, use_normalize=True)

    def _check_is_loading(self) -> bool:
        for i in LOADING_TYPES:
            if self.display.get('resource-id', i).exists:
                return True

    def _check_is_call(self) -> bool:
        for i in CALL_TYPES:
            if self.display.get('resource-id', i).exists:
                return True

    def scan(self) -> AppActivity:

        """ Получение информации о текущем экране """

        is_frame = self._check_frame()
        frame_text = self._get_frame_text(is_frame)
        if is_frame and not frame_text:
            is_frame = False
            frame_text = None
        is_loading = self._check_is_loading()
        is_call = self._check_is_call()

        return AppActivity(self.package, self.activity, bool(is_frame), frame_text, bool(is_loading), bool(is_call))
