"""The Versioneer - like a rocketeer, but for versions.

The Versioneer
==============

* like a rocketeer, but for versions!
* https://github.com/python-versioneer/python-versioneer
* Brian Warner
* License: Public Domain
* Compatible with: Python 3.6, 3.7, 3.8, 3.9, 3.10 and pypy3
* [![Latest Version][pypi-image]][pypi-url]
* [![Build Status][travis-image]][travis-url]

This is a tool for managing a recorded version number in distutils/setuptools-based
python projects. The goal is to remove the tedious and error-prone "update
the embedded version string" step from your release process. Making a new
release should be as easy as recording a new tag in your version-control
system, and maybe making new tarballs.


## Quick Install

* `pip install versioneer` to somewhere in your $PATH
* add a `[versioneer]` section to your setup.cfg (see [Install](INSTALL.md))
* run `versioneer install` in your source tree, commit the results
* Verify version information with `python setup.py version`

## Version Identifiers

Source trees come from a variety of places:

* a version-control system checkout (mostly used by developers)
* a nightly tarball, produced by build automation
* a snapshot tarball, produced by a web-based VCS browser, like github's
  "tarball from tag" feature
* a release tarball, produced by "setup.py sdist", distributed through PyPI

Within each source tree, the version identifier (either a string or a number,
this tool is format-agnostic) can come from a variety of places:

* ask the VCS tool itself, e.g. "git describe" (for checkouts), which knows
  about recent "tags" and an absolute revision-id
* the name of the directory into which the tarball was unpacked
* an expanded VCS keyword ($Id$, etc)
* a `_version.py` created by some earlier build step

For released software, the version identifier is closely related to a VCS
tag. Some projects use tag names that include more than just the version
string (e.g. "myproject-1.2" instead of just "1.2"), in which case the tool
needs to strip the tag prefix to extract the version identifier. For
unreleased software (between tags), the version identifier should provide
enough information to help developers recreate the same tree, while also
giving them an idea of roughly how old the tree is (after version 1.2, before
version 1.3). Many VCS systems can report a description that captures this,
for example `git describe --tags --dirty --always` reports things like
"0.7-1-g574ab98-dirty" to indicate that the checkout is one revision past the
0.7 tag, has a unique revision id of "574ab98", and is "dirty" (it has
uncommitted changes).

The version identifier is used for multiple purposes:

* to allow the module to self-identify its version: `myproject.__version__`
* to choose a name and prefix for a 'setup.py sdist' tarball

## Theory of Operation

Versioneer works by adding a special `_version.py` file into your source
tree, where your `__init__.py` can import it. This `_version.py` knows how to
dynamically ask the VCS tool for version information at import time.

`_version.py` also contains `$Revision$` markers, and the installation
process marks `_version.py` to have this marker rewritten with a tag name
during the `git archive` command. As a result, generated tarballs will
contain enough information to get the proper version.

To allow `setup.py` to compute a version too, a `versioneer.py` is added to
the top level of your source tree, next to `setup.py` and the `setup.cfg`
that configures it. This overrides several distutils/setuptools commands to
compute the version when invoked, and changes `setup.py build` and `setup.py
sdist` to replace `_version.py` with a small static file that contains just
the generated version data.

## Installation

See [INSTALL.md](./INSTALL.md) for detailed installation instructions.

## Version-String Flavors

Code which uses Versioneer can learn about its version string at runtime by
importing `_version` from your main `__init__.py` file and running the
`get_versions()` function. From the "outside" (e.g. in `setup.py`), you can
import the top-level `versioneer.py` and run `get_versions()`.

Both functions return a dictionary with different flavors of version
information:

* `['version']`: A condensed version string, rendered using the selected
  style. This is the most commonly used value for the project's version
  string. The default "pep440" style yields strings like `0.11`,
  `0.11+2.g1076c97`, or `0.11+2.g1076c97.dirty`. See the "Styles" section
  below for alternative styles.

* `['full-revisionid']`: detailed revision identifier. For Git, this is the
  full SHA1 commit id, e.g. "1076c978a8d3cfc70f408fe5974aa6c092c949ac".

* `['date']`: Date and time of the latest `HEAD` commit. For Git, it is the
  commit date in ISO 8601 format. This will be None if the date is not
  available.

* `['dirty']`: a boolean, True if the tree has uncommitted changes. Note that
  this is only accurate if run in a VCS checkout, otherwise it is likely to
  be False or None

* `['error']`: if the version string could not be computed, this will be set
  to a string describing the problem, otherwise it will be None. It may be
  useful to throw an exception in setup.py if this is set, to avoid e.g.
  creating tarballs with a version string of "unknown".

Some variants are more useful than others. Including `full-revisionid` in a
bug report should allow developers to reconstruct the exact code being tested
(or indicate the presence of local changes that should be shared with the
developers). `version` is suitable for display in an "about" box or a CLI
`--version` output: it can be easily compared against release notes and lists
of bugs fixed in various releases.

The installer adds the following text to your `__init__.py` to place a basic
version in `YOURPROJECT.__version__`:

    from ._version import get_versions
    __version__ = get_versions()['version']
    del get_versions

## Styles

The setup.cfg `style=` configuration controls how the VCS information is
rendered into a version string.

The default style, "pep440", produces a PEP440-compliant string, equal to the
un-prefixed tag name for actual releases, and containing an additional "local
version" section with more detail for in-between builds. For Git, this is
TAG[+DISTANCE.gHEX[.dirty]] , using information from `git describe --tags
--dirty --always`. For example "0.11+2.g1076c97.dirty" indicates that the
tree is like the "1076c97" commit but has uncommitted changes (".dirty"), and
that this commit is two revisions ("+2") beyond the "0.11" tag. For released
software (exactly equal to a known tag), the identifier will only contain the
stripped tag, e.g. "0.11".

Other styles are available. See [details.md](details.md) in the Versioneer
source tree for descriptions.

## Debugging

Versioneer tries to avoid fatal errors: if something goes wrong, it will tend
to return a version of "0+unknown". To investigate the problem, run `setup.py
version`, which will run the version-lookup code in a verbose mode, and will
display the full contents of `get_versions()` (including the `error` string,
which may help identify what went wrong).

## Known Limitations

Some situations are known to cause problems for Versioneer. This details the
most significant ones. More can be found on Github
[issues page](https://github.com/python-versioneer/python-versioneer/issues).

### Subprojects

Versioneer has limited support for source trees in which `setup.py` is not in
the root directory (e.g. `setup.py` and `.git/` are *not* siblings). The are
two common reasons why `setup.py` might not be in the root:

* Source trees which contain multiple subprojects, such as
  [Buildbot](https://github.com/buildbot/buildbot), which contains both
  "master" and "slave" subprojects, each with their own `setup.py`,
  `setup.cfg`, and `tox.ini`. Projects like these produce multiple PyPI
  distributions (and upload multiple independently-installable tarballs).
* Source trees whose main purpose is to contain a C library, but which also
  provide bindings to Python (and perhaps other languages) in subdirectories.

Versioneer will look for `.git` in parent directories, and most operations
should get the right version string. However `pip` and `setuptools` have bugs
and implementation details which frequently cause `pip install .` from a
subproject directory to fail to find a correct version string (so it usually
defaults to `0+unknown`).

`pip install --editable .` should work correctly. `setup.py install` might
work too.

Pip-8.1.1 is known to have this problem, but hopefully it will get fixed in
some later version.

[Bug #38](https://github.com/python-versioneer/python-versioneer/issues/38) is tracking
this issue. The discussion in
[PR #61](https://github.com/python-versioneer/python-versioneer/pull/61) describes the
issue from the Versioneer side in more detail.
[pip PR#3176](https://github.com/pypa/pip/pull/3176) and
[pip PR#3615](https://github.com/pypa/pip/pull/3615) contain work to improve
pip to let Versioneer work correctly.

Versioneer-0.16 and earlier only looked for a `.git` directory next to the
`setup.cfg`, so subprojects were completely unsupported with those releases.

### Editable installs with setuptools <= 18.5

`setup.py develop` and `pip install --editable .` allow you to install a
project into a virtualenv once, then continue editing the source code (and
test) without re-installing after every change.

"Entry-point scripts" (`setup(entry_points={"console_scripts": ..})`) are a
convenient way to specify executable scripts that should be installed along
with the python package.

These both work as expected when using modern setuptools. When using
setuptools-18.5 or earlier, however, certain operations will cause
`pkg_resources.DistributionNotFound` errors when running the entrypoint
script, which must be resolved by re-installing the package. This happens
when the install happens with one version, then the egg_info data is
regenerated while a different version is checked out. Many setup.py commands
cause egg_info to be rebuilt (including `sdist`, `wheel`, and installing into
a different virtualenv), so this can be surprising.

[Bug #83](https://github.com/python-versioneer/python-versioneer/issues/83) describes
this one, but upgrading to a newer version of setuptools should probably
resolve it.


## Updating Versioneer

To upgrade your project to a new release of Versioneer, do the following:

* install the new Versioneer (`pip install -U versioneer` or equivalent)
* edit `setup.cfg`, if necessary, to include any new configuration settings
  indicated by the release notes. See [UPGRADING](./UPGRADING.md) for details.
* re-run `versioneer install` in your source tree, to replace
  `SRC/_version.py`
* commit any changed files

## Future Directions

This tool is designed to make it easily extended to other version-control
systems: all VCS-specific components are in separate directories like
src/git/ . The top-level `versioneer.py` script is assembled from these
components by running make-versioneer.py . In the future, make-versioneer.py
will take a VCS name as an argument, and will construct a version of
`versioneer.py` that is specific to the given VCS. It might also take the
configuration arguments that are currently provided manually during
installation by editing setup.py . Alternatively, it might go the other
direction and include code from all supported VCS systems, reducing the
number of intermediate scripts.

## Similar projects

* [setuptools_scm](https://github.com/pypa/setuptools_scm/) - a non-vendored build-time
  dependency
* [minver](https://github.com/jbweston/miniver) - a lightweight reimplementation of
  versioneer
* [versioningit](https://github.com/jwodder/versioningit) - a PEP 518-based setuptools
  plugin

## License

To make Versioneer easier to embed, all its code is dedicated to the public
domain. The `_version.py` that it creates is also in the public domain.
Specifically, both are released under the Creative Commons "Public Domain
Dedication" license (CC0-1.0), as described in
https://creativecommons.org/publicdomain/zero/1.0/ .

[pypi-image]: https://img.shields.io/pypi/v/versioneer.svg
[pypi-url]: https://pypi.python.org/pypi/versioneer/
[travis-image]:
https://img.shields.io/travis/com/python-versioneer/python-versioneer.svg
[travis-url]: https://travis-ci.com/github/python-versioneer/python-versioneer

"""
import configparser
import errno
import json
import os
import re
import subprocess
import sys
from typing import Callable, Dict
import functools

