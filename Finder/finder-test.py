import unittest
import finder

class TestFinder(unittest.TestCase):

    def setUp(self):
        self.instance = finder.Finder('SMario.sfc', 'elcome')


    def test_translateStringToHexadecimalArray(self):
        expected = ['65', '6c', '63', '6f', '6d', '65']
        arr = self.instance.translateStringToHexadecimalArray()

        self.assertEqual(arr, expected)

    def test_getRelativeValuesByString(self):
        self.assertEqual([7, 9, 12, 2, 8], self.instance.getRelativeValuesByString())

    def test_absoluteDifferenceBetweenTwoHexadecimals(self):
        expected = 1
        a = self.instance.absoluteDifferenceBetweenTwoHexadecimals('0', '1')
        b = self.instance.absoluteDifferenceBetweenTwoHexadecimals('1', '0')

        self.assertEqual(a, expected)
        self.assertEqual(b, expected)

if __name__ == '__main__':
    unittest.main()