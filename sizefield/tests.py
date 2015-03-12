from django.test import TestCase

from .utils import filesizeformat, parse_size
from .templatetags.sizefieldtags import filesize


class ParseRenderTest(TestCase):

    def test_render(self):

        from sizefield import utils
        utils.SIZEFIELD_FORMAT = '{value} {unit}'

        # Usual case
        self.assertEqual('123.0 B', filesizeformat(123))
        self.assertEqual('123.0 B', filesizeformat('123'))
        # Incorrect input
        self.assertRaises(ValueError, filesizeformat, (''))
        self.assertRaises(ValueError, filesizeformat, ('abc'))
        self.assertRaises(ValueError, filesizeformat, ('12 HB'))
        # Units
        self.assertEqual('1000.0 B', filesizeformat(1000))
        self.assertEqual('1023.0 B', filesizeformat(1023))
        self.assertEqual('1.0 KB', filesizeformat(1024))
        self.assertEqual('1.0 MB', filesizeformat(1024 * 1024))
        self.assertEqual('1.0 GB', filesizeformat(1024 * 1024 * 1024))
        self.assertEqual('512.0 KB', filesizeformat(1024 * 1024 * 0.5))
        self.assertEqual('307.2 KB', filesizeformat(1024 * 1024 * 0.3))
        # Decimals
        self.assertEqual('1 KB', filesizeformat(1024, decimals=0))
        self.assertEqual('1.0 KB', filesizeformat(1024, decimals=1))
        self.assertEqual('1.00 KB', filesizeformat(1024, decimals=2))
        self.assertEqual('1.000 KB', filesizeformat(1024, decimals=3))
        self.assertEqual('1.0000 KB', filesizeformat(1024, decimals=4))

        # test SIZEFIELD_FORMAT
        utils.SIZEFIELD_FORMAT = '{value}xxx {unit}'
        self.assertEqual('1xxx KB', filesizeformat(1024, decimals=0))
        self.assertEqual('1.0xxx KB', filesizeformat(1024, decimals=1))
        self.assertEqual('1.00xxx KB', filesizeformat(1024, decimals=2))
        self.assertEqual('1.000xxx KB', filesizeformat(1024, decimals=3))
        self.assertEqual('1.0000xxx KB', filesizeformat(1024, decimals=4))

    def test_parse(self):
        # Usual case
        self.assertEqual(123, parse_size('123'))
        self.assertEqual(123, parse_size('123B'))
        self.assertEqual(123, parse_size('123 B'))
        # Units
        self.assertEqual(1 << 10, parse_size('1KB'))
        self.assertEqual(1 << 20, parse_size('1MB'))
        self.assertEqual(1 << 30, parse_size('1GB'))
        self.assertEqual(1 << 40, parse_size('1TB'))
        self.assertEqual(1 << 50, parse_size('1PB'))
        self.assertEqual(1 << 60, parse_size('1EB'))
        self.assertEqual((1 << 10) * 0.5, parse_size('0.5KB'))
        self.assertEqual((1 << 20) * 0.5, parse_size('0.5MB'))
        self.assertEqual((1 << 30) * 0.5, parse_size('0.5GB'))
        self.assertEqual((1 << 40) * 0.5, parse_size('0.5TB'))
        self.assertEqual((1 << 50) * 0.5, parse_size('0.5PB'))
        self.assertEqual((1 << 60) * 0.5, parse_size('0.5EB'))
        self.assertEqual((1 << 70) * 0.5, parse_size('0.5ZB'))
        self.assertEqual((1 << 80) * 0.5, parse_size('0.5YB'))
        # Case and spaces
        self.assertEqual(1 << 10, parse_size('1Kb'))
        self.assertEqual(1 << 10, parse_size('1kB'))
        self.assertEqual(1 << 10, parse_size('1kb'))
        self.assertEqual(1 << 10, parse_size('1 kb'))
        self.assertEqual(1 << 10, parse_size('1      kb'))
        # Incorrect input
        self.assertRaises(ValueError, parse_size, (''))
        self.assertRaises(ValueError, parse_size, ('abc'))
        self.assertRaises(ValueError, parse_size, ('12 HB'))
        self.assertRaises(ValueError, parse_size, ('12 BB'))
        self.assertRaises(ValueError, parse_size, ('12 BKB'))
        self.assertRaises(ValueError, parse_size, ('12 K'))
        # Already rendered
        self.assertEqual(123, parse_size(123))


class TemplateTagTest(TestCase):

    def test_tag_should_support_none_values(self):
        self.assertEqual('', filesize(None))
