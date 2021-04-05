import typing

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from src.trello_boards import TrelloBoard
from src.trello_member import TrelloMember


class KeyboardBuilder:
    def __init__(self, list_of_values: typing.List[typing.Any]):
        self.list_of_values = list_of_values
        self.skip_cancel_buttons = [
            KeyboardButton(text='Skip'),
            KeyboardButton(text='Cancel')
        ]

    def create_new_keyboard(self) -> ReplyKeyboardMarkup:
        list_of_values = self.convert_to_buttons(self.list_of_values)
        if len(self.list_of_values) not in range(2):
            list_of_values = self.to_table_buttons(list_of_values=list_of_values,
                                                   n_in_row=2)
        keyboard = ReplyKeyboardMarkup(
            keyboard=[*list_of_values, self.skip_cancel_buttons],
            resize_keyboard=True,
            one_time_keyboard=True
        )
        return keyboard

    @staticmethod
    def to_table_buttons(list_of_values: typing.List[typing.Any], n_in_row: int = 2) -> typing.List[typing.Any]:
        if len(list_of_values) % 2 == 0:
            return [list_of_values[i:i + n_in_row] for i in range(0, len(list_of_values), n_in_row)]
        else:
            return [list_of_values[i:i + n_in_row] for i in range(0, len(list_of_values) - 1, n_in_row)] \
                   + [[list_of_values[-1]]]

    @staticmethod
    def convert_to_buttons(list_of_values: typing.List[typing.Any]) -> typing.List[typing.Any]:
        return [KeyboardButton(text=value) for value in list_of_values]


Board = TrelloBoard()
board_members = Board.get_memberships()
Member = TrelloMember()
member_names = [Member.get_member(board_member.id_member).full_name for board_member in board_members]
tags_colors = ['Green🟩', 'Yellow🟨', 'Orange🟧', 'Red🟥', 'Purple🟪', 'Blue🟦']

keyboard_empty = KeyboardBuilder([]).create_new_keyboard()
keyboard_with_members = KeyboardBuilder(member_names).create_new_keyboard()
keyboard_with_tags = KeyboardBuilder(tags_colors).create_new_keyboard()

if __name__ == "__main__":
    pass

