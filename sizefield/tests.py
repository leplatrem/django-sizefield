from django.test import TestCase

from sizefield import render_size, parse_size


class ParseRenderTest(TestCase):
    def test_render(self):
        # Usual case
        self.assertEqual('123.0B', render_size(123))
        self.assertEqual('123.0B', render_size('123'))
        # Incorrect input
        self.assertRaises(ValueError, render_size, (''))
        self.assertRaises(ValueError, render_size, ('abc'))
        self.assertRaises(ValueError, render_size, ('12 HB'))
        # Already rendered
        self.assertEqual('1.0KB', render_size('1.0KB'))
        self.assertEqual('1.0KB', render_size('1 KB'))
        # Units
        self.assertEqual('1000.0B', render_size(1000))
        self.assertEqual('1023.0B', render_size(1023))
        self.assertEqual('1.0KB', render_size(1024))
        self.assertEqual('1.0MB', render_size('1024 KB'))
        self.assertEqual('1.0GB', render_size('1048576 KB'))
        self.assertEqual('512.0KB', render_size('0.5 MB'))
        self.assertEqual('307.2KB', render_size('0.3 MB'))
        # Decimals
        self.assertEqual('307KB', render_size('0.3 MB', decimals=0))
        self.assertEqual('307.2KB', render_size('0.3 MB', decimals=1))
        self.assertEqual('307.20KB', render_size('0.3 MB', decimals=2))
        self.assertEqual('307.199KB', render_size('0.3 MB', decimals=3))
        self.assertEqual('307.1992KB', render_size('0.3 MB', decimals=4))

    def test_parse(self):
        # Usual case
        self.assertEqual(123, parse_size('123'))
        self.assertEqual(123, parse_size('123B'))
        self.assertEqual(123, parse_size('123 B'))
        # Incorrect input
        self.assertRaises(ValueError, parse_size, (''))
        self.assertRaises(ValueError, parse_size, ('abc'))
        self.assertRaises(ValueError, parse_size, ('12 HB'))
        self.assertRaises(ValueError, parse_size, ('12 BB'))
        self.assertRaises(ValueError, parse_size, ('12 BKB'))
        self.assertRaises(ValueError, parse_size, ('12 K'))
        # Already rendered
        self.assertEqual(123, parse_size(123))

