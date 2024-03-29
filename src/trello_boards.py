import typing
from collections import OrderedDict

from requests import Response

from settings import trelloSettings
from src.trello_base import TrelloBase
from src.trello_dataclasses import SerializedCard
from src.trello_dataclasses import SerializedCardLabels
from src.trello_dataclasses import SerializedList
from src.trello_dataclasses import SerializedMember


class TrelloBoard(TrelloBase):
    def __init__(self):
        super().__init__()
        self.primary_url = f'boards/{trelloSettings.BOARD_ID}/'

    def create_board(self, **kwargs) -> Response:
        """
        Create a new board.

        possible request params:
            - name: The new name for the board.
            - defaultLabels: Determines whether to use the
                default set of labels.
            - defaultLists: Determines whether to add the default
                            set of lists to a board (To Do, Doing, Done).
            - desc: A new description for the board.
            - idOrganization: The id or name of the Workspace
                the board should belong to.
            - idBoardSource: The id of a board to copy into the new board.
            - keepFromSource: To keep cards from
                the original board pass in the value cards.
            - powerUps: The Power-Ups that should be enabled on the new board.
                        One of: all, calendar, cardAging, recap, voting.
            - prefs_permissionLevel: The permissions level of the board.
                                     One of: org, private, public.
            - prefs_voting: Who can vote on this board.
                            One of disabled, members, observers, org, public.
            - prefs_comments: Who can comment on cards on this board.
                One of: disabled, members,
                observers, org, public.
            - prefs_invitations: Determines what
                types of members can invite users to join.
                One of: admins, members.
            - prefs_selfJoin: Determines whether users can
                join the boards themselves
                or whether they have to be invited.
            - prefs_cardCovers: Determines whether card covers are enabled.
            - prefs_background: The id of a custom background or one of:
                blue, orange, green, red,
                purple, pink, lime, sky, grey.
            - prefs_cardAging: Determines the type of card aging
                that should take place
                on the board if card aging is enabled.
                One of: pirate, regular.

            :return: Response
        """
        if 'name' not in kwargs.keys():
            raise NotImplementedError('Should contains param: "name"!')

        secondary_params = OrderedDict(kwargs)
        response = self.make_response(
            call_method='POST',
            primary_url='boards/',
            secondary_params=secondary_params,
        )

        return response

    def delete_board(self, board_id: str) -> Response:
        """
        Delete a Board

        :param board_id: Board ID to remove
        :return: Response
        """
        response = self.make_response(
            call_method='DELETE',
            primary_url='boards/',
            secondary_url=board_id,
            is_headers=False,
        )

        return response

    def get_member(self, member_id: typing.AnyStr) -> SerializedMember:
        """
        Get a member by member_id

        :param member_id: ID of member
        :return: BoardMember
        """
        response = self.make_response(
            call_method='GET', primary_url='members/', secondary_url=member_id,
        )

        member_data: SerializedMember = SerializedMember.parse_obj(
            response.json(),
        )

        return member_data

    def get_members(self) -> typing.List[SerializedMember]:
        """
        Get the Members for a board

        :return: List[BoardMember]
        """
        response = self.make_response(
            call_method='GET',
            primary_url=self.primary_url,
            secondary_url='members',
        )

        members: typing.List[SerializedMember] = [
            SerializedMember.parse_obj(member) for member in response.json()
        ]

        return members

    def get_lists(
        self,
        list_filter: typing.Optional[str] = 'open',
    ) -> typing.List[SerializedList]:
        """
        Get available lists of board

        :param list_filter: Valid values: all, closed, none, open
        :return: List[SerializedList]
        """
        secondary_params = OrderedDict({'filter': list_filter})
        response = self.make_response(
            call_method='GET',
            primary_url=self.primary_url,
            secondary_params=secondary_params,
            secondary_url='lists',
            is_headers=False,
        )

        board_lists: typing.List[SerializedList] = [
            SerializedList.parse_obj(board_list) for board_list in
            response.json()
        ]

        return board_lists

    def invite_member(
        self,
        email: str,
        full_name: typing.Optional[str] = None,
    ) -> Response:
        """
        Invite a Member to a Board via their email address.

        :param email: The email address of a user.
        :param full_name: The full name of the user.
        :return: Response
        """
        secondary_params = OrderedDict(
            {
                'email': email,
                'fullName': full_name,
            },
        )

        response = self.make_response(
            call_method='PUT',
            primary_url=self.primary_url,
            secondary_url='members',
            secondary_params=secondary_params,
            is_headers=False,
        )

        return response

    def remove_member(self, member_id: str) -> Response:
        """
        Delete a Member from board

        :param member_id: The id of the member to remove from the board.
        :return: Response
        """
        response = self.make_response(
            call_method='DELETE',
            primary_url=self.primary_url,
            secondary_url=f'members/{member_id}',
            is_headers=False,
        )

        return response

    def create_list(
            self,
            list_name: typing.Optional[str],
            list_pos: typing.Literal['top', 'bottom'] = 'top',
    ) -> Response:
        """
        Create a new List on a Board

        :param list_name: The name of the list to be created.
        :param list_pos: Determines the position of the list.
                         Valid values: top, bottom. Default - 'top'.
        :return: Response
        """
        secondary_params = OrderedDict({
            'name': list_name,
            'pos': list_pos,
        })

        response = self.make_response(
            call_method='POST',
            primary_url=self.primary_url,
            secondary_url='lists',
            secondary_params=secondary_params,
            is_headers=False,
        )

        return response

    def archive_list(self, list_id: str, archive: bool = True) -> Response:
        """
        Archive or unarchive a list

        :param list_id: The ID of the list
        :param archive: If True - archive, False - unarchive
        :return: Response
        """
        secondary_params = OrderedDict(
            {'value': 'true' * archive + 'false' * (not archive)},
        )

        response = self.make_response(
            call_method='PUT',
            primary_url='lists/',
            secondary_url=f'{list_id}/closed',
            secondary_params=secondary_params,
            is_headers=False,
        )

        return response

    def get_card(self, card_id: str) -> SerializedCard:
        """
        Get card by idCard

        :return: SerializedCard
        """
        response = self.make_response(
            call_method='GET',
            primary_url=self.primary_url,
            secondary_url=f'cards/{card_id}',
        )

        card: SerializedCard = SerializedCard.parse_obj(response.json())

        return card

    def get_cards(
            self,
            card_filter: typing.Optional[str] = 'open',
    ) -> typing.List[SerializedCard]:
        """
        Get cards on a board

        :param card_filter: Valid Values: all, closed, none, open, visible.
        :return: List[SerializedCard]
        """
        response = self.make_response(
            call_method='GET',
            primary_url=self.primary_url,
            secondary_url=f'cards/{card_filter}',
        )

        card_list: typing.List[SerializedCard] = [
            SerializedCard.parse_obj(card) for card in response.json()
        ]

        return card_list

    def get_labels(self) -> typing.List[SerializedCardLabels]:
        """
        Get labels on a board

        :return: List[TrelloCardLabels]
        """
        response = self.make_response(
            call_method='GET',
            primary_url=self.primary_url,
            secondary_url='labels',
            is_headers=False,
        )

        label_list: typing.List[SerializedCardLabels] = [
            SerializedCardLabels.parse_obj(label) for label in
            response.json()
        ]

        return label_list

    def create_label(
            self,
            label_name: str,
            label_color: str = 'null',
    ) -> Response:
        """
        Create a new Label on a Board

        :param label_name: The name of the label to be created.
        :param label_color: Sets the color of the new label.
        :return: Response
        """
        secondary_params = OrderedDict({
            'name': label_name,
            'color': label_color,
        })

        response = self.make_response(
            call_method='POST',
            primary_url=self.primary_url,
            secondary_url='labels',
            secondary_params=secondary_params,
            is_headers=False,
        )

        return response

    def delete_label(self, label_id: str) -> Response:
        """
        Delete a label by ID

        :param label_id: The ID of the label
        :return: Response
        """
        response = self.make_response(
            call_method='DELETE',
            primary_url='labels/',
            secondary_url=f'{label_id}',
            is_headers=False,
        )

        return response
