import pytest
from project import Window
from translator import Translator

@pytest.fixture
def translator():
    return Translator("en", "es")

@pytest.fixture
def window():
    return Window()

def test_translate_text(window):
    window.from_textbox.insert("1.0", "Hello")
    window.translate_text()
    assert window.to_textbox.get("1.0", "end-1c") != ""

def test_switch_text(window):
    window.from_textbox.insert("1.0", "Hello")
    window.to_textbox.insert("1.0", "Hola")
    window.switch_text()
    assert window.from_textbox.get("1.0", "end-1c") == "Hola"
    assert window.to_textbox.get("1.0", "end-1c") == "Hello"

def test_check_languages(window, capsys):
    window.check_languages()
    captured = capsys.readouterr()
    assert "Available languages:" in captured.out

def test_refresh_comboboxes(window):
    window.refresh_comboboxes()
    assert len(window.language_names) > 0

def test_translate_empty_text(window):
    window.translate_text()
    assert window.to_textbox.get("1.0", "end-1c") == ""

def test_update_from_code(window):
    window.update_from_code()
    assert window.translator.from_code == "en"

def test_update_to_code(window):
    window.update_to_code()
    assert window.translator.to_code == "es"

def test_translate(translator):
    translated_text = translator.translate("Hello")
    assert translated_text is not None

def test_update_language_map(translator):
    initial_map_length = len(translator._language_map)
    translator.update_language_map()
    updated_map_length = len(translator._language_map)
    assert updated_map_length > initial_map_length
