# Tools for using Babel with Django

This package contains various utilities for integration of [Babel][] into the
[Django][] web framework:

 * A message extraction plugin for Django templates.
 * A middleware class that adds the Babel `Locale` object to requests.
 * A set of template tags for date and number formatting.


## Extracting Messages

Babel provides a message extraction framework similar to GNU `xgettext`, but
more extensible and geared towards Python applications. While Django does
provide [wrapper scripts][Django_i18n] for making the use of `xgettext` more
convenient, the extraction functionality is rather limited. For example, you
can't use template files with an extension other than `.html`, and everything
needs to be in your project package directory.

### Extraction Method Mapping

So `django-babel` comes with an extraction method plugin that can extract
localizable messages from Django template files. Python is supported out of the
box by Babel. To use this extraction functionality, create a file called
`babel.cfg` in your project directory (the directory above your project
package), with the content:

```ini
[django: templates/**.*]
[django: mypkg/*/templates/**.*]
[python: mypkg/**.py]
```

This instructs Babel to look for any files in the top-level `templates`
directory, or any files in application `templates` directories, and use the
extraction method named “django” to extract messages from those template files.
You'll need to adjust those glob patterns to wherever you my be storing your
templates.

Also, any files with the extension `.py` inside your package directory (replace
“mypkg” with the actual name of your Django project package) are processed by
the “python” extraction method.

If you don't use setuptools, or for some reason haven't installed !BabelDjango
using setuptools/pip, you'll need to define what function the extraction method
“django” maps to. This is done in an extra section at the top of the
configuration file:

```ini
[extractors]
django = babeldjango.extract:extract_django
```

The encoding of the templates is assumed to be UTF-8. If you are using a
different encoding, you will need to specify it in the configuration. For
example:

```ini
[django: templates/**.*]
encoding = iso-8859-1
```

### Running the Extraction Process

Once you've set up the configuration file, the actual extraction is performed
by executing the command-line program `pybabel` which is installed alongside
the Babel package:

```bash
$ cd projectdir
$ pybabel extract -F babel.cfg -o mypkg/locale/django.pot .
```

This creates the PO file template in `mypkg/locale/django.pot`.

### Creating and Updating Translations Catalogs

If you don't already have translation catalogs, you need to create them. This
is done using the `pybabel init` command:

```bash
$ pybabel init -D django -i mypkg/locale/django.pot -d mypkg/locale -l en_US
$ pybabel init -D django -i mypkg/locale/django.pot -d mypkg/locale -l de_DE
```

This should create two files: `mypkg/locale/en_US/django.po` and
`mypkg/locale/de_DE/django.po`. These files are where you put the actual
translations.

When you modify your Python source files or your templates, you genereally need
to sync the translation catalogs. For that, you first perform a fresh
extraction as described in the previous section, so that the `django.pot` file
gets updated.

Then, you run the `pybabel update` command to merge the changes into the
translation catalogs:

```bash $ pybabel update -D django -i mypkg/locale/django.pot -d mypkg/locale
```

This will update all the `.po` files found in the `mypkg/locale` directory.

### Compiling Translations Catalogs

Finally, you need to compile those `.po` files to binary `.mo` files. Use the
`pybabel compile` command for that:

```bash
$ pybabel compile -D django -d mypkg/locale
```

Add the `--statistics` option to get information about the completeness of your
translations:

```bash
$ pybabel compile -D django -d mypkg/locale --statistics
```

### Using `setup.py`

Much of the above process can be automated if you add a `setup.py` script to
your project and use the distutils/setuptools commands that come with Babel.
This is described at [Distutils/Setuptools Integration][setup].


## Using the Middleware

To use the Babel middleware, add it to the list of `MIDDLEWARE_CLASSES` in your
settings module. If you're also using Django's own `LocaleMiddleware` to vary
the locale based on user preference, the Babel middleware must be inserted
after the Django one:

```python
MIDDLEWARE_CLASSES = (
    ...
    'django.middleware.locale.LocaleMiddleware',
    'babeldjango.middleware.LocaleMiddleware',
    ...
)
```

