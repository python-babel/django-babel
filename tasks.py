import invoke


@invoke.task
def release(version):
    """`version`` should be a string like '0.4' or '1.0'."""
    invoke.run('git tag -s {0}'.format(version))
    invoke.run('git push --tags')

    invoke.run('python setup.py sdist')
    invoke.run('python setup.py bdist_wheel')

    invoke.run('twine upload -s dist/django-babel{0}* '.format(version))
    invoke.run('twine upload -s dist/django_babel{0}* '.format(version))
