upper_button_pin = 23
lower_button_pin = 24

class UserInput(object):

    def __init__(self, gpio):
        self._menu_items = ["Wärmer", "Kälter", "Ausschalten"]
        self._current_item = 0
        self.title = "Auswahl"
        self.temperatureGoal = 30
        self.exit = False

        def upper_button_callback(channel):
            self._upper_button_pressed()
        def lower_button_callback(channel):
            self._lower_button_pressed()

        gpio.add_input(upper_button_pin, upper_button_callback)
        gpio.add_input(lower_button_pin, lower_button_callback)

    def get_current_item(self):
        return self._menu_items[self._current_item]

    def _upper_button_pressed(self):
        current = self._current_item
        current += 1
        if current >= len(self._menu_items):
            current = 0
        self._current_item = current

    def _lower_button_pressed(self):
        current_item = self._current_item
        if current_item == 0 and self.temperatureGoal <= 34:
            self.temperatureGoal += 1
        elif current_item == 1:
            self.temperatureGoal -= 1
        elif current_item == 2:
            self.exit = True
            

