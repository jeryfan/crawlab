from crawlab.settings.setting_manager import SettingManager


def get_settings(settings="settings"):
    _settings = SettingManager()
    _settings.set_settings(settings)
    return _settings
