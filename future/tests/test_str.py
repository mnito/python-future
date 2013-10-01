# -*- coding: utf-8 -*-
"""
Tests for the backported class:`str` class.
"""

from __future__ import absolute_import, unicode_literals, print_function
from future.builtins import *
from future import utils

import unittest

TEST_UNICODE_STR = u'ℝεα∂@ßʟ℮ ☂ℯṧт υηḯ¢☺ḓ℮'


class TestStr(unittest.TestCase):
    def test_str(self):
        self.assertIsNot(str, bytes)            # Py2: assertIsNot only in 2.7
        self.assertEqual(str('blah'), u'blah')  # u'' prefix: Py3.3 and Py2 only
        self.assertEqual(str(b'1234'), "b'1234'")

    def test_str_encode_utf8(self):
        b = str(TEST_UNICODE_STR).encode('utf-8')
        self.assertTrue(isinstance(b, bytes))
        self.assertFalse(isinstance(b, str))
        s = b.decode('utf-8')
        self.assertTrue(isinstance(s, str))
        self.assertEqual(s, TEST_UNICODE_STR)

    def test_str_encode_decode_big5(self):
        a = u'Unicode string: \u5b54\u5b50'
        self.assertEqual(str(a), a.encode('big5').decode('big5'))

    def test_str_empty(self):
        """
        str() -> u''
        """
        self.assertEqual(str(), u'')

    def test_str_iterable_of_ints(self):
        self.assertEqual(str([65, 66, 67]), '[65, 66, 67]')
        self.assertNotEqual(str([65, 66, 67]), 'ABC')

    def test_str_str(self):
        self.assertEqual(str('ABC'), u'ABC')
        self.assertEqual(str('ABC'), 'ABC')

    def test_str_is_str(self):
        s = str(u'ABC')
        self.assertTrue(str(s) is s)
        self.assertEqual(repr(str(s)), "'ABC'")

    def test_str_fromhex(self):
        self.assertFalse(hasattr(str, 'fromhex'))

    def test_isinstance_str(self):
        self.assertTrue(isinstance(str('blah'), str))

    def test_str_getitem(self):
        s = str('ABCD')
        self.assertNotEqual(s[0], 65)
        self.assertEqual(s[0], 'A')
        self.assertEqual(s[-1], 'D')
        self.assertEqual(s[0:1], 'A')
        self.assertEqual(s[:], u'ABCD')

    @unittest.expectedFailure
    def test_u_literal_creates_newstr_object(self):
        """
        It would nice if the u'' or '' literal syntax could be coaxed
        into producing our new str objects somehow ...
        """
        s = u'ABCD'
        self.assertTrue(isinstance(s, str))
        self.assertFalse(repr(b).startswith('b'))

    def test_repr(self):
        s = str('ABCD')
        self.assertFalse(repr(s).startswith('b'))

    def test_str(self):
        b = str('ABCD')
        self.assertTrue(str(b), 'ABCD')

    def test_str_setitem(self):
        s = 'ABCD'
        with self.assertRaises(TypeError):
            s[0] = b'B'

    def test_str_iteration(self):
        s = str('ABCD')
        for item in s:
            self.assertFalse(isinstance(item, int))
            self.assertTrue(isinstance(item, str))
        self.assertNotEqual(list(s), [65, 66, 67, 68])
        self.assertEqual(list(s), ['A', 'B', 'C', 'D'])

    def test_str_plus_bytes(self):
        s = str(u'ABCD')
        b = b'EFGH'
        with self.assertRaises(TypeError):
            s + b
        # str objects don't have an __radd__ method, so the following
        # does not raise a TypeError. Is this a problem?
        # with self.assertRaises(TypeError):
        #     b + s

        # Now with our custom bytes object:
        b2 = bytes(b'EFGH')
        with self.assertRaises(TypeError):
            s + b2
        with self.assertRaises(TypeError):
            b2 + s

    def test_str_plus_str(self):
        s1 = str('ABCD')
        s2 = s1 + s1
        self.assertEqual(s2, u'ABCDABCD')
        self.assertTrue(isinstance(s2, str))

        s3 = s1 + u'ZYXW'
        self.assertEqual(s3, 'ABCDZYXW')
        self.assertTrue(isinstance(s3, str))

        s4 = 'ZYXW' + s1
        self.assertEqual(s4, 'ZYXWABCD')
        # str objects don't have an __radd__ method, so the following is
        # not True. Is this a problem?
        # self.assertTrue(isinstance(s4, str))

    def test_str_join_str(self):
        s = str(' * ')
        strings = ['AB', 'EFGH', 'IJKL', TEST_UNICODE_STR]
        result = s.join(strings)
        self.assertEqual(result, 'AB * EFGH * IJKL * ' + TEST_UNICODE_STR)
        self.assertTrue(isinstance(result, str))

    def test_str_join_bytes(self):
        s = str('ABCD')
        byte_strings = [b'EFGH', u'IJKL']
        with self.assertRaises(TypeError):
            s.join(byte_strings)

    def test_str_replace(self):
        s = str('ABCD')
        c = s.replace('A', 'F')
        self.assertEqual(c, 'FBCD')
        self.assertTrue(isinstance(c, str))

        with self.assertRaises(TypeError):
            s.replace(b'A', u'F')
        with self.assertRaises(TypeError):
            s.replace(u'A', b'F')

    def test_str_partition(self):
        s1 = str('ABCD')
        parts = s1.partition('B')
        self.assertEqual(parts, ('A', 'B', 'CD'))
        self.assertTrue(all([isinstance(p, str) for p in parts]))

        s2 = str('ABCDABCD')
        parts = s2.partition('B')
        self.assertEqual(parts, ('A', 'B', 'CDABCD'))

    def test_str_rpartition(self):
        s2 = str('ABCDABCD')
        parts = s2.rpartition('B')
        self.assertEqual(parts, ('ABCDA', 'B', 'CD'))
        self.assertTrue(all([isinstance(p, str) for p in parts]))

    def test_str_contains_something(self):
        s = str('ABCD')
        self.assertTrue('A' in s)
        with self.assertRaises(TypeError):
            b'A' in s                  
        with self.assertRaises(TypeError):
            65 in s                                 # unlike bytes

        self.assertTrue('AB' in s)
        self.assertFalse(str([65, 66]) in s)        # unlike bytes
        self.assertFalse('AC' in s)
        self.assertFalse('Z' in s)

    def test_str_index(self):
        s = str('ABCD')
        self.assertEqual(s.index('B'), 1)
        with self.assertRaises(TypeError):
            s.index(67)
        with self.assertRaises(TypeError):
            s.index(b'C')

    def test_startswith(self):
        s = str('abcd')
        self.assertTrue(s.startswith('a'))
        self.assertTrue(s.startswith(('a', 'd')))
        self.assertTrue(s.startswith(str('ab')))
        with self.assertRaises(TypeError) as cm:
            s.startswith(b'A')
        with self.assertRaises(TypeError) as cm:
            s.startswith((b'A', b'B'))
        with self.assertRaises(TypeError) as cm:
            s.startswith(65)

    def test_endswith(self):
        s = str('abcd')
        self.assertTrue(s.endswith('d'))
        self.assertTrue(s.endswith(('b', 'd')))
        self.assertTrue(s.endswith(str('cd')))
        self.assertFalse(s.endswith(('A', 'B')))

        with self.assertRaises(TypeError) as cm:
            s.endswith(65)
        with self.assertRaises(TypeError) as cm:
            s.endswith([b'D'])

    def test_split(self):
        s = str('ABCD')
        self.assertEqual(s.split('B'), ['A', 'CD'])
        with self.assertRaises(TypeError) as cm:
            s.split(b'B')

    def test_rsplit(self):
        s = str('ABCD')
        self.assertEqual(s.rsplit('B'), ['A', 'CD'])
        with self.assertRaises(TypeError) as cm:
            s.rsplit(b'B')

    def test_eq_bytes(self):
        s = str('ABCD')
        b = bytes(b'ABCD')
        self.assertNotEqual(s, b)
        self.assertNotEqual(str(''), bytes(b''))
        native_s = 'ABCD'
        self.assertNotEqual(b, native_s)
        # Fails:
        # self.assertNotEqual(native_s, b)
        native_b = b'ABCD'
        self.assertNotEqual(native_b, s)
        self.assertNotEqual(s, native_b)

    def test_eq(self):
        s = str('ABCD')
        self.assertEqual('ABCD', s)
        self.assertEqual(s, 'ABCD')
        self.assertEqual(s, s)
        self.assertTrue(u'ABCD' == s)
        self.assertFalse(b'ABCD' == s)
        self.assertFalse(bytes(b'ABCD') == s)

    def test_ne(self):
        s = str('ABCD')
        self.assertNotEqual('A', s)
        self.assertNotEqual(s, 'A')
        self.assertNotEqual(s, 5)
        self.assertNotEqual(2.7, s)
        self.assertNotEqual(s, ['A', 'B', 'C', 'D'])
        self.assertTrue(b'ABCD' != s)
        self.assertTrue(bytes(b'ABCD') != s)


if __name__ == '__main__':
    unittest.main()
