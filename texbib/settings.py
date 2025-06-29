import os
import configparser
from pathlib import Path


class Settings:

    def __init__(self, env_var_prefix: str):
        self.env_var_prefix = env_var_prefix
        self.sections = {}

    def add_section(self, name: str):
        return self.sections.setdefault(name, SettingsSection())

    def read_settings(self, config_path: Path) -> dict[str, dict[str, str]]:
        config = configparser.ConfigParser()
        config.read(config_path.absolute())

        for section in config.sections():
            if not section in self.sections:
                raise ValueError(f'Unkown config section "{section}"')
            self.sections[section].read_from_config(config[section])

        for section_name, section in self.sections.items():
            section.read_from_env(f'{self.env_var_prefix}_{section_name}')

        return {n: s.test_settings() for n, s in self.sections.items()}


class SettingsSection:

    def __init__(self):
        self.settings = {}

    def add_setting(self, name: str, default=None):
        self.settings[name] = default
        return self

    def read_from_config(self, config_section):
        for setting in config_section:
            if not setting in self.settings:
                raise ValueError(f'Unkown setting "{setting}"')
            self.settings[setting] = config_section[setting]

    def read_from_env(self, prefix: str):
        for setting_name, setting in self.settings.items():
            var_name = f'{prefix}_{setting_name}'.upper()
            if var_name in os.environ:
                self.settings[setting_name] = os.environ[var_name]

    def test_settings(self) -> dict[str, str]:
        for name, value in self.settings.items():
            if value is None:
                raise ValueError(f'Missing required setting: {name}')
        return self.settings


def get_settings(config_path: Path):
    settings = Settings('bib')
    # settings.add_section('core') \
        # .add_setting('test') \
        # .add_setting('bibdir', default=None)
    settings.add_section('fulltext') \
        .add_setting('pdf_reader_cmd', default='xdg-open %%')
    return settings.read_settings(config_path)
