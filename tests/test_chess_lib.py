from libs.chess_lib import Chess_Lib
import unittest

class TestChessLib(unittest.TestCase):

    def setUp(self):
        # Code to run before each test
        pass

    def tearDown(self):
        # Code to run after each test
        pass

    def test_eval(self):
        self.assertEqual(Chess_Lib.get_eval_value(1.0,0), 100)
        self.assertEqual(Chess_Lib.get_eval_value(-2.13,0), -213)
        self.assertEqual(Chess_Lib.get_eval_value(0.0,0), 0)
        self.assertEqual(Chess_Lib.get_eval_value(1.0,1), 1000 * 2 + 99 * 1000)
        self.assertEqual(Chess_Lib.get_eval_value(-2.13,-2), -(1000 * 2 + 98 * 1000))
        self.assertEqual(Chess_Lib.get_eval_value(0.0,101), 1000 * 2 + 1 * 1000)
        self.assertEqual(Chess_Lib.MAX_EVAL, 1000 * 2 + 100 * 1000)

def main():
    unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestChessLib))

if __name__ == "__main__":
    main()