class VersioneerConfig:
    """Container for Versioneer configuration parameters."""

def get_root():
    """Get the project root directory.

    We require that all commands are run from the project root, i.e. the
    directory that contains setup.py, setup.cfg, and versioneer.py .
    """
    root = os.path.realpath(os.path.abspath(os.getcwd()))
    setup_py = os.path.join(root, 'setup.py')
    versioneer_py = os.path.join(root, 'versioneer.py')
    if not (os.path.exists(setup_py) or os.path.exists(versioneer_py)):
        root = os.path.dirname(os.path.realpath(os.path.abspath(sys.argv[0])))
        setup_py = os.path.join(root, 'setup.py')
        versioneer_py = os.path.join(root, 'versioneer.py')
    if not (os.path.exists(setup_py) or os.path.exists(versioneer_py)):
        err = "Versioneer was unable to run the project root directory. Versioneer requires setup.py to be executed from its immediate directory (like 'python setup.py COMMAND'), or in a way that lets it use sys.argv[0] to find the root (like 'python path/to/setup.py COMMAND')."
        raise VersioneerBadRootError(err)
    try:
        my_path = os.path.realpath(os.path.abspath(__file__))
        me_dir = os.path.normcase(os.path.splitext(my_path)[0])
        vsr_dir = os.path.normcase(os.path.splitext(versioneer_py)[0])
        if me_dir != vsr_dir:
            print('Warning: build in %s is using versioneer.py from %s' % (os.path.dirname(my_path), versioneer_py))
    except NameError:
        pass
    return root

def get_config_from_root(root):
    """Read the project setup.cfg file to determine Versioneer config."""
    setup_cfg = os.path.join(root, 'setup.cfg')
    parser = configparser.ConfigParser()
    with open(setup_cfg, 'r') as cfg_file:
        parser.read_file(cfg_file)
    VCS = parser.get('versioneer', 'VCS')
    section = parser['versioneer']
    cfg = VersioneerConfig()
    cfg.VCS = VCS
    cfg.style = section.get('style', '')
    cfg.versionfile_source = section.get('versionfile_source')
    cfg.versionfile_build = section.get('versionfile_build')
    cfg.tag_prefix = section.get('tag_prefix')
    if cfg.tag_prefix in ("''", '""'):
        cfg.tag_prefix = ''
    cfg.parentdir_prefix = section.get('parentdir_prefix')
    cfg.verbose = section.get('verbose')
    return cfg

class NotThisMethod(Exception):
    """Exception raised if a method is not valid for the current scenario."""
LONG_VERSION_PY: Dict[str, str] = {}
HANDLERS: Dict[str, Dict[str, Callable]] = {}

def register_vcs_handler(vcs, method):
    """Create decorator to mark a method as the handler of a VCS."""

    def decorate(f):
        """Store f in HANDLERS[vcs][method]."""
        HANDLERS.setdefault(vcs, {})[method] = f
        return f
    return decorate

def run_command(commands, args, cwd=None, verbose=False, hide_stderr=False, env=None):
    """Call the given command(s)."""
    assert isinstance(commands, list)
    process = None
    popen_kwargs = {}
    if sys.platform == 'win32':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        popen_kwargs['startupinfo'] = startupinfo
    for command in commands:
        try:
            dispcmd = str([command] + args)
            process = subprocess.Popen([command] + args, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE if hide_stderr else None, **popen_kwargs)
            break
        except OSError:
            e = sys.exc_info()[1]
            if e.errno == errno.ENOENT:
                continue
            if verbose:
                print('unable to run %s' % dispcmd)
                print(e)
            return (None, None)
    else:
        if verbose:
            print('unable to find command, tried %s' % (commands,))
        return (None, None)
    stdout = process.communicate()[0].strip().decode()
    if process.returncode != 0:
        if verbose:
            print('unable to run %s (error)' % dispcmd)
            print('stdout was %s' % stdout)
        return (None, process.returncode)
    return (stdout, process.returncode)
