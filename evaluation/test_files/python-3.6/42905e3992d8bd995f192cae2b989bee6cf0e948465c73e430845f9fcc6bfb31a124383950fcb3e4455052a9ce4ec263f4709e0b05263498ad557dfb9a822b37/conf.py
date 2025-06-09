import datetime
import glob
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
from importlib.metadata import version
setupVersion = version('pygithub')
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.coverage', 'sphinx.ext.mathjax']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = 'PyGithub'
copyright = '%d, Vincent Jacques' % datetime.date.today().year
version = setupVersion
release = setupVersion
exclude_patterns = []
pygments_style = 'sphinx'
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
htmlhelp_basename = 'PyGithubdoc'
latex_documents = [('index', 'PyGithub.tex', 'PyGithub Documentation', 'Vincent Jacques', 'manual')]
man_pages = [('index', 'pygithub', 'PyGithub Documentation', ['Vincent Jacques'], 1)]
texinfo_documents = [('index', 'PyGithub', 'PyGithub Documentation', 'Vincent Jacques', 'PyGithub', 'One line description of project.', 'Miscellaneous')]
autodoc_default_flags = ['members']
autodoc_member_order = 'bysource'
autoclass_content = 'both'
githubClasses = [fileName[10:-3] for fileName in sorted(glob.glob('../github/*.py')) if fileName not in ['../github/GithubException.py', '../github/GithubObject.py', '../github/InputFileContent.py', '../github/InputGitAuthor.py', '../github/InputGitTreeElement.py', '../github/Legacy.py', '../github/MainClass.py', '../github/PaginatedList.py', '../github/Requester.py', '../github/Consts.py', '../github/__init__.py']]
with open('github_objects.rst', 'w') as f:
    f.write('Github objects\n')
    f.write('==============\n')
    f.write('\n')
    f.write('.. autoclass:: github.GithubObject.GithubObject()\n')
    f.write('\n')
    f.write('.. toctree::\n')
    for githubClass in githubClasses:
        f.write('   github_objects/' + githubClass + '\n')
for githubClass in githubClasses:
    with open('github_objects/' + githubClass + '.rst', 'w') as f:
        f.write(githubClass + '\n')
        f.write('=' * len(githubClass) + '\n')
        f.write('\n')
        f.write('.. autoclass:: github.' + githubClass + '.' + githubClass + '()\n')
methods = dict()
for githubClass in githubClasses + ['MainClass']:
    with open('../github/' + githubClass + '.py') as f:
        if githubClass == 'MainClass':
            githubClass = 'github.MainClass.Github'
        else:
            githubClass = 'github.' + githubClass + '.' + githubClass
        method = None
        isProperty = False
        for line in f:
            line = line.rstrip()
            if line == '    @property':
                isProperty = True
            if line.startswith('    def '):
                if not isProperty:
                    method = line.split('(')[0][8:]
                    if method in ['_initAttributes', '_useAttributes', '__init__', '__create_pull_1', '__create_pull_2', '__create_pull', '_hub', '__get_FIX_REPO_GET_GIT_REF', '__set_FIX_REPO_GET_GIT_REF', '__get_per_page', '__set_per_page', 'create_from_raw_data', 'dump', 'load']:
                        method = None
                isProperty = False
            if line.startswith('        :calls: `'):
                for callee in line[16:].split(' or '):
                    (verb, url) = callee[1:].split(' ')[0:2]
                    if url not in methods:
                        methods[url] = dict()
                    if verb not in methods[url]:
                        methods[url][verb] = set()
                    methods[url][verb].add(':meth:`' + githubClass + '.' + method + '`')
                method = None
methods['/markdown/raw'] = dict()
methods['/markdown/raw']['POST'] = ['Not implemented, see ``/markdown``']
methods['/rate_limit'] = dict()
methods['/rate_limit']['GET'] = ['Not implemented, see `Github.rate_limiting`']
with open('apis.rst', 'w') as apis:
    apis.write('APIs\n')
    apis.write('====\n')
    apis.write('\n')
    for (url, verbs) in sorted(methods.items()):
        apis.write('* ``' + url + '``\n')
        apis.write('\n')
        for verb in ['GET', 'PATCH', 'POST', 'PUT', 'DELETE']:
            if verb in verbs:
                apis.write('  * ' + verb + ': ' + ' or '.join(sorted(verbs[verb])) + '\n')
        apis.write('\n')