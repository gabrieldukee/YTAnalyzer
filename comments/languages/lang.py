import os
import json

def get_config_path():
    base_dir = os.path.dirname(__file__)
    return os.path.join(base_dir, "language.cfg")

def load_language():
    config_path = get_config_path()
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            lang = f.read().strip()
        if lang in ("1", "2"):
            return lang
    return "1"

LANGUAGE = load_language()

def load_messages():
    base_dir = os.path.dirname(__file__)
    messages_file = os.path.join(base_dir, "messages.json")
    if not os.path.exists(messages_file):
        raise FileNotFoundError("Arquivo messages.json não encontrado!")
    with open(messages_file, "r", encoding="utf-8") as f:
        messages = json.load(f)
    return messages

MESSAGES = load_messages()

def get_message(key, **kwargs):
    lang = "en" if LANGUAGE == "1" else "pt"
    message = MESSAGES.get(lang, {}).get(key, key)
    if kwargs:
        message = message.format(**kwargs)
    return message

def set_language(lang_code):
    global LANGUAGE
    if lang_code in ("1", "2"):
        LANGUAGE = lang_code
        config_path = get_config_path()
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(lang_code)
    else:
        raise ValueError("Invalid language code")