LONG_VERSION_PY['git'] = '\n# This file helps to compute a version number in source trees obtained from\n# git-archive tarball (such as those provided by githubs download-from-tag\n# feature). Distribution tarballs (built by setup.py sdist) and build\n# directories (produced by setup.py build) will contain a much shorter file\n# that just contains the computed version number.\n\n# This file is released into the public domain. Generated by\n# versioneer-0.22 (https://github.com/python-versioneer/python-versioneer)\n\n"""Git implementation of _version.py."""\n\nimport errno\nimport os\nimport re\nimport subprocess\nimport sys\nfrom typing import Callable, Dict\nimport functools\n\n\ndef get_keywords():\n    """Get the keywords needed to look up the version information."""\n    # these strings will be replaced by git during git-archive.\n    # setup.py/versioneer.py will grep for the variable names, so they must\n    # each be defined on a line of their own. _version.py will just call\n    # get_keywords().\n    git_refnames = "%(DOLLAR)sFormat:%%d%(DOLLAR)s"\n    git_full = "%(DOLLAR)sFormat:%%H%(DOLLAR)s"\n    git_date = "%(DOLLAR)sFormat:%%ci%(DOLLAR)s"\n    keywords = {"refnames": git_refnames, "full": git_full, "date": git_date}\n    return keywords\n\n\nclass VersioneerConfig:\n    """Container for Versioneer configuration parameters."""\n\n\ndef get_config():\n    """Create, populate and return the VersioneerConfig() object."""\n    # these strings are filled in when \'setup.py versioneer\' creates\n    # _version.py\n    cfg = VersioneerConfig()\n    cfg.VCS = "git"\n    cfg.style = "%(STYLE)s"\n    cfg.tag_prefix = "%(TAG_PREFIX)s"\n    cfg.parentdir_prefix = "%(PARENTDIR_PREFIX)s"\n    cfg.versionfile_source = "%(VERSIONFILE_SOURCE)s"\n    cfg.verbose = False\n    return cfg\n\n\nclass NotThisMethod(Exception):\n    """Exception raised if a method is not valid for the current scenario."""\n\n\nLONG_VERSION_PY: Dict[str, str] = {}\nHANDLERS: Dict[str, Dict[str, Callable]] = {}\n\n\ndef register_vcs_handler(vcs, method):  # decorator\n    """Create decorator to mark a method as the handler of a VCS."""\n    def decorate(f):\n        """Store f in HANDLERS[vcs][method]."""\n        if vcs not in HANDLERS:\n            HANDLERS[vcs] = {}\n        HANDLERS[vcs][method] = f\n        return f\n    return decorate\n\n\ndef run_command(commands, args, cwd=None, verbose=False, hide_stderr=False,\n                env=None):\n    """Call the given command(s)."""\n    assert isinstance(commands, list)\n    process = None\n\n    popen_kwargs = {}\n    if sys.platform == "win32":\n        # This hides the console window if pythonw.exe is used\n        startupinfo = subprocess.STARTUPINFO()\n        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW\n        popen_kwargs["startupinfo"] = startupinfo\n\n    for command in commands:\n        try:\n            dispcmd = str([command] + args)\n            # remember shell=False, so use git.cmd on windows, not just git\n            process = subprocess.Popen([command] + args, cwd=cwd, env=env,\n                                       stdout=subprocess.PIPE,\n                                       stderr=(subprocess.PIPE if hide_stderr\n                                               else None), **popen_kwargs)\n            break\n        except OSError:\n            e = sys.exc_info()[1]\n            if e.errno == errno.ENOENT:\n                continue\n            if verbose:\n                print("unable to run %%s" %% dispcmd)\n                print(e)\n            return None, None\n    else:\n        if verbose:\n            print("unable to find command, tried %%s" %% (commands,))\n        return None, None\n    stdout = process.communicate()[0].strip().decode()\n    if process.returncode != 0:\n        if verbose:\n            print("unable to run %%s (error)" %% dispcmd)\n            print("stdout was %%s" %% stdout)\n        return None, process.returncode\n    return stdout, process.returncode\n\n\ndef versions_from_parentdir(parentdir_prefix, root, verbose):\n    """Try to determine the version from the parent directory name.\n\n    Source tarballs conventionally unpack into a directory that includes both\n    the project name and a version string. We will also support searching up\n    two directory levels for an appropriately named parent directory\n    """\n    rootdirs = []\n\n    for _ in range(3):\n        dirname = os.path.basename(root)\n        if dirname.startswith(parentdir_prefix):\n            return {"version": dirname[len(parentdir_prefix):],\n                    "full-revisionid": None,\n                    "dirty": False, "error": None, "date": None}\n        rootdirs.append(root)\n        root = os.path.dirname(root)  # up a level\n\n    if verbose:\n        print("Tried directories %%s but none started with prefix %%s" %%\n              (str(rootdirs), parentdir_prefix))\n    raise NotThisMethod("rootdir doesn\'t start with parentdir_prefix")\n\n\n@register_vcs_handler("git", "get_keywords")\ndef git_get_keywords(versionfile_abs):\n    """Extract version information from the given file."""\n    # the code embedded in _version.py can just fetch the value of these\n    # keywords. When used from setup.py, we don\'t want to import _version.py,\n    # so we do it with a regexp instead. This function is not used from\n    # _version.py.\n    keywords = {}\n    try:\n        with open(versionfile_abs, "r") as fobj:\n            for line in fobj:\n                if line.strip().startswith("git_refnames ="):\n                    mo = re.search(r\'=\\s*"(.*)"\', line)\n                    if mo:\n                        keywords["refnames"] = mo.group(1)\n                if line.strip().startswith("git_full ="):\n                    mo = re.search(r\'=\\s*"(.*)"\', line)\n                    if mo:\n                        keywords["full"] = mo.group(1)\n                if line.strip().startswith("git_date ="):\n                    mo = re.search(r\'=\\s*"(.*)"\', line)\n                    if mo:\n                        keywords["date"] = mo.group(1)\n    except OSError:\n        pass\n    return keywords\n\n\n@register_vcs_handler("git", "keywords")\ndef git_versions_from_keywords(keywords, tag_prefix, verbose):\n    """Get version information from git keywords."""\n    if "refnames" not in keywords:\n        raise NotThisMethod("Short version file found")\n    date = keywords.get("date")\n    if date is not None:\n        # Use only the last line.  Previous lines may contain GPG signature\n        # information.\n        date = date.splitlines()[-1]\n\n        # git-2.2.0 added "%%cI", which expands to an ISO-8601 -compliant\n        # datestamp. However we prefer "%%ci" (which expands to an "ISO-8601\n        # -like" string, which we must then edit to make compliant), because\n        # it\'s been around since git-1.5.3, and it\'s too difficult to\n        # discover which version we\'re using, or to work around using an\n        # older one.\n        date = date.strip().replace(" ", "T", 1).replace(" ", "", 1)\n    refnames = keywords["refnames"].strip()\n    if refnames.startswith("$Format"):\n        if verbose:\n            print("keywords are unexpanded, not using")\n        raise NotThisMethod("unexpanded keywords, not a git-archive tarball")\n    refs = {r.strip() for r in refnames.strip("()").split(",")}\n    # starting in git-1.8.3, tags are listed as "tag: foo-1.0" instead of\n    # just "foo-1.0". If we see a "tag: " prefix, prefer those.\n    TAG = "tag: "\n    tags = {r[len(TAG):] for r in refs if r.startswith(TAG)}\n    if not tags:\n        # Either we\'re using git < 1.8.3, or there really are no tags. We use\n        # a heuristic: assume all version tags have a digit. The old git %%d\n        # expansion behaves like git log --decorate=short and strips out the\n        # refs/heads/ and refs/tags/ prefixes that would let us distinguish\n        # between branches and tags. By ignoring refnames without digits, we\n        # filter out many common branch names like "release" and\n        # "stabilization", as well as "HEAD" and "master".\n        tags = {r for r in refs if re.search(r\'\\d\', r)}\n        if verbose:\n            print("discarding \'%%s\', no digits" %% ",".join(refs - tags))\n    if verbose:\n        print("likely tags: %%s" %% ",".join(sorted(tags)))\n    for ref in sorted(tags):\n        # sorting will prefer e.g. "2.0" over "2.0rc1"\n        if ref.startswith(tag_prefix):\n            r = ref[len(tag_prefix):]\n            # Filter out refs that exactly match prefix or that don\'t start\n            # with a number once the prefix is stripped (mostly a concern\n            # when prefix is \'\')\n            if not re.match(r\'\\d\', r):\n                continue\n            if verbose:\n                print("picking %%s" %% r)\n            return {"version": r,\n                    "full-revisionid": keywords["full"].strip(),\n                    "dirty": False, "error": None,\n                    "date": date}\n    # no suitable tags, so version is "0+unknown", but full hex is still there\n    if verbose:\n        print("no suitable tags, using unknown + full revision id")\n    return {"version": "0+unknown",\n            "full-revisionid": keywords["full"].strip(),\n            "dirty": False, "error": "no suitable tags", "date": None}\n\n\n@register_vcs_handler("git", "pieces_from_vcs")\ndef git_pieces_from_vcs(tag_prefix, root, verbose, runner=run_command):\n    """Get version from \'git describe\' in the root of the source tree.\n\n    This only gets called if the git-archive \'subst\' keywords were *not*\n    expanded, and _version.py hasn\'t already been rewritten with a short\n    version string, meaning we\'re inside a checked out source tree.\n    """\n    GITS = ["git"]\n    if sys.platform == "win32":\n        GITS = ["git.cmd", "git.exe"]\n\n    # GIT_DIR can interfere with correct operation of Versioneer.\n    # It may be intended to be passed to the Versioneer-versioned project,\n    # but that should not change where we get our version from.\n    env = os.environ.copy()\n    env.pop("GIT_DIR", None)\n    runner = functools.partial(runner, env=env)\n\n    _, rc = runner(GITS, ["rev-parse", "--git-dir"], cwd=root,\n                   hide_stderr=True)\n    if rc != 0:\n        if verbose:\n            print("Directory %%s not under git control" %% root)\n        raise NotThisMethod("\'git rev-parse --git-dir\' returned error")\n\n    MATCH_ARGS = ["--match", "%%s*" %% tag_prefix] if tag_prefix else []\n\n    # if there is a tag matching tag_prefix, this yields TAG-NUM-gHEX[-dirty]\n    # if there isn\'t one, this yields HEX[-dirty] (no NUM)\n    describe_out, rc = runner(GITS, ["describe", "--tags", "--dirty",\n                                     "--always", "--long", *MATCH_ARGS],\n                              cwd=root)\n    # --long was added in git-1.5.5\n    if describe_out is None:\n        raise NotThisMethod("\'git describe\' failed")\n    describe_out = describe_out.strip()\n    full_out, rc = runner(GITS, ["rev-parse", "HEAD"], cwd=root)\n    if full_out is None:\n        raise NotThisMethod("\'git rev-parse\' failed")\n    full_out = full_out.strip()\n\n    pieces = {}\n    pieces["long"] = full_out\n    pieces["short"] = full_out[:7]  # maybe improved later\n    pieces["error"] = None\n\n    branch_name, rc = runner(GITS, ["rev-parse", "--abbrev-ref", "HEAD"],\n                             cwd=root)\n    # --abbrev-ref was added in git-1.6.3\n    if rc != 0 or branch_name is None:\n        raise NotThisMethod("\'git rev-parse --abbrev-ref\' returned error")\n    branch_name = branch_name.strip()\n\n    if branch_name == "HEAD":\n        # If we aren\'t exactly on a branch, pick a branch which represents\n        # the current commit. If all else fails, we are on a branchless\n        # commit.\n        branches, rc = runner(GITS, ["branch", "--contains"], cwd=root)\n        # --contains was added in git-1.5.4\n        if rc != 0 or branches is None:\n            raise NotThisMethod("\'git branch --contains\' returned error")\n        branches = branches.split("\\n")\n\n        # Remove the first line if we\'re running detached\n        if "(" in branches[0]:\n            branches.pop(0)\n\n        # Strip off the leading "* " from the list of branches.\n        branches = [branch[2:] for branch in branches]\n        if "master" in branches:\n            branch_name = "master"\n        elif not branches:\n            branch_name = None\n        else:\n            # Pick the first branch that is returned. Good or bad.\n            branch_name = branches[0]\n\n    pieces["branch"] = branch_name\n\n    # parse describe_out. It will be like TAG-NUM-gHEX[-dirty] or HEX[-dirty]\n    # TAG might have hyphens.\n    git_describe = describe_out\n\n    # look for -dirty suffix\n    dirty = git_describe.endswith("-dirty")\n    pieces["dirty"] = dirty\n    if dirty:\n        git_describe = git_describe[:git_describe.rindex("-dirty")]\n\n    # now we have TAG-NUM-gHEX or HEX\n\n    if "-" in git_describe:\n        # TAG-NUM-gHEX\n        mo = re.search(r\'^(.+)-(\\d+)-g([0-9a-f]+)$\', git_describe)\n        if not mo:\n            # unparsable. Maybe git-describe is misbehaving?\n            pieces["error"] = ("unable to parse git-describe output: \'%%s\'"\n                               %% describe_out)\n            return pieces\n\n        # tag\n        full_tag = mo.group(1)\n        if not full_tag.startswith(tag_prefix):\n            if verbose:\n                fmt = "tag \'%%s\' doesn\'t start with prefix \'%%s\'"\n                print(fmt %% (full_tag, tag_prefix))\n            pieces["error"] = ("tag \'%%s\' doesn\'t start with prefix \'%%s\'"\n                               %% (full_tag, tag_prefix))\n            return pieces\n        pieces["closest-tag"] = full_tag[len(tag_prefix):]\n\n        # distance: number of commits since tag\n        pieces["distance"] = int(mo.group(2))\n\n        # commit: short hex revision ID\n        pieces["short"] = mo.group(3)\n\n    else:\n        # HEX: no tags\n        pieces["closest-tag"] = None\n        count_out, rc = runner(GITS, ["rev-list", "HEAD", "--count"], cwd=root)\n        pieces["distance"] = int(count_out)  # total number of commits\n\n    # commit date: see ISO-8601 comment in git_versions_from_keywords()\n    date = runner(GITS, ["show", "-s", "--format=%%ci", "HEAD"], cwd=root)[0].strip()\n    # Use only the last line.  Previous lines may contain GPG signature\n    # information.\n    date = date.splitlines()[-1]\n    pieces["date"] = date.strip().replace(" ", "T", 1).replace(" ", "", 1)\n\n    return pieces\n\n\ndef plus_or_dot(pieces):\n    """Return a + if we don\'t already have one, else return a ."""\n    if "+" in pieces.get("closest-tag", ""):\n        return "."\n    return "+"\n\n\ndef render_pep440(pieces):\n    """Build up version string, with post-release "local version identifier".\n\n    Our goal: TAG[+DISTANCE.gHEX[.dirty]] . Note that if you\n    get a tagged build and then dirty it, you\'ll get TAG+0.gHEX.dirty\n\n    Exceptions:\n    1: no tags. git_describe was just HEX. 0+untagged.DISTANCE.gHEX[.dirty]\n    """\n    if pieces["closest-tag"]:\n        rendered = pieces["closest-tag"]\n        if pieces["distance"] or pieces["dirty"]:\n            rendered += plus_or_dot(pieces)\n            rendered += "%%d.g%%s" %% (pieces["distance"], pieces["short"])\n            if pieces["dirty"]:\n                rendered += ".dirty"\n    else:\n        # exception #1\n        rendered = "0+untagged.%%d.g%%s" %% (pieces["distance"],\n                                          pieces["short"])\n        if pieces["dirty"]:\n            rendered += ".dirty"\n    return rendered\n\n\ndef render_pep440_branch(pieces):\n    """TAG[[.dev0]+DISTANCE.gHEX[.dirty]] .\n\n    The ".dev0" means not master branch. Note that .dev0 sorts backwards\n    (a feature branch will appear "older" than the master branch).\n\n    Exceptions:\n    1: no tags. 0[.dev0]+untagged.DISTANCE.gHEX[.dirty]\n    """\n    if pieces["closest-tag"]:\n        rendered = pieces["closest-tag"]\n        if pieces["distance"] or pieces["dirty"]:\n            if pieces["branch"] != "master":\n                rendered += ".dev0"\n            rendered += plus_or_dot(pieces)\n            rendered += "%%d.g%%s" %% (pieces["distance"], pieces["short"])\n            if pieces["dirty"]:\n                rendered += ".dirty"\n    else:\n        # exception #1\n        rendered = "0"\n        if pieces["branch"] != "master":\n            rendered += ".dev0"\n        rendered += "+untagged.%%d.g%%s" %% (pieces["distance"],\n                                          pieces["short"])\n        if pieces["dirty"]:\n            rendered += ".dirty"\n    return rendered\n\n\ndef pep440_split_post(ver):\n    """Split pep440 version string at the post-release segment.\n\n    Returns the release segments before the post-release and the\n    post-release version number (or -1 if no post-release segment is present).\n    """\n    vc = str.split(ver, ".post")\n    return vc[0], int(vc[1] or 0) if len(vc) == 2 else None\n\n\ndef render_pep440_pre(pieces):\n    """TAG[.postN.devDISTANCE] -- No -dirty.\n\n    Exceptions:\n    1: no tags. 0.post0.devDISTANCE\n    """\n    if pieces["closest-tag"]:\n        if pieces["distance"]:\n            # update the post release segment\n            tag_version, post_version = pep440_split_post(pieces["closest-tag"])\n            rendered = tag_version\n            if post_version is not None:\n                rendered += ".post%%d.dev%%d" %% (post_version+1, pieces["distance"])\n            else:\n                rendered += ".post0.dev%%d" %% (pieces["distance"])\n        else:\n            # no commits, use the tag as the version\n            rendered = pieces["closest-tag"]\n    else:\n        # exception #1\n        rendered = "0.post0.dev%%d" %% pieces["distance"]\n    return rendered\n\n\ndef render_pep440_post(pieces):\n    """TAG[.postDISTANCE[.dev0]+gHEX] .\n\n    The ".dev0" means dirty. Note that .dev0 sorts backwards\n    (a dirty tree will appear "older" than the corresponding clean one),\n    but you shouldn\'t be releasing software with -dirty anyways.\n\n    Exceptions:\n    1: no tags. 0.postDISTANCE[.dev0]\n    """\n    if pieces["closest-tag"]:\n        rendered = pieces["closest-tag"]\n        if pieces["distance"] or pieces["dirty"]:\n            rendered += ".post%%d" %% pieces["distance"]\n            if pieces["dirty"]:\n                rendered += ".dev0"\n            rendered += plus_or_dot(pieces)\n            rendered += "g%%s" %% pieces["short"]\n    else:\n        # exception #1\n        rendered = "0.post%%d" %% pieces["distance"]\n        if pieces["dirty"]:\n            rendered += ".dev0"\n        rendered += "+g%%s" %% pieces["short"]\n    return rendered\n\n\ndef render_pep440_post_branch(pieces):\n    """TAG[.postDISTANCE[.dev0]+gHEX[.dirty]] .\n\n    The ".dev0" means not master branch.\n\n    Exceptions:\n    1: no tags. 0.postDISTANCE[.dev0]+gHEX[.dirty]\n    """\n    if pieces["closest-tag"]:\n        rendered = pieces["closest-tag"]\n        if pieces["distance"] or pieces["dirty"]:\n            rendered += ".post%%d" %% pieces["distance"]\n            if pieces["branch"] != "master":\n                rendered += ".dev0"\n            rendered += plus_or_dot(pieces)\n            rendered += "g%%s" %% pieces["short"]\n            if pieces["dirty"]:\n                rendered += ".dirty"\n    else:\n        # exception #1\n        rendered = "0.post%%d" %% pieces["distance"]\n        if pieces["branch"] != "master":\n            rendered += ".dev0"\n        rendered += "+g%%s" %% pieces["short"]\n        if pieces["dirty"]:\n            rendered += ".dirty"\n    return rendered\n\n\ndef render_pep440_old(pieces):\n    """TAG[.postDISTANCE[.dev0]] .\n\n    The ".dev0" means dirty.\n\n    Exceptions:\n    1: no tags. 0.postDISTANCE[.dev0]\n    """\n    if pieces["closest-tag"]:\n        rendered = pieces["closest-tag"]\n        if pieces["distance"] or pieces["dirty"]:\n            rendered += ".post%%d" %% pieces["distance"]\n            if pieces["dirty"]:\n                rendered += ".dev0"\n    else:\n        # exception #1\n        rendered = "0.post%%d" %% pieces["distance"]\n        if pieces["dirty"]:\n            rendered += ".dev0"\n    return rendered\n\n\ndef render_git_describe(pieces):\n    """TAG[-DISTANCE-gHEX][-dirty].\n\n    Like \'git describe --tags --dirty --always\'.\n\n    Exceptions:\n    1: no tags. HEX[-dirty]  (note: no \'g\' prefix)\n    """\n    if pieces["closest-tag"]:\n        rendered = pieces["closest-tag"]\n        if pieces["distance"]:\n            rendered += "-%%d-g%%s" %% (pieces["distance"], pieces["short"])\n    else:\n        # exception #1\n        rendered = pieces["short"]\n    if pieces["dirty"]:\n        rendered += "-dirty"\n    return rendered\n\n\ndef render_git_describe_long(pieces):\n    """TAG-DISTANCE-gHEX[-dirty].\n\n    Like \'git describe --tags --dirty --always -long\'.\n    The distance/hash is unconditional.\n\n    Exceptions:\n    1: no tags. HEX[-dirty]  (note: no \'g\' prefix)\n    """\n    if pieces["closest-tag"]:\n        rendered = pieces["closest-tag"]\n        rendered += "-%%d-g%%s" %% (pieces["distance"], pieces["short"])\n    else:\n        # exception #1\n        rendered = pieces["short"]\n    if pieces["dirty"]:\n        rendered += "-dirty"\n    return rendered\n\n\ndef render(pieces, style):\n    """Render the given version pieces into the requested style."""\n    if pieces["error"]:\n        return {"version": "unknown",\n                "full-revisionid": pieces.get("long"),\n                "dirty": None,\n                "error": pieces["error"],\n                "date": None}\n\n    if not style or style == "default":\n        style = "pep440"  # the default\n\n    if style == "pep440":\n        rendered = render_pep440(pieces)\n    elif style == "pep440-branch":\n        rendered = render_pep440_branch(pieces)\n    elif style == "pep440-pre":\n        rendered = render_pep440_pre(pieces)\n    elif style == "pep440-post":\n        rendered = render_pep440_post(pieces)\n    elif style == "pep440-post-branch":\n        rendered = render_pep440_post_branch(pieces)\n    elif style == "pep440-old":\n        rendered = render_pep440_old(pieces)\n    elif style == "git-describe":\n        rendered = render_git_describe(pieces)\n    elif style == "git-describe-long":\n        rendered = render_git_describe_long(pieces)\n    else:\n        raise ValueError("unknown style \'%%s\'" %% style)\n\n    return {"version": rendered, "full-revisionid": pieces["long"],\n            "dirty": pieces["dirty"], "error": None,\n            "date": pieces.get("date")}\n\n\ndef get_versions():\n    """Get version information or return default if unable to do so."""\n    # I am in _version.py, which lives at ROOT/VERSIONFILE_SOURCE. If we have\n    # __file__, we can work backwards from there to the root. Some\n    # py2exe/bbfreeze/non-CPython implementations don\'t do __file__, in which\n    # case we can only use expanded keywords.\n\n    cfg = get_config()\n    verbose = cfg.verbose\n\n    try:\n        return git_versions_from_keywords(get_keywords(), cfg.tag_prefix,\n                                          verbose)\n    except NotThisMethod:\n        pass\n\n    try:\n        root = os.path.realpath(__file__)\n        # versionfile_source is the relative path from the top of the source\n        # tree (where the .git directory might live) to this file. Invert\n        # this to find the root from __file__.\n        for _ in cfg.versionfile_source.split(\'/\'):\n            root = os.path.dirname(root)\n    except NameError:\n        return {"version": "0+unknown", "full-revisionid": None,\n                "dirty": None,\n                "error": "unable to find root of source tree",\n                "date": None}\n\n    try:\n        pieces = git_pieces_from_vcs(cfg.tag_prefix, root, verbose)\n        return render(pieces, cfg.style)\n    except NotThisMethod:\n        pass\n\n    try:\n        if cfg.parentdir_prefix:\n            return versions_from_parentdir(cfg.parentdir_prefix, root, verbose)\n    except NotThisMethod:\n        pass\n\n    return {"version": "0+unknown", "full-revisionid": None,\n            "dirty": None,\n            "error": "unable to compute version", "date": None}\n'

