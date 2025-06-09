import doctest
from insights.parsers import rpm_pkgs
from insights.parsers.rpm_pkgs import RpmPkgs
from insights.tests import context_wrap
PACKAGES = ['httpd-core']

def test_system_user_dirs():
    test = RpmPkgs(context_wrap(PACKAGES))
    assert test.packages == PACKAGES

def test_doc_examples():
    env = {'rpm_pkgs': RpmPkgs(context_wrap(PACKAGES))}
    (failed, total) = doctest.testmod(rpm_pkgs, globs=env)
    assert failed == 0