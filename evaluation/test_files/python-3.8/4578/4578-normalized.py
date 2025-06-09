def construct_publish_comands(additional_steps=None, nightly=False):
    """Get the shell commands we'll use to actually build and publish a package to PyPI."""
    publish_commands = ['rm -rf dist'] + (additional_steps if additional_steps else []) + ['python setup.py sdist bdist_wheel{nightly}'.format(nightly=' --nightly' if nightly else ''), 'twine upload dist/*']
    return publish_commands