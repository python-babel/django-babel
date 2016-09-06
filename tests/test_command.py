import os

from django.core.management import call_command

TEST_LOCALE_DIR = os.path.join(
    os.path.dirname(__file__),
    'locale',
)


def test_babel_compilemessages():
    call_command(
        'babel',
        'compilemessages',
        '-l', 'fi',
    )
    # Assert that the .mo file was created by attempting to delete it.
    os.unlink(
        os.path.join(TEST_LOCALE_DIR, 'fi', 'LC_MESSAGES', 'django.mo')
    )


def test_babel_makemessages():
    call_command(
        'babel',
        'makemessages',
        '-l', 'en',
        '-F', os.path.join(os.path.dirname(__file__), 'babel.cfg'),
    )
    # See that the expected files get populated with the discovered message
    for path in [
        os.path.join(TEST_LOCALE_DIR, 'django.pot'),
        os.path.join(TEST_LOCALE_DIR, 'en', 'LC_MESSAGES', 'django.po'),
    ]:
        with open(path) as infp:
            assert '"This could be translated."' in infp.read()
        os.unlink(path)  # clean up
