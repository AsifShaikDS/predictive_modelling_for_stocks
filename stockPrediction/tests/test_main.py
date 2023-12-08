import unittest

# Function to be tested
def add_numbers(a, b):
    return a + b

# Test case class
class TestAddNumbers(unittest.TestCase):
    def test_add_numbers(self):
        # Test case 1: Positive numbers
        result = add_numbers(2, 3)
        self.assertEqual(result, 5)

        # Test case 2: Negative numbers
        result = add_numbers(-2, -3)
        self.assertEqual(result, -5)

        # Test case 3: Zero
        result = add_numbers(0, 0)
        self.assertEqual(result, 0)

        # Test case 4: One positive, one negative
        result = add_numbers(5, -3)
        self.assertEqual(result, 2)

if __name__ == '__main__':
    unittest.main()
