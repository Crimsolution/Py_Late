import argostranslate.package
import argostranslate.translate
import threading, time

class Translator:
    def __init__(self, _from_: str, _to_: str):
        self._from_code = _from_
        self._to_code = _to_
        self._language_map = {}
        self.update_language_map()

    @property
    def from_code(self) -> str:
        return self._from_code

    @from_code.setter
    def from_code(self, code: str):
        self._from_code = code

    @property
    def to_code(self) -> str:
        return self._to_code

    @to_code.setter
    def to_code(self, code: str):
        self._to_code = code


    def get_language_names(self) -> dict:
        installed_languages = argostranslate.translate.get_installed_languages()
        return {lang.code: lang.name for lang in installed_languages}

    # updates our language map with available languages
    def update_language_map(self):
        self._language_map = self.get_language_names()

    # fast download method with 2 languages for first initialization
    def quick_download(self):
        argostranslate.package.update_package_index()
        available_packages = argostranslate.package.get_available_packages()
        packages_to_install = [
            next(filter(lambda x: x.from_code == "en" and x.to_code == "es", available_packages)),
            next(filter(lambda x: x.from_code == "es" and x.to_code == "en", available_packages))
        ]
        for package in packages_to_install:
            argostranslate.package.install_from_path(package.download())
        self.update_language_map()

    # downloads only selected packages from index (and their reverse translation order)
    def selected_download(self, selected_packages):
        for package in selected_packages:
            from_code, to_code = package.from_code, package.to_code
            reverse_package = next(
                (p for p in argostranslate.package.get_available_packages()
                 if p.from_code == to_code and p.to_code == from_code), None)
            argostranslate.package.install_from_path(package.download())
            if reverse_package:
                argostranslate.package.install_from_path(reverse_package.download())
        self.update_language_map()

    # tries to translate, fails if the langs aren't compatible / not available
    def translate(self, text: str) -> str:
        try:
            translated_text = argostranslate.translate.translate(text, self.from_code, self.to_code)
            return translated_text
        except AttributeError as e:
            raise ValueError(f"Error: {e}, no packages installed!")

    # returns installed packages
    def check_languages(self) -> list:
        return argostranslate.translate.get_installed_languages()

    # uninstalls all packages
    def uninstall(self):
        pkgs = argostranslate.package.get_installed_packages()
        for pkg in pkgs:
            argostranslate.package.uninstall(pkg)

    # gets packages from updated argos package index
    def get_packages(self):
        argostranslate.package.update_package_index()
        return argostranslate.package.get_available_packages()
