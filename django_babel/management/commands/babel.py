#-*- coding: utf-8 -*-
import os
from distutils.dist import Distribution
from optparse import make_option
from subprocess import call

from django.core.management.base import LabelCommand, CommandError
from django.conf import settings


class Command(LabelCommand):

    args = '[makemessages] [compilemessages]'

    option_list = LabelCommand.option_list + (
        make_option('--locale', '-l', default=None, dest='locale', action='append',
            help='Creates or updates the message files for the given locale(s) (e.g. pt_BR). '
                 'Can be used multiple times.'),
        make_option('--domain', '-d', default='django', dest='domain',
            help='The domain of the message files (default: "django").'),
        make_option('--mapping-file', '-F', default=None, dest='mapping_file',
            help='Mapping file')
    )

    def handle_label(self, command, **options):
        if command not in ('makemessages', 'compilemessages'):
            raise CommandError("You must either apply 'makemessages' or 'compilemessages'")

        if command == 'makemessages':
            self.handle_makemessages(**options)
        if command == 'compilemessages':
            self.handle_compilemessages(**options)

    def handle_makemessages(self, **options):
        locale_paths = list(settings.LOCALE_PATHS)
        domain = options.pop('domain')
        locales = options.pop('locale')

        # support for mapping file specification via setup.cfg
        # TODO: Try to support all possible options.
        distribution = Distribution()
        distribution.parse_config_files(distribution.find_config_files())

        mapping_file = options.pop('mapping_file', None)
        if mapping_file is None and 'extract_messages' in distribution.command_options:
            opts = distribution.command_options['extract_messages']
            try:
                mapping_file = opts.get('mapping_file', ())[1]
            except IndexError:
                mapping_file = None

        for path in locale_paths:
            potfile = os.path.join(path, '%s.pot' % domain)
            if not os.path.exists(potfile):
                continue

            cmd = ['pybabel', 'extract', '-o',
                   os.path.join(path, '%s.pot' % domain)]

            if mapping_file is not None:
                cmd.extend(['-F', mapping_file])

            cmd.append(os.path.dirname(path))

            print cmd
            call(cmd)

            for locale in locales:
                cmd = ['pybabel', 'update', '-D', domain,
                      '-i', os.path.join(path, '%s.pot' % domain),
                      '-d', path,
                      '-l', locale]
                print cmd
                call(cmd)

    def handle_compilemessages(self, **options):
        locale_paths = list(settings.LOCALE_PATHS)
        domain = options.pop('domain')
        locales = options.pop('locale')

        for path in locale_paths:
            for locale in locales:
                po_file = os.path.join(path, locale, 'LC_MESSAGES', domain + '.po')
                if os.path.exists(po_file):
                    cmd = ['pybabel', 'compile', '-D', domain, '-d', path, '-l', locale]
                    call(cmd)