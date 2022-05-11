import unittest
from AA import sbst


class AATest(unittest.TestCase):
    def setUp(self):
        self.AA = sbst()

    def test_addval(self):
        self.AA.add(12)
        self.assertEqual(self.AA.root.val, 12)

    def test_addval_float(self):
        self.AA.add(12.3)
        self.assertEqual(self.AA.root.val, 12.3)

    def test_addval_mul(self):
        self.AA.add(12)
        self.AA.add(23)
        self.assertEqual(self.AA.root.val, 12)
        self.assertEqual(self.AA.root.right.val, 23)

    def test_addval_mul_plus(self):
        self.AA.add(12)
        self.AA.add(23)
        self.AA.add(67)
        self.AA.add(25)
        self.AA.add(34)
        self.AA.add(45)
        self.AA.add(14)
        self.AA.add(9)
        self.AA.add(8)
        self.AA.add(7)
        self.assertEqual(self.AA.root.val, 23)
        self.assertEqual(self.AA.root.left.val, 8)
        self.assertEqual(self.AA.root.right.val, 34)
        self.assertEqual(self.AA.root.left.left.val, 7)
        self.assertEqual(self.AA.root.left.right.val, 12)
        self.assertEqual(self.AA.root.left.right.left.val, 9)
        self.assertEqual(self.AA.root.left.right.right.val, 14)
        self.assertEqual(self.AA.root.right.left.val, 25)
        self.assertEqual(self.AA.root.right.right.val, 45)
        self.assertEqual(self.AA.root.right.right.right.val, 67)
        self.assertEqual(self.AA.root.right.right.val, 45)

    def test_remove_no_val(self):
        self.AA.remove(23)
        self.assertEqual(self.AA.root, None)

    def test_remove_val(self):
        self.AA.add(12)
        self.AA.add(23)
        self.AA.remove(23)
        self.assertEqual(self.AA.root.val, 12)

    def test_remove_val_more(self):
        self.AA.add(12)
        self.AA.add(23)
        self.AA.add(67)
        self.AA.add(25)
        self.AA.add(34)
        self.AA.add(45)
        self.AA.add(14)
        self.AA.add(9)
        self.AA.add(8)
        self.AA.add(7)
        self.AA.add(1)
        self.AA.remove(1)
        self.assertEqual(self.AA.root.val, 23)
        self.assertEqual(self.AA.root.left.val, 8)
        self.assertEqual(self.AA.root.right.val, 34)
        self.assertEqual(self.AA.root.left.left.val, 7)
        self.assertEqual(self.AA.root.left.right.val, 12)
        self.assertEqual(self.AA.root.left.right.left.val, 9)
        self.assertEqual(self.AA.root.left.right.right.val, 14)
        self.assertEqual(self.AA.root.right.left.val, 25)
        self.assertEqual(self.AA.root.right.right.val, 45)
        self.assertEqual(self.AA.root.right.right.right.val, 67)
        self.assertEqual(self.AA.root.right.right.val, 45)

    def test_remove_val_more_then_2(self):
        self.AA.add(12)
        self.AA.add(23)
        self.AA.add(24)
        self.AA.remove(23)
        self.assertEqual(self.AA.root.val, 12)
        self.assertEqual(self.AA.root.right.val, 24)

    def test_min(self):
        self.AA.add(12)
        self.AA.add(23)
        self.AA.add(34)
        self.AA.min()
        self.assertEqual(self.AA.min(), 12)

    def test_add_from(self):
        self.AA.addfrom(i ** 3 for i in range(2, 4))
        self.assertEqual(self.AA.root.val, 8)
        self.assertEqual(self.AA.root.right.val, 27)

    def test_skew_and_split(self):
        self.AA.add(12)
        self.AA.add(165)
        self.AA.add(13)
        self.assertEqual(self.AA.root.val, 13)
        self.assertEqual(self.AA.root.right.val, 165)
        self.assertEqual(self.AA.root.left.val, 12)

if __name__ == '__main__':
    pass
