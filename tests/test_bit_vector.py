from libs.bit_vector import BitVector
import unittest
import torch

class TestBitVector(unittest.TestCase):

    def setUp(self):
        # Code to run before each test
        pass

    def tearDown(self):
        # Code to run after each test
        pass

    def test64(self):
        self.bv64 = BitVector(64)
        self.bv64.set_bit(1)
        self.bv64.set_bit(0)
        self.bv64.set_bit(63)
        self.assertEqual(self.bv64.get_non_zeros(), [0,1,63])
        self.assertEqual(str(self.bv64),"1100000000000000000000000000000000000000000000000000000000000001")
        left = str(self.bv64.get_range(0,31))
        right = str(self.bv64.get_range(32,63))
        self.assertEqual(str(self.bv64), left + right)
        self.bv64.clear_bit(1)
        self.bv64.clear_bit(2)
        self.assertEqual(str(self.bv64),"1000000000000000000000000000000000000000000000000000000000000001")
        self.bv64.set_bit(62)
        self.bv64.set_bit(61)
        self.bv64.set_bit(60)
        self.bv64.set_bit(59)
        self.assertEqual(self.bv64.get_range(0,31).to_int(), 2147483648)
        self.assertEqual(self.bv64.get_range(32,63).to_int(), 31)

    def testHalfKP(self):
        self.bvhkp = BitVector(40960)
        self.bvhkp.set_bit(1)
        self.bvhkp.set_bit(0)
        self.bvhkp.set_bit(409)
        self.assertEqual(self.bvhkp.to_tensor().size(), torch.Size([40960]))
        self.assertEqual(self.bvhkp.to_tensor().dtype, torch.int8)
        left = str(self.bvhkp.get_range(0,20480))
        right = str(self.bvhkp.get_range(20481,40959))
        self.assertEqual(str(self.bvhkp), left + right)

def main():
    unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestBitVector))

if __name__ == "__main__":
    main()