@register_vcs_handler('git', 'get_keywords')
def git_get_keywords(versionfile_abs):
    """Extract version information from the given file."""
    keywords = {}
    try:
        with open(versionfile_abs, 'r') as fobj:
            for line in fobj:
                if line.strip().startswith('git_refnames ='):
                    mo = re.search('=\\s*"(.*)"', line)
                    if mo:
                        keywords['refnames'] = mo.group(1)
                if line.strip().startswith('git_full ='):
                    mo = re.search('=\\s*"(.*)"', line)
                    if mo:
                        keywords['full'] = mo.group(1)
                if line.strip().startswith('git_date ='):
                    mo = re.search('=\\s*"(.*)"', line)
                    if mo:
                        keywords['date'] = mo.group(1)
    except OSError:
        pass
    return keywords

@register_vcs_handler('git', 'keywords')
def git_versions_from_keywords(keywords, tag_prefix, verbose):
    """Get version information from git keywords."""
    if 'refnames' not in keywords:
        raise NotThisMethod('Short version file found')
    date = keywords.get('date')
    if date is not None:
        date = date.splitlines()[-1]
        date = date.strip().replace(' ', 'T', 1).replace(' ', '', 1)
    refnames = keywords['refnames'].strip()
    if refnames.startswith('$Format'):
        if verbose:
            print('keywords are unexpanded, not using')
        raise NotThisMethod('unexpanded keywords, not a git-archive tarball')
    refs = {r.strip() for r in refnames.strip('()').split(',')}
    TAG = 'tag: '
    tags = {r[len(TAG):] for r in refs if r.startswith(TAG)}
    if not tags:
        tags = {r for r in refs if re.search('\\d', r)}
        if verbose:
            print("discarding '%s', no digits" % ','.join(refs - tags))
    if verbose:
        print('likely tags: %s' % ','.join(sorted(tags)))
    for ref in sorted(tags):
        if ref.startswith(tag_prefix):
            r = ref[len(tag_prefix):]
            if not re.match('\\d', r):
                continue
            if verbose:
                print('picking %s' % r)
            return {'version': r, 'full-revisionid': keywords['full'].strip(), 'dirty': False, 'error': None, 'date': date}
    if verbose:
        print('no suitable tags, using unknown + full revision id')
    return {'version': '0+unknown', 'full-revisionid': keywords['full'].strip(), 'dirty': False, 'error': 'no suitable tags', 'date': None}

