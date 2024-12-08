class AppActivity:

    def __init__(self, package, activity_name, popup_exists=False, text=None, is_loading=False, is_call=False):
        self.package = package
        self.activity_name = activity_name
        self.popup_exists = popup_exists
        self.is_loading = is_loading
        self.is_call = is_call
        self.text = text
        self.uniq_code = f"P={self.package}_A={self.activity_name}_U={int(self.popup_exists)}_T{hash(self.text)}_L{int(self.is_loading)}_C{int(self.is_call)}"

    def __eq__(self, other: "AppActivity"):
        return self.package == other.package \
               and self.activity_name == other.activity_name \
               and self.popup_exists == other.popup_exists \
               and self.is_loading == other.is_loading \
               and self.is_call == other.is_call \
               and self.text == other.text

    def __hash__(self):
        return hash(self.uniq_code)

    def __str__(self):
        text = self.text.replace('\n', '\\n') if self.text else None
        return f"AppActivity(package='{self.package}', activity_name='{self.activity_name}'{', popup_exists=True' if self.popup_exists else ''}{', text=' + text if self.text else ''}{', is_loading=True' if self.is_loading else ''}{', is_call=True' if self.is_call else ''})"


class AppActivityWithLikeText(AppActivity):

    def __eq__(self, other: "AppActivity"):
        return self.package == other.package \
               and self.activity_name == other.activity_name \
               and self.popup_exists == other.popup_exists \
               and self.is_loading == other.is_loading \
               and self.is_call == other.is_call \
               and self.text in other.text

    def __hash__(self):
        return super().__hash__()


class ActivityMethodDict(dict):
    def __init__(self, *args, **kwargs):
        super(ActivityMethodDict, self).__init__(*args, **kwargs)
        self._keys = list(self.keys())
        self._values = list(self.values())

    def __getitem__(self, item):
        return self._values[self._keys.index(item)]

    def get(self, value, other_value=None):
        try:
            return self.__getitem__(value)
        except (IndexError, ValueError):
            return other_value


class Any(str):

    def __eq__(self, other):
        return True

    def __str__(self):
        return 'ANY'

    def __hash__(self):
        return hash(1)

    def __int__(self):
        return 5


ANY = Any()
