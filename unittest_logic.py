import unittest
import logic

class TestBoard(unittest.TestCase):
    
    def test_is_in_mill(self):
        board = logic.Board()
        walter = logic.Player('Walter', 'white')

        for i in in range(3):
            board.move_piece(walter, new_field=logic.Field('outer', i, walter))

        for field in board.get_all_fields(walter)['outer']:
            self.assertTrue(board.is_in_mill(field))
        
        field = logic.Field('mid', 1, walter)
        self.assertFalse(board.is_in_mill(field))

    def test_get_allowed_fields(self):
        board = logic.Board()
        walter = logic.Player('Walter', 'white')
        peter = logic.Player('Peter', 'black')

        for square, i in [('outer', 0), ('mid', 1), ('outer', 2)]:
            board.move_piece(walter, new_field=logic.Field(square, i, walter))
        board.move_piece(peter, new_field=logic.Field('outer', 1, peter))
        
        allowed = board.get_allowed_fields(logic.Field('mid', 1, walter))
        
        self.assertIn(logic.Field('mid', 0, walter), allowed['mid'])
        self.assertIn(logic.Field('mid', 2, walter), allowed['mid'])
        self.assertNotIn(logic.Field('inner', 1, peter), allowed['inner'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