@register_vcs_handler('git', 'pieces_from_vcs')
def git_pieces_from_vcs(tag_prefix, root, verbose, runner=run_command):
    """Get version from 'git describe' in the root of the source tree.

    This only gets called if the git-archive 'subst' keywords were *not*
    expanded, and _version.py hasn't already been rewritten with a short
    version string, meaning we're inside a checked out source tree.
    """
    GITS = ['git']
    if sys.platform == 'win32':
        GITS = ['git.cmd', 'git.exe']
    env = os.environ.copy()
    env.pop('GIT_DIR', None)
    runner = functools.partial(runner, env=env)
    (_, rc) = runner(GITS, ['rev-parse', '--git-dir'], cwd=root, hide_stderr=True)
    if rc != 0:
        if verbose:
            print('Directory %s not under git control' % root)
        raise NotThisMethod("'git rev-parse --git-dir' returned error")
    MATCH_ARGS = ['--match', '%s*' % tag_prefix] if tag_prefix else []
    (describe_out, rc) = runner(GITS, ['describe', '--tags', '--dirty', '--always', '--long', *MATCH_ARGS], cwd=root)
    if describe_out is None:
        raise NotThisMethod("'git describe' failed")
    describe_out = describe_out.strip()
    (full_out, rc) = runner(GITS, ['rev-parse', 'HEAD'], cwd=root)
    if full_out is None:
        raise NotThisMethod("'git rev-parse' failed")
    full_out = full_out.strip()
    pieces = {}
    pieces['long'] = full_out
    pieces['short'] = full_out[:7]
    pieces['error'] = None
    (branch_name, rc) = runner(GITS, ['rev-parse', '--abbrev-ref', 'HEAD'], cwd=root)
    if rc != 0 or branch_name is None:
        raise NotThisMethod("'git rev-parse --abbrev-ref' returned error")
    branch_name = branch_name.strip()
    if branch_name == 'HEAD':
        (branches, rc) = runner(GITS, ['branch', '--contains'], cwd=root)
        if rc != 0 or branches is None:
            raise NotThisMethod("'git branch --contains' returned error")
        branches = branches.split('\n')
        if '(' in branches[0]:
            branches.pop(0)
        branches = [branch[2:] for branch in branches]
        if 'master' in branches:
            branch_name = 'master'
        elif not branches:
            branch_name = None
        else:
            branch_name = branches[0]
    pieces['branch'] = branch_name
    git_describe = describe_out
    dirty = git_describe.endswith('-dirty')
    pieces['dirty'] = dirty
    if dirty:
        git_describe = git_describe[:git_describe.rindex('-dirty')]
    if '-' in git_describe:
        mo = re.search('^(.+)-(\\d+)-g([0-9a-f]+)$', git_describe)
        if not mo:
            pieces['error'] = "unable to parse git-describe output: '%s'" % describe_out
            return pieces
        full_tag = mo.group(1)
        if not full_tag.startswith(tag_prefix):
            if verbose:
                fmt = "tag '%s' doesn't start with prefix '%s'"
                print(fmt % (full_tag, tag_prefix))
            pieces['error'] = "tag '%s' doesn't start with prefix '%s'" % (full_tag, tag_prefix)
            return pieces
        pieces['closest-tag'] = full_tag[len(tag_prefix):]
        pieces['distance'] = int(mo.group(2))
        pieces['short'] = mo.group(3)
    else:
        pieces['closest-tag'] = None
        (count_out, rc) = runner(GITS, ['rev-list', 'HEAD', '--count'], cwd=root)
        pieces['distance'] = int(count_out)
    date = runner(GITS, ['show', '-s', '--format=%ci', 'HEAD'], cwd=root)[0].strip()
    date = date.splitlines()[-1]
    pieces['date'] = date.strip().replace(' ', 'T', 1).replace(' ', '', 1)
    return pieces

