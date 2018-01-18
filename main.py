from collections import namedtuple
from random import choice

SQUARE_NAMES = ('inner', 'mid', 'outer')

MIN_INDEX = 0
MAX_INDEX = 7
SQUARE_INDICES = range(MIN_INDEX, MAX_INDEX + 1)

COLORS = ('white', 'black')

class Field(namedtuple('Field', 'square_name, index, player')):
    def __new__(cls, square_name, index, player=None):
        if square_name not in SQUARE_NAMES:
            raise ValueError('Invalid square name')
        if not MIN_INDEX <= index <= MAX_INDEX:
            raise ValueError('Field index out of range')
        return tuple.__new__(cls, (square_name, index, player))
 
class Board(object):
    def __init__(self):
        self.fields = {
            square: [Field(square, i) for i in SQUARE_INDICES]
            for square in SQUARE_NAMES
        }
        
    def get_all_fields(self, player=None):
        # get all fields (24 pieces) or those of the player
        if not player:
            return self.fields.copy()
        return {
            square: [f for f in self.fields[square] if f.player == player]
            for square in SQUARE_NAMES
        }

    def move_piece(self, player, old_field=None, new_field=None):
        # Get original field to avoid cheating
        new_field = self.fields[new_field.square_name][new_field.index]

        if new_field.player:
            msg = 'New field already owned by {}'
            raise ValueError(msg.format(new_field.player.name))
        new_field = new_field._replace(player=player)
        self.fields[new_field.square_name][new_field.index] = new_field

        # if self.is_in_mill(self.fields, new_field):
    
    def get_allowed_fields(self, field=None):
        # get all unoccupied fields or the neighboring fields from the field
        if field:
            square_fields = self.fields[field.square_name]
            square_index = SQUARE_NAMES.index(field.square_name)
            player = field.player

            candidates = [ self.fields[SQUARE_NAMES[square_index-i]][field.index]
                           for i in (-1,1) if 0 <= square_index-i <= 2]
            candidates.extend([  square_fields[(field.index + i) % 8] for i in (-1, 1)])

            fields = { square: [] for square in SQUARE_NAMES }
            [fields[field.square_name].append(field) for field in candidates if not field.player]
            return { square: fields[square] for square in fields }
        return {
            square: [field for field in self.fields[square] if not field.player]
            for square in SQUARE_NAMES
        }

    def is_in_mill(self, field):
        # check if a mill has been created
        square_fields = self.fields[field.square_name]
        player = field.player

        if (field.index % 2) == 0:
            candidates = [
                [square_fields[(field.index + i) % 8] for i in (0, 1, 2)],
                [square_fields[(field.index - i) % 8] for i in (0, 1, 2)]
            ]
        else:
            candidates = [
                [self.fields[square][field.index] for square in SQUARE_NAMES],
                [square_fields[(field.index + i) % 8] for i in (-1, 0, 1)]
            ]
        for candidate in candidates:
            if all(field.player == player for field in candidate):
                return True
        return False

class Player(object):
    def __init__(self, name, color):
        if color not in COLORS:
            raise ValueError('Invalid color')
        self.name = name
        self.color = color
    
    def make_move(self, board, field):
        board.move_piece(self, new_field=field)

    def __repr__(self):
        return '{}(name={!r}, color={!r})'.format(
            type(self).__name__, self.name, self.color
        )

if __name__  == '__main__':

    board = Board()
    walter = Player('Walter', 'white')
    print(walter)

    field = Field('outer', 4, walter)
    print(field)
    walter.make_move(board, field)
    
    field = Field('outer', 3, walter)
    walter.make_move(board, field)
    print(board.get_allowed_fields(field))
    print(board.get_all_fields(walter))
