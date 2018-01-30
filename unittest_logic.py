import unittest
import logic

class TestBoard(unittest.TestCase):
    
    def test_is_in_mill(self):
        board = logic.Board()
        walter = logic.Player('Walter', 'white')

        board.move_piece(walter, new_field=logic.Field(square_name='outer', index=0, owner=walter))
        board.move_piece(walter, new_field=logic.Field(square_name='outer', index=1, owner=walter))
        board.move_piece(walter, new_field=logic.Field(square_name='outer', index=2, owner=walter))
        
        field = logic.Field('outer', 0, walter)
        self.assertEqual(board.is_in_mill(field), True)
        
        field = logic.Field('outer', 1, walter)
        self.assertEqual(board.is_in_mill(field), True)

        field = logic.Field('outer', 2, walter)
        self.assertEqual(board.is_in_mill(field), True)

        field = logic.Field('mid', 1, walter)
        self.assertEqual(board.is_in_mill(field), False)

    def test_get_allowed_fields(self):
        board = logic.Board()
        walter = logic.Player('Walter', 'white')
        peter = logic.Player('Peter', 'black')

        board.move_piece(walter, new_field=logic.Field(square_name='outer', index=0, owner=walter))
        board.move_piece(walter, new_field=logic.Field(square_name='mid', index=1, owner=walter))
        board.move_piece(walter, new_field=logic.Field(square_name='outer', index=2, owner=walter))
        
        board.move_piece(peter, new_field=logic.Field(square_name='outer', index=1, owner=peter))
        
        field = logic.Field(square_name='mid', index=1, owner=walter)
        result = board.get_allowed_fields(field)

        field = logic.Field(square_name='mid', index=0, owner=None)
        self.assertEqual(result['mid'][0].__eq__(field), True)

        field = logic.Field(square_name='mid', index=2, owner=None)
        self.assertEqual(result['mid'][1].__eq__(field), True)

        field = logic.Field(square_name='inner', index=1, owner=peter)
        self.assertEqual(result['inner'][0].__eq__(field), False)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBoard)
    unittest.TextTestRunner(verbosity=2).run(suite)
    #unittest.main()