def do_vcs_install(manifest_in, versionfile_source, ipy):
    """Git-specific installation logic for Versioneer.

    For Git, this means creating/changing .gitattributes to mark _version.py
    for export-subst keyword substitution.
    """
    GITS = ['git']
    if sys.platform == 'win32':
        GITS = ['git.cmd', 'git.exe']
    files = [manifest_in, versionfile_source]
    if ipy:
        files.append(ipy)
    try:
        my_path = __file__
        if my_path.endswith('.pyc') or my_path.endswith('.pyo'):
            my_path = os.path.splitext(my_path)[0] + '.py'
        versioneer_file = os.path.relpath(my_path)
    except NameError:
        versioneer_file = 'versioneer.py'
    files.append(versioneer_file)
    present = False
    try:
        with open('.gitattributes', 'r') as fobj:
            for line in fobj:
                if line.strip().startswith(versionfile_source):
                    if 'export-subst' in line.strip().split()[1:]:
                        present = True
                        break
    except OSError:
        pass
    if not present:
        with open('.gitattributes', 'a+') as fobj:
            fobj.write(f'{versionfile_source} export-subst\n')
        files.append('.gitattributes')
    run_command(GITS, ['add', '--'] + files)

def versions_from_parentdir(parentdir_prefix, root, verbose):
    """Try to determine the version from the parent directory name.

    Source tarballs conventionally unpack into a directory that includes both
    the project name and a version string. We will also support searching up
    two directory levels for an appropriately named parent directory
    """
    rootdirs = []
    for _ in range(3):
        dirname = os.path.basename(root)
        if dirname.startswith(parentdir_prefix):
            return {'version': dirname[len(parentdir_prefix):], 'full-revisionid': None, 'dirty': False, 'error': None, 'date': None}
        rootdirs.append(root)
        root = os.path.dirname(root)
    if verbose:
        print('Tried directories %s but none started with prefix %s' % (str(rootdirs), parentdir_prefix))
    raise NotThisMethod("rootdir doesn't start with parentdir_prefix")
SHORT_VERSION_PY = "\n# This file was generated by 'versioneer.py' (0.22) from\n# revision-control system data, or from the parent directory name of an\n# unpacked source archive. Distribution tarballs contain a pre-generated copy\n# of this file.\n\nimport json\n\nversion_json = '''\n%s\n'''  # END VERSION_JSON\n\n\ndef get_versions():\n    return json.loads(version_json)\n"

def versions_from_file(filename):
    """Try to determine the version from _version.py if present."""
    try:
        with open(filename) as f:
            contents = f.read()
    except OSError:
        raise NotThisMethod('unable to read _version.py')
    mo = re.search("version_json = '''\\n(.*)'''  # END VERSION_JSON", contents, re.M | re.S)
    if not mo:
        mo = re.search("version_json = '''\\r\\n(.*)'''  # END VERSION_JSON", contents, re.M | re.S)
    if not mo:
        raise NotThisMethod('no version_json in _version.py')
    return json.loads(mo.group(1))

def write_to_version_file(filename, versions):
    """Write the given version number to the given _version.py file."""
    os.unlink(filename)
    contents = json.dumps(versions, sort_keys=True, indent=1, separators=(',', ': '))
    with open(filename, 'w') as f:
        f.write(SHORT_VERSION_PY % contents)
    print("set %s to '%s'" % (filename, versions['version']))

def plus_or_dot(pieces):
    """Return a + if we don't already have one, else return a ."""
    if '+' in pieces.get('closest-tag', ''):
        return '.'
    return '+'

def render_pep440(pieces):
    """Build up version string, with post-release "local version identifier".

    Our goal: TAG[+DISTANCE.gHEX[.dirty]] . Note that if you
    get a tagged build and then dirty it, you'll get TAG+0.gHEX.dirty

    Exceptions:
    1: no tags. git_describe was just HEX. 0+untagged.DISTANCE.gHEX[.dirty]
    """
    if pieces['closest-tag']:
        rendered = pieces['closest-tag']
        if pieces['distance'] or pieces['dirty']:
            rendered += plus_or_dot(pieces)
            rendered += '%d.g%s' % (pieces['distance'], pieces['short'])
            if pieces['dirty']:
                rendered += '.dirty'
    else:
        rendered = '0+untagged.%d.g%s' % (pieces['distance'], pieces['short'])
        if pieces['dirty']:
            rendered += '.dirty'
    return rendered

def render_pep440_branch(pieces):
    """TAG[[.dev0]+DISTANCE.gHEX[.dirty]] .

    The ".dev0" means not master branch. Note that .dev0 sorts backwards
    (a feature branch will appear "older" than the master branch).

    Exceptions:
    1: no tags. 0[.dev0]+untagged.DISTANCE.gHEX[.dirty]
    """
    if pieces['closest-tag']:
        rendered = pieces['closest-tag']
        if pieces['distance'] or pieces['dirty']:
            if pieces['branch'] != 'master':
                rendered += '.dev0'
            rendered += plus_or_dot(pieces)
            rendered += '%d.g%s' % (pieces['distance'], pieces['short'])
            if pieces['dirty']:
                rendered += '.dirty'
    else:
        rendered = '0'
        if pieces['branch'] != 'master':
            rendered += '.dev0'
        rendered += '+untagged.%d.g%s' % (pieces['distance'], pieces['short'])
        if pieces['dirty']:
            rendered += '.dirty'
    return rendered

def pep440_split_post(ver):
    """Split pep440 version string at the post-release segment.

    Returns the release segments before the post-release and the
    post-release version number (or -1 if no post-release segment is present).
    """
    vc = str.split(ver, '.post')
    return (vc[0], int(vc[1] or 0) if len(vc) == 2 else None)

def render_pep440_pre(pieces):
    """TAG[.postN.devDISTANCE] -- No -dirty.

    Exceptions:
    1: no tags. 0.post0.devDISTANCE
    """
    if pieces['closest-tag']:
        if pieces['distance']:
            (tag_version, post_version) = pep440_split_post(pieces['closest-tag'])
            rendered = tag_version
            if post_version is not None:
                rendered += '.post%d.dev%d' % (post_version + 1, pieces['distance'])
            else:
                rendered += '.post0.dev%d' % pieces['distance']
        else:
            rendered = pieces['closest-tag']
    else:
        rendered = '0.post0.dev%d' % pieces['distance']
    return rendered

