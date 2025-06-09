import doctest
import unittest
import samplelayers
x = 0
y = 0
z = 0

class TestA(unittest.TestCase):

    def setUp(self):
        global x
        x = 1

    def tearDown(self):
        global x
        x = 0

    def test_x1(self):
        self.assertEqual(x, 1)

    def test_y0(self):
        self.assertEqual(y, 0)

    def test_z0(self):
        self.assertEqual(z, 0)

class TestA2(unittest.TestCase):
    level = 2

    def setUp(self):
        global x
        x = 1

    def tearDown(self):
        global x
        x = 0

    def test_x1(self):
        self.assertEqual(x, 1)

    def test_y0(self):
        self.assertEqual(y, 0)

    def test_z0(self):
        self.assertEqual(z, 0)

class TestB(unittest.TestCase):

    def setUp(self):
        global y
        y = 1

    def tearDown(self):
        global y
        y = 0

    def test_y1(self):
        self.assertEqual(y, 1)

    def test_x0(self):
        self.assertEqual(x, 0)

    def test_z0(self):
        self.assertEqual(z, 0)

class TestNotMuch(unittest.TestCase):

    def test_1(self):
        pass

    def test_2(self):
        pass

    def test_3(self):
        pass

def setUp(test):
    test.globs['z'] = 1

def test_y0(self):
    """
    >>> y = 0
    >>> y
    0
    """

def test_x0(self):
    """
    >>> x = 0
    >>> x
    0
    """

def test_z1(self):
    """
    >>> z
    1
    """

class Layered:
    layer = 'samplelayers.Layer1'
    layerv = '1'
    layerx = '0'

class TestA1(unittest.TestCase, Layered):

    def setUp(self):
        global x
        x = 1

    def tearDown(self):
        global x
        x = 0

    def test_x1(self):
        self.assertEqual(x, 1)
        self.assertEqual(samplelayers.layer, self.layerv)
        self.assertEqual(samplelayers.layerx, self.layerx)

    def test_y0(self):
        self.assertEqual(y, 0)
        self.assertEqual(samplelayers.layer, self.layerv)
        self.assertEqual(samplelayers.layerx, self.layerx)

    def test_z0(self):
        self.assertEqual(z, 0)
        self.assertEqual(samplelayers.layer, self.layerv)
        self.assertEqual(samplelayers.layerx, self.layerx)

class TestB1(unittest.TestCase, Layered):

    def setUp(self):
        global y
        y = 1

    def tearDown(self):
        global y
        y = 0

    def test_y1(self):
        self.assertEqual(y, 1)
        self.assertEqual(samplelayers.layer, self.layerv)
        self.assertEqual(samplelayers.layerx, self.layerx)

    def test_x0(self):
        self.assertEqual(x, 0)
        self.assertEqual(samplelayers.layer, self.layerv)
        self.assertEqual(samplelayers.layerx, self.layerx)

    def test_z0(self):
        self.assertEqual(z, 0)
        self.assertEqual(samplelayers.layer, self.layerv)
        self.assertEqual(samplelayers.layerx, self.layerx)

class TestNotMuch1(unittest.TestCase, Layered):

    def test_1(self):
        self.assertEqual(samplelayers.layer, self.layerv)
        self.assertEqual(samplelayers.layerx, self.layerx)

    def test_2(self):
        self.assertEqual(samplelayers.layer, self.layerv)
        self.assertEqual(samplelayers.layerx, self.layerx)

    def test_3(self):
        self.assertEqual(samplelayers.layer, self.layerv)
        self.assertEqual(samplelayers.layerx, self.layerx)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestA))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestA2))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestB))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestNotMuch))
    suite.addTest(doctest.DocTestSuite(setUp=setUp))
    suite.addTest(doctest.DocFileSuite('sampletests.rst', setUp=setUp))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestA1))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestB1))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestNotMuch1))
    return suite