This adds a `locale` attribute to the request object, which is an instance of
the Babel `Locale` class. You can access the locale via `request.locale` when
the request object is available, or otherwise use the
`babeldjango.middleware.get_current_locale()` function to get the current
locale from a thread-local cache.


## Using the Template Tags

The template filters provided by !BabelDjango allow formatting of date/time and
number values in a locale-sensitive manner, providing much more powerful
alternatives to the `date`, `time`, and `floatformat` filters that come with
Django.

To make the template filters/tags available, you need to add !BabelDjango to
the list of `INSTALLED_APPS` in your settings module:

```python
INSTALLED_APPS = (
    ...
    'babeldjango',
    ...
)
```

And in every template you want to use the filters, you need to explicitly load
the !BabelDjango library:

```jinja
{% load babel %}
```

General information on date/time and number formatting can be found at
[Date Formatting][Dates] and [Number Formatting][Numbers].

The following filters are made available. The examples assume a locale of
`en_US`.

### `datefmt`

Renders a string representation of a date.

* __Input__:  `datetime.date`, `datetime.datetime`, or a float/int timestamp
* __Parameters__:  the format name or pattern (optional)

Assuming that `book.pubdate` returns a `datetime.date` or `datetime.datetime`
object:

```jinja
{{ book.pubdate|datefmt:"short" }}
```

would render: **4/1/07**, and

```jinja
{{ book.pubdate|datefmt:"E, MMM dd yyyy GGG" }}
```

would render: **Sun, Apr 01 2007 AD**

### `datetimefmt` 

Renders a string representation of a date and time.

* __Input__:  `datetime.datetime`, or a float/int timestamp
* __Parameters__:  the format name or pattern (optional)

Examples:
```jinja
{{ book.pubdate|datetimefmt:"short" }}
```

would render: **4/1/07 3:30 PM**, and

```jinja
{{ book.pubdate|datetimefmt:"E, MMM dd yyyy GGG' - 'HH:mm:ss'" }}
```

would render: **Sun, Apr 01 2007 AD - 15:30:00**

### `timefmt`

Renders a string representation of a time.

* __Input__:  `datetime.datetime`, `datetime.time`, or a float/int timestamp
* __Parameters__:  the format name or pattern (optional)

Examples:

```jinja
{{ book.pubdate|timefmt:"short" }}
```

would render: **3:30 PM**, and

```jinja
{{ book.pubdate|timefmt:"h 'o''clock' a'" }}
```

would render: **3 o'clock PM**

### `decimalfmt`

Renders a string representation of a decimal number.

* __Input__:  a `Decimal` object, or a float/int/long value
* __Parameters__:  the format name or pattern (optional)

Examples:

```jinja
{{ book.pagecount|decimalfmt }}
```

would render: **1,234**, and

```jinja
{{ book.pagecount|decimalfmt:"#,##0.00" }}
```

would render: **1,234.00**

### `currencyfmt`

Renders a number formatted as a currency value.

* __Input__:  a `Decimal` object, or a float/int/long value
* __Parameters__:  the currency code

Examples:

```jinja
{{ book.price|currencyfmt:"USD" }}
```

would render: **$49.90**

### `percentfmt`

Renders a string representation of a number as a percentage.

* __Input__:  a `Decimal` object, or a float/int/long value
* __Parameters__:  the format name or pattern (optional)

Examples:

Assuming `book.rebate` would return `0.15`,

```jinja
{{ book.rebate|percentfmt }}
```

would render **15%**, and

```jinja
{{ book.rebate|percentfmt:"#,##0.00%" }}
```

would render **15.00%**.

### `scientificfmt`

Renders a string representation of a number using scientific notation.

* __Input__:  a `Decimal` object, or a float/int/long value
* __Parameters__:  none

Examples:

Assuming `book.numsold` would return 1.000.000,

```jinja
{{ book.numsold|scientificfmt }}
```

would render **10E5**.



[Babel]: http://babel.pocoo.org/
[Django]: https://www.djangoproject.com/
[Django_i18n]: https://docs.djangoproject.com/en/dev/topics/i18n/translation/#localization-how-to-create-language-files
[Setup]: http://babel.pocoo.org/docs/setup/
[Dates]: http://babel.pocoo.org/docs/dates/
[Numbers]: http://babel.pocoo.org/docs/numbers/