def render_pep440_post(pieces):
    """TAG[.postDISTANCE[.dev0]+gHEX] .

    The ".dev0" means dirty. Note that .dev0 sorts backwards
    (a dirty tree will appear "older" than the corresponding clean one),
    but you shouldn't be releasing software with -dirty anyways.

    Exceptions:
    1: no tags. 0.postDISTANCE[.dev0]
    """
    if pieces['closest-tag']:
        rendered = pieces['closest-tag']
        if pieces['distance'] or pieces['dirty']:
            rendered += '.post%d' % pieces['distance']
            if pieces['dirty']:
                rendered += '.dev0'
            rendered += plus_or_dot(pieces)
            rendered += 'g%s' % pieces['short']
    else:
        rendered = '0.post%d' % pieces['distance']
        if pieces['dirty']:
            rendered += '.dev0'
        rendered += '+g%s' % pieces['short']
    return rendered

def render_pep440_post_branch(pieces):
    """TAG[.postDISTANCE[.dev0]+gHEX[.dirty]] .

    The ".dev0" means not master branch.

    Exceptions:
    1: no tags. 0.postDISTANCE[.dev0]+gHEX[.dirty]
    """
    if pieces['closest-tag']:
        rendered = pieces['closest-tag']
        if pieces['distance'] or pieces['dirty']:
            rendered += '.post%d' % pieces['distance']
            if pieces['branch'] != 'master':
                rendered += '.dev0'
            rendered += plus_or_dot(pieces)
            rendered += 'g%s' % pieces['short']
            if pieces['dirty']:
                rendered += '.dirty'
    else:
        rendered = '0.post%d' % pieces['distance']
        if pieces['branch'] != 'master':
            rendered += '.dev0'
        rendered += '+g%s' % pieces['short']
        if pieces['dirty']:
            rendered += '.dirty'
    return rendered

def render_pep440_old(pieces):
    """TAG[.postDISTANCE[.dev0]] .

    The ".dev0" means dirty.

    Exceptions:
    1: no tags. 0.postDISTANCE[.dev0]
    """
    if pieces['closest-tag']:
        rendered = pieces['closest-tag']
        if pieces['distance'] or pieces['dirty']:
            rendered += '.post%d' % pieces['distance']
            if pieces['dirty']:
                rendered += '.dev0'
    else:
        rendered = '0.post%d' % pieces['distance']
        if pieces['dirty']:
            rendered += '.dev0'
    return rendered

def render_git_describe(pieces):
    """TAG[-DISTANCE-gHEX][-dirty].

    Like 'git describe --tags --dirty --always'.

    Exceptions:
    1: no tags. HEX[-dirty]  (note: no 'g' prefix)
    """
    if pieces['closest-tag']:
        rendered = pieces['closest-tag']
        if pieces['distance']:
            rendered += '-%d-g%s' % (pieces['distance'], pieces['short'])
    else:
        rendered = pieces['short']
    if pieces['dirty']:
        rendered += '-dirty'
    return rendered

def render_git_describe_long(pieces):
    """TAG-DISTANCE-gHEX[-dirty].

    Like 'git describe --tags --dirty --always -long'.
    The distance/hash is unconditional.

    Exceptions:
    1: no tags. HEX[-dirty]  (note: no 'g' prefix)
    """
    if pieces['closest-tag']:
        rendered = pieces['closest-tag']
        rendered += '-%d-g%s' % (pieces['distance'], pieces['short'])
    else:
        rendered = pieces['short']
    if pieces['dirty']:
        rendered += '-dirty'
    return rendered

def render(pieces, style):
    """Render the given version pieces into the requested style."""
    if pieces['error']:
        return {'version': 'unknown', 'full-revisionid': pieces.get('long'), 'dirty': None, 'error': pieces['error'], 'date': None}
    if not style or style == 'default':
        style = 'pep440'
    if style == 'pep440':
        rendered = render_pep440(pieces)
    elif style == 'pep440-branch':
        rendered = render_pep440_branch(pieces)
    elif style == 'pep440-pre':
        rendered = render_pep440_pre(pieces)
    elif style == 'pep440-post':
        rendered = render_pep440_post(pieces)
    elif style == 'pep440-post-branch':
        rendered = render_pep440_post_branch(pieces)
    elif style == 'pep440-old':
        rendered = render_pep440_old(pieces)
    elif style == 'git-describe':
        rendered = render_git_describe(pieces)
    elif style == 'git-describe-long':
        rendered = render_git_describe_long(pieces)
    else:
        raise ValueError("unknown style '%s'" % style)
    return {'version': rendered, 'full-revisionid': pieces['long'], 'dirty': pieces['dirty'], 'error': None, 'date': pieces.get('date')}

class VersioneerBadRootError(Exception):
    """The project root directory is unknown or missing key files."""

def get_versions(verbose=False):
    """Get the project version from whatever source is available.

    Returns dict with two keys: 'version' and 'full'.
    """
    if 'versioneer' in sys.modules:
        del sys.modules['versioneer']
    root = get_root()
    cfg = get_config_from_root(root)
    assert cfg.VCS is not None, 'please set [versioneer]VCS= in setup.cfg'
    handlers = HANDLERS.get(cfg.VCS)
    assert handlers, "unrecognized VCS '%s'" % cfg.VCS
    verbose = verbose or cfg.verbose
    assert cfg.versionfile_source is not None, 'please set versioneer.versionfile_source'
    assert cfg.tag_prefix is not None, 'please set versioneer.tag_prefix'
    versionfile_abs = os.path.join(root, cfg.versionfile_source)
    get_keywords_f = handlers.get('get_keywords')
    from_keywords_f = handlers.get('keywords')
    if get_keywords_f and from_keywords_f:
        try:
            keywords = get_keywords_f(versionfile_abs)
            ver = from_keywords_f(keywords, cfg.tag_prefix, verbose)
            if verbose:
                print('got version from expanded keyword %s' % ver)
            return ver
        except NotThisMethod:
            pass
    try:
        ver = versions_from_file(versionfile_abs)
        if verbose:
            print('got version from file %s %s' % (versionfile_abs, ver))
        return ver
    except NotThisMethod:
        pass
    from_vcs_f = handlers.get('pieces_from_vcs')
    if from_vcs_f:
        try:
            pieces = from_vcs_f(cfg.tag_prefix, root, verbose)
            ver = render(pieces, cfg.style)
            if verbose:
                print('got version from VCS %s' % ver)
            return ver
        except NotThisMethod:
            pass
    try:
        if cfg.parentdir_prefix:
            ver = versions_from_parentdir(cfg.parentdir_prefix, root, verbose)
            if verbose:
                print('got version from parentdir %s' % ver)
            return ver
    except NotThisMethod:
        pass
    if verbose:
        print('unable to compute version')
    return {'version': '0+unknown', 'full-revisionid': None, 'dirty': None, 'error': 'unable to compute version', 'date': None}

def get_version():
    """Get the short version string for this project."""
    return get_versions()['version']

