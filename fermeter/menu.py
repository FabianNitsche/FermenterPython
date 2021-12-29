import RPi.GPIO as GPIO

class Menu(object):
    upper_button = 23
    lower_button = 24

    def __init__(self):
        self._menu_items = ["Wärmer", "Kälter", "Ausschalten"]
        self.current_item = self._menu_items[0]
        self.title = "Auswahl"

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass