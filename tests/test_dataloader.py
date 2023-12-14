from data.loader import fetch_dataloader
import unittest

class TestDataLoader(unittest.TestCase):

    def setUp(self):
        # Code to run before each test
        self.dls = fetch_dataloader()

    def tearDown(self):
        # Code to run after each test
        pass

    def test_dataloaders(self):
        for dl in self.dls:
          print(dl)
          print(dl[0])
          self.assertEqual(len(dl), 1)

def main():
    unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestDataLoader))
if __name__ == "__main__":
    main()