def get_cmdclass(cmdclass=None):
    """Get the custom setuptools/distutils subclasses used by Versioneer.

    If the package uses a different cmdclass (e.g. one from numpy), it
    should be provide as an argument.
    """
    if 'versioneer' in sys.modules:
        del sys.modules['versioneer']
    cmds = {} if cmdclass is None else cmdclass.copy()
    try:
        from setuptools import Command
    except ImportError:
        from distutils.core import Command

    class cmd_version(Command):
        description = 'report generated version string'
        user_options = []
        boolean_options = []

        def initialize_options(self):
            pass

        def finalize_options(self):
            pass

        def run(self):
            vers = get_versions(verbose=True)
            print('Version: %s' % vers['version'])
            print(' full-revisionid: %s' % vers.get('full-revisionid'))
            print(' dirty: %s' % vers.get('dirty'))
            print(' date: %s' % vers.get('date'))
            if vers['error']:
                print(' error: %s' % vers['error'])
    cmds['version'] = cmd_version
    if 'build_py' in cmds:
        _build_py = cmds['build_py']
    elif 'setuptools' in sys.modules:
        from setuptools.command.build_py import build_py as _build_py
    else:
        from distutils.command.build_py import build_py as _build_py

    class cmd_build_py(_build_py):

        def run(self):
            root = get_root()
            cfg = get_config_from_root(root)
            versions = get_versions()
            _build_py.run(self)
            if cfg.versionfile_build:
                target_versionfile = os.path.join(self.build_lib, cfg.versionfile_build)
                print('UPDATING %s' % target_versionfile)
                write_to_version_file(target_versionfile, versions)
    cmds['build_py'] = cmd_build_py
    if 'build_ext' in cmds:
        _build_ext = cmds['build_ext']
    elif 'setuptools' in sys.modules:
        from setuptools.command.build_ext import build_ext as _build_ext
    else:
        from distutils.command.build_ext import build_ext as _build_ext

    class cmd_build_ext(_build_ext):

        def run(self):
            root = get_root()
            cfg = get_config_from_root(root)
            versions = get_versions()
            _build_ext.run(self)
            if self.inplace:
                return
            target_versionfile = os.path.join(self.build_lib, cfg.versionfile_build)
            print('UPDATING %s' % target_versionfile)
            write_to_version_file(target_versionfile, versions)
    cmds['build_ext'] = cmd_build_ext
    if 'cx_Freeze' in sys.modules:
        from cx_Freeze.dist import build_exe as _build_exe

        class cmd_build_exe(_build_exe):

            def run(self):
                root = get_root()
                cfg = get_config_from_root(root)
                versions = get_versions()
                target_versionfile = cfg.versionfile_source
                print('UPDATING %s' % target_versionfile)
                write_to_version_file(target_versionfile, versions)
                _build_exe.run(self)
                os.unlink(target_versionfile)
                with open(cfg.versionfile_source, 'w') as f:
                    LONG = LONG_VERSION_PY[cfg.VCS]
                    f.write(LONG % {'DOLLAR': '$', 'STYLE': cfg.style, 'TAG_PREFIX': cfg.tag_prefix, 'PARENTDIR_PREFIX': cfg.parentdir_prefix, 'VERSIONFILE_SOURCE': cfg.versionfile_source})
        cmds['build_exe'] = cmd_build_exe
        del cmds['build_py']
    if 'py2exe' in sys.modules:
        from py2exe.distutils_buildexe import py2exe as _py2exe

        class cmd_py2exe(_py2exe):

            def run(self):
                root = get_root()
                cfg = get_config_from_root(root)
                versions = get_versions()
                target_versionfile = cfg.versionfile_source
                print('UPDATING %s' % target_versionfile)
                write_to_version_file(target_versionfile, versions)
                _py2exe.run(self)
                os.unlink(target_versionfile)
                with open(cfg.versionfile_source, 'w') as f:
                    LONG = LONG_VERSION_PY[cfg.VCS]
                    f.write(LONG % {'DOLLAR': '$', 'STYLE': cfg.style, 'TAG_PREFIX': cfg.tag_prefix, 'PARENTDIR_PREFIX': cfg.parentdir_prefix, 'VERSIONFILE_SOURCE': cfg.versionfile_source})
        cmds['py2exe'] = cmd_py2exe
    if 'sdist' in cmds:
        _sdist = cmds['sdist']
    elif 'setuptools' in sys.modules:
        from setuptools.command.sdist import sdist as _sdist
    else:
        from distutils.command.sdist import sdist as _sdist

    class cmd_sdist(_sdist):

        def run(self):
            versions = get_versions()
            self._versioneer_generated_versions = versions
            self.distribution.metadata.version = versions['version']
            return _sdist.run(self)

        def make_release_tree(self, base_dir, files):
            root = get_root()
            cfg = get_config_from_root(root)
            _sdist.make_release_tree(self, base_dir, files)
            target_versionfile = os.path.join(base_dir, cfg.versionfile_source)
            print('UPDATING %s' % target_versionfile)
            write_to_version_file(target_versionfile, self._versioneer_generated_versions)
    cmds['sdist'] = cmd_sdist
    return cmds
CONFIG_ERROR = "\nsetup.cfg is missing the necessary Versioneer configuration. You need\na section like:\n\n [versioneer]\n VCS = git\n style = pep440\n versionfile_source = src/myproject/_version.py\n versionfile_build = myproject/_version.py\n tag_prefix =\n parentdir_prefix = myproject-\n\nYou will also need to edit your setup.py to use the results:\n\n import versioneer\n setup(version=versioneer.get_version(),\n       cmdclass=versioneer.get_cmdclass(), ...)\n\nPlease read the docstring in ./versioneer.py for configuration instructions,\nedit setup.cfg, and re-run the installer or 'python versioneer.py setup'.\n"
SAMPLE_CONFIG = "\n# See the docstring in versioneer.py for instructions. Note that you must\n# re-run 'versioneer.py setup' after changing this section, and commit the\n# resulting files.\n\n[versioneer]\n#VCS = git\n#style = pep440\n#versionfile_source =\n#versionfile_build =\n#tag_prefix =\n#parentdir_prefix =\n\n"
OLD_SNIPPET = "\nfrom ._version import get_versions\n__version__ = get_versions()['version']\ndel get_versions\n"
INIT_PY_SNIPPET = "\nfrom . import {0}\n__version__ = {0}.get_versions()['version']\n"

def do_setup():
    """Do main VCS-independent setup function for installing Versioneer."""
    root = get_root()
    try:
        cfg = get_config_from_root(root)
    except (OSError, configparser.NoSectionError, configparser.NoOptionError) as e:
        if isinstance(e, (OSError, configparser.NoSectionError)):
            print('Adding sample versioneer config to setup.cfg', file=sys.stderr)
            with open(os.path.join(root, 'setup.cfg'), 'a') as f:
                f.write(SAMPLE_CONFIG)
        print(CONFIG_ERROR, file=sys.stderr)
        return 1
    print(' creating %s' % cfg.versionfile_source)
    with open(cfg.versionfile_source, 'w') as f:
        LONG = LONG_VERSION_PY[cfg.VCS]
        f.write(LONG % {'DOLLAR': '$', 'STYLE': cfg.style, 'TAG_PREFIX': cfg.tag_prefix, 'PARENTDIR_PREFIX': cfg.parentdir_prefix, 'VERSIONFILE_SOURCE': cfg.versionfile_source})
    ipy = os.path.join(os.path.dirname(cfg.versionfile_source), '__init__.py')
    if os.path.exists(ipy):
        try:
            with open(ipy, 'r') as f:
                old = f.read()
        except OSError:
            old = ''
        module = os.path.splitext(os.path.basename(cfg.versionfile_source))[0]
        snippet = INIT_PY_SNIPPET.format(module)
        if OLD_SNIPPET in old:
            print(' replacing boilerplate in %s' % ipy)
            with open(ipy, 'w') as f:
                f.write(old.replace(OLD_SNIPPET, snippet))
        elif snippet not in old:
            print(' appending to %s' % ipy)
            with open(ipy, 'a') as f:
                f.write(snippet)
        else:
            print(' %s unmodified' % ipy)
    else:
        print(" %s doesn't exist, ok" % ipy)
        ipy = None
    manifest_in = os.path.join(root, 'MANIFEST.in')
    simple_includes = set()
    try:
        with open(manifest_in, 'r') as f:
            for line in f:
                if line.startswith('include '):
                    for include in line.split()[1:]:
                        simple_includes.add(include)
    except OSError:
        pass
    if 'versioneer.py' not in simple_includes:
        print(" appending 'versioneer.py' to MANIFEST.in")
        with open(manifest_in, 'a') as f:
            f.write('include versioneer.py\n')
    else:
        print(" 'versioneer.py' already in MANIFEST.in")
    if cfg.versionfile_source not in simple_includes:
        print(" appending versionfile_source ('%s') to MANIFEST.in" % cfg.versionfile_source)
        with open(manifest_in, 'a') as f:
            f.write('include %s\n' % cfg.versionfile_source)
    else:
        print(' versionfile_source already in MANIFEST.in')
    do_vcs_install(manifest_in, cfg.versionfile_source, ipy)
    return 0

def scan_setup_py():
    """Validate the contents of setup.py against Versioneer's expectations."""
    found = set()
    setters = False
    errors = 0
    with open('setup.py', 'r') as f:
        for line in f.readlines():
            if 'import versioneer' in line:
                found.add('import')
            if 'versioneer.get_cmdclass()' in line:
                found.add('cmdclass')
            if 'versioneer.get_version()' in line:
                found.add('get_version')
            if 'versioneer.VCS' in line:
                setters = True
            if 'versioneer.versionfile_source' in line:
                setters = True
    if len(found) != 3:
        print('')
        print('Your setup.py appears to be missing some important items')
        print('(but I might be wrong). Please make sure it has something')
        print('roughly like the following:')
        print('')
        print(' import versioneer')
        print(' setup( version=versioneer.get_version(),')
        print('        cmdclass=versioneer.get_cmdclass(),  ...)')
        print('')
        errors += 1
    if setters:
        print("You should remove lines like 'versioneer.VCS = ' and")
        print("'versioneer.versionfile_source = ' . This configuration")
        print('now lives in setup.cfg, and should be removed from setup.py')
        print('')
        errors += 1
    return errors
if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'setup':
        errors = do_setup()
        errors += scan_setup_py()
        if errors:
            sys.exit(1)