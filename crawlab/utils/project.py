from crawlab.settings.setting_manager import SettingManager
from crawlab.spider import Spider


def get_settings(settings="settings"):
    _settings = SettingManager()
    _settings.set_settings(settings)
    return _settings


def update_settings(spider: Spider, settings: SettingManager):
    if hasattr(spider, "custom_settings"):
        custom_settings = getattr(spider, "custom_settings")
        settings.update_values(custom_settings)
