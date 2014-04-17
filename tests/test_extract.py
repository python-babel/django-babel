#-*- coding: utf-8 -*-
import codecs
import sys
import unittest

from django_babel.extract import extract_django
from babel.messages import extract
from babel._compat import BytesIO, StringIO


class ExtractDjangoTestCase(unittest.TestCase):
    # TODO: translator comments are not yet supported!

    def test_extract_simple(self):
        buf = BytesIO(b'{% trans "Bunny" %}')
        messages = list(extract_django(buf, extract.DEFAULT_KEYWORDS.keys(), [], {}))
        self.assertEqual([(1, None, u'Bunny', [])], messages)

    def test_extract_var(self):
        buf = BytesIO(b'{% blocktrans %}{{ anton }}{% endblocktrans %}')
        messages = list(extract_django(buf, extract.DEFAULT_KEYWORDS.keys(), [], {}))
        self.assertEqual([(1, None, u'%(anton)s', [])], messages)

    def test_extract_filter_with_filter(self):
        buf = BytesIO(b'{% blocktrans with berta=anton|lower %}{{ berta }}{% endblocktrans %}')
        messages = list(extract_django(buf, extract.DEFAULT_KEYWORDS.keys(), [], {}))
        self.assertEqual([(1, None, u'%(berta)s', [])], messages)

    def test_extract_with_interpolation(self):
        buf = BytesIO(b'{% blocktrans %}xxx{{ anton }}xxx{% endblocktrans %}')
        messages = list(extract_django(buf, extract.DEFAULT_KEYWORDS.keys(), [], {}))
        self.assertEqual([(1, None, u'xxx%(anton)sxxx', [])], messages)

    def test_extract_unicode(self):
        buf = BytesIO(b'{% trans "@ſðæ314“ſſ¶ÐĐÞ→SÆ^ĸŁ" %}')
        messages = list(extract_django(buf, extract.DEFAULT_KEYWORDS.keys(), [], {}))
        self.assertEqual([(1, None, u'@ſðæ314“ſſ¶ÐĐÞ→SÆ^ĸŁ', [])], messages)

    def test_extract_unicode_blocktrans(self):
        buf = BytesIO(b'{% blocktrans %}@ſðæ314“ſſ¶ÐĐÞ→SÆ^ĸŁ{% endblocktrans %}')
        messages = list(extract_django(buf, extract.DEFAULT_KEYWORDS.keys(), [], {}))
        self.assertEqual([(1, None, u'@ſðæ314“ſſ¶ÐĐÞ→SÆ^ĸŁ', [])], messages)

    # TODO: Yet expected to not extract the comments.
    def test_extract_ignored_comment(self):
        buf = BytesIO(b'{# ignored comment #1 #}{% trans "Translatable literal #9a" %}')
        messages = list(extract_django(buf, extract.DEFAULT_KEYWORDS.keys(), [], {}))
        self.assertEqual([(1, None, u'Translatable literal #9a', [])], messages)

    def test_extract_ignored_comment2(self):
        buf = BytesIO(b'{# Translators: ignored i18n comment #1 #}{% trans "Translatable literal #9a" %}')
        messages = list(extract_django(buf, extract.DEFAULT_KEYWORDS.keys(), [], {}))
        self.assertEqual([(1, None, u'Translatable literal #9a', [])], messages)

    def test_extract_valid_comment(self):
        buf = BytesIO(b'{# ignored comment #6 #}{% trans "Translatable literal #9h" %}{# Translators: valid i18n comment #7 #}')
        messages = list(extract_django(buf, extract.DEFAULT_KEYWORDS.keys(), [], {}))
        self.assertEqual([(1, None, u'Translatable literal #9h', [])], messages)

    def test_extract_singular_form(self):
        buf = BytesIO(b'{% blocktrans count counter=number %}singular{% plural %}{{ counter }} plural{% endblocktrans %}')
        messages = list(extract_django(buf, extract.DEFAULT_KEYWORDS.keys(), [], {}))
        self.assertEqual([(1, 'ngettext', (u'singular', u'%(counter)s plural'), [])], messages)
