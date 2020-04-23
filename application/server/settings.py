import json
import os


class SettingNotFound(KeyError):
    pass

class DeleteFlag():
    pass


class Settings():
    def __init__(self, src, defaults, *args, **kwargs):
        self._defaults = defaults
        self._settings_file_src = src
        self._cached_settings = None
        self._settings_file_last_modified = -1

    def get(self, *keys):
        settings = self._load()
        if not keys:
            merged = dict()
            merged.update(self._defaults)
            merged.update(settings)
            return merged

        try:
            return self._get_from_nested(settings, keys)
        except KeyError:
            try:
                return self._get_from_nested(self._defaults, keys)
            except KeyError:
                raise SettingNotFound()

    def set(self, value, *keys):
        settings = self._load()
        if not keys:  # Full save, set everything as is.
            merged = dict()
            merged.update(settings)
            merged.update(value)
            self._save(merged)
            return

        mod_settings = self._set_to_nested(settings, value, keys)  # mod_settings will be same list with settings but eh.
        self._save(mod_settings)

    def _load(self, use_cache=True):
        if not os.path.isfile(self._settings_file_src):
            return {}

        if use_cache:
            file_last_mod = os.path.getmtime(self._settings_file_src)
            if file_last_mod == self._settings_file_last_modified:
                return self._cached_settings

        with open(self._settings_file_src, 'r') as s_file:
            settings = json.load(s_file)
            self._cache(settings)
            return settings

    def _cache(self, settings):
        self._cached_settings = settings
        self._settings_file_last_modified = os.path.getmtime(self._settings_file_src)

    def _save(self, settings):
        with open(self._settings_file_src, "w") as s_file:
            json.dump(settings, s_file, indent=2)
            self._cache(settings)

    def _get_from_nested(self, iterable, keys):
        layer = iterable
        for key in keys:
            if isinstance(key, dict):
                layer = self._find_in_list(layer, key)
            else:
                layer = layer[key]

        return layer

    def _set_to_nested(self, iterable, value, keys):
        layer = iterable
        keys = list(keys)
        last_key = keys.pop()

        for key in keys:
            try:
                if isinstance(key, dict):
                    layer = self._find_in_list(layer, key)
                else:
                    layer = layer[key]
            except KeyError:
                layer[key] = dict()
                layer = layer[key]

        if isinstance(last_key, dict):
            list_item = self._find_in_list(layer, last_key)
            index = layer.index(list_item)
        else:
            index = last_key

        if isinstance(value, DeleteFlag):
            del layer[index]
        else:
            layer[index] = value

        return iterable

    def _find_in_list(self, target_list, search_values_dict):
        if not isinstance(target_list, list):
            raise KeyError

        for item in target_list:
            for key, value in search_values_dict.items():
                try:
                    if item[key] != value:
                        break
                except KeyError:
                    break
            else:
                # No breaks, everything matched.
                return item
        else:
            # No breaks, nothing matched.
            raise KeyError


if __name__ == "__main__":
    test_settings = Settings('testSettings.json', {
        "A": {
            "AA": "AAA"
        },
        "B": {
            "BA": "BAA",
            "BB": "BBA"
        }
    })

    print(test_settings.get("A", "AA"))
    print(test_settings.get("B", "BB"))
    test_settings.set("TEST", "C", "CA", "CAA")
    print(test_settings.get("C", "CA", "CAA"))
