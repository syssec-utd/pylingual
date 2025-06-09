from .buttons import InlineButton
from .deps import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton
ReplyButton = str | KeyboardButton

class ReplyKeyboard(ReplyKeyboardMarkup):
    buttons: list[ReplyButton] = None
    row_width = 1

    def __init__(self, *buttons: str | KeyboardButton):
        super().__init__(row_width=self.row_width, resize_keyboard=True)
        self.add(*(self.buttons or []), *buttons)

class InlineKeyboard(InlineKeyboardMarkup):
    buttons: list[InlineButton] = None
    row_width = 1

    def __init__(self, *buttons: InlineButton):
        super().__init__(row_width=self.row_width)
        self.add(*(self.buttons or []), *buttons)