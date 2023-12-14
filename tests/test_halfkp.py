from libs.halfkp_lib import Half_KP_Converter
import unittest
import torch

class TestKpConverter(unittest.TestCase):

    fen_strings = [
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    "k1K5/8/8/8/8/8/8/8 w",
    "k1K5/8/8/8/8/8/8/8 b",
    "k1K5/8/8/8/8/8/8/7r b",
    "k1K5/8/8/8/8/8/8/7R w",
    "k1K5/8/8/8/8/8/8/7q w",
    "k1K5/8/8/8/8/8/8/7Q b",
    "k1K5/8/8/8/8/8/8/7n w",
    "k1K5/8/8/8/8/8/8/7N b",
    "k1K5/8/8/8/8/8/8/7b w",
    "k1K5/8/8/8/8/8/8/7B b"

    ]

    def setUp(self):
        # Code to run before each test
        self.hkp_conv = Half_KP_Converter()

    def tearDown(self):
        # Code to run after each test
        pass

    def test_index(self):
        fen = "k7/8/8/8/8/8/P7/K7 w"
        hkp_tensor = self.hkp_conv.fen2tensor(fen)
        self.assertEqual(hkp_tensor[72].item(), 1)
        fen = "k7/8/8/8/8/8/p7/K7 w"
        hkp_tensor = self.hkp_conv.fen2tensor(fen)
        self.assertEqual(hkp_tensor[8].item(), 1)
        fen = "k7/8/8/8/8/8/P7/K7 b"
        hkp_tensor = self.hkp_conv.fen2tensor(fen)
        self.assertEqual(hkp_tensor[72 + 40960].item(), 1)
        fen = "k7/8/8/8/8/8/p7/K7 b"
        hkp_tensor = self.hkp_conv.fen2tensor(fen)
        self.assertEqual(hkp_tensor[8 + 40960].item(), 1)
        fen = "k5KQ/8/8/8/8/8/8/8 w"
        hkp_tensor = self.hkp_conv.fen2tensor(fen)
        self.assertEqual(hkp_tensor[63+(9+62*10)*64].item(), 1)
        fen = "k4K1Q/8/8/8/8/8/8/8 w"
        hkp_tensor = self.hkp_conv.fen2tensor(fen)
        self.assertEqual(hkp_tensor[63+(9+61*10)*64].item(), 1)
        fen = "6QK/8/8/8/8/8/8/k7 w"
        hkp_tensor = self.hkp_conv.fen2tensor(fen)
        self.assertEqual(hkp_tensor[62+(9+63*10)*64].item(), 1)

    def test_fen(self):
      for index, fen in enumerate(self.fen_strings):

        hkp_tensor = self.hkp_conv.fen2tensor(fen)

        self.assertEqual(hkp_tensor.shape, torch.Size([81920]))
        self.assertEqual(hkp_tensor.dtype, torch.int8)

        num_non_zeros = torch.sum(hkp_tensor != 0).item()

        if index < 1:
          self.assertEqual(num_non_zeros, 60)
        elif index < 3:
          self.assertEqual(num_non_zeros, 0)
        elif index < 11:
          self.assertEqual(num_non_zeros, 2)

def main():
    unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestKpConverter))
if __name__ == "__main__":
    main()
