import unittest
import finder

class TestFinder(unittest.TestCase):

    def setUp(self):
        self.instance = finder.Finder('SMario.sfc', 'elcome')


    def test_translateStringToHexadecimalArray(self):
        expected = ['65', '6c', '63', '6f', '6d', '65']
        arr = self.instance.translateStringToHexadecimalArray()

        self.assertEqual(arr, expected)

    def test_absoluteDifferenceBetweenTwoHexadecimals(self):
        expected = 1
        a = self.instance.absoluteDifferenceBetweenTwoHexadecimals('0', '1')
        b = self.instance.absoluteDifferenceBetweenTwoHexadecimals('1', '0')

        self.assertEqual(a, expected)
        self.assertEqual(b, expected)

    def test_findLastOccourInAray(self):
        response = self.instance.findLastOccourInAray([1, 2, 3, 4], [3, 4])
        self.assertEqual(2, response)

        response = self.instance.findLastOccourInAray([1, 2, 3, 4, 0, 1, 2, 3, 3, 4, 8, 5], [3, 4])
        self.assertEqual(8, response)

    def test_getRelativeValuesByString(self):
        expected = [7, 9, 12, 2, 8]
        response = self.instance.getRelativeValuesByString()

        self.assertEqual(expected, response)

if __name__ == '__main__':
    unittest.main()