import minsk.utils as utils


class GameState(utils.CommonEqualityMixin):
    def __init__(self, cards, player_num, pot):
        super().__init__()
        self._cards = cards
        self._player_num = player_num
        self._pot = pot

    def is_successor(self, other):
        if self == other:
            return False
        my_cards = ''.join(map(repr, self._cards))
        other_cards = ''.join(map(repr, other._cards))
        return all((my_cards.startswith(other_cards),
                    self._pot >= other._pot,
                    self._player_num <= other._player_num,))


class GameStack:
    def __init__(self):
        super().__init__()
        self._stack = []

    def add_state(self, state):
        if self._stack and not state.is_successor(self._stack[-1]):
            self._stack = []
        self._stack.append(state)

    @property
    def stack(self):
        return self._stack