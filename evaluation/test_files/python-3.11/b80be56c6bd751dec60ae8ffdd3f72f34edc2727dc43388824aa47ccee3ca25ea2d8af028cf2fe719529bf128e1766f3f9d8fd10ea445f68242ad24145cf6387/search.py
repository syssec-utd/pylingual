import difflib
import re
import portage
from portage import os
from portage.dbapi.porttree import _parse_uri_map
from portage.dbapi.IndexedPortdb import IndexedPortdb
from portage.dbapi.IndexedVardb import IndexedVardb
from portage.exception import InvalidBinaryPackageFormat
from portage.localization import localized_size
from portage.output import bold, darkgreen, green, red
from portage.util import writemsg_stdout
from portage.util.iterators.MultiIterGroupBy import MultiIterGroupBy
from _emerge.Package import Package

class search:
    VERSION_SHORT = 1
    VERSION_RELEASE = 2

    def __init__(self, root_config, spinner, searchdesc, verbose, usepkg, usepkgonly, search_index=True, search_similarity=None, fuzzy=True, regex_auto=False):
        """Searches the available and installed packages for the supplied search key.
        The list of available and installed packages is created at object instantiation.
        This makes successive searches faster."""
        self.settings = root_config.settings
        self.verbose = verbose
        self.searchdesc = searchdesc
        self.searchkey = None
        self._results_specified = False
        self.spinner = None
        self.root_config = root_config
        self.setconfig = root_config.setconfig
        self.regex_auto = regex_auto
        self.fuzzy = fuzzy
        self.search_similarity = 80 if search_similarity is None else search_similarity
        self.matches = {'pkg': []}
        self.mlen = 0
        self._dbs = []
        portdb = root_config.trees['porttree'].dbapi
        bindb = root_config.trees['bintree'].dbapi
        vardb = root_config.trees['vartree'].dbapi
        if search_index:
            portdb = IndexedPortdb(portdb)
            vardb = IndexedVardb(vardb)
        if not usepkgonly and portdb._have_root_eclass_dir:
            self._dbs.append(portdb)
        if (usepkg or usepkgonly) and bindb.cp_all():
            self._dbs.append(bindb)
        self._dbs.append(vardb)
        self._portdb = portdb
        self._vardb = vardb

    def _spinner_update(self):
        if self.spinner:
            self.spinner.update()

    def _cp_all(self):
        iterators = []
        for db in self._dbs:
            i = db.cp_all(sort=True)
            try:
                i = iter(i)
            except TypeError:
                pass
            iterators.append(i)
        for group in MultiIterGroupBy(iterators):
            yield group[0]

    def _aux_get(self, *args, **kwargs):
        for db in self._dbs:
            try:
                return db.aux_get(*args, **kwargs)
            except KeyError:
                pass
        raise KeyError(args[0])

    def _aux_get_error(self, cpv):
        portage.writemsg("emerge: search: aux_get('%s') failed, skipping\n" % cpv, noiselevel=-1)

    def _findname(self, *args, **kwargs):
        for db in self._dbs:
            if db is not self._portdb:
                continue
            func = getattr(db, 'findname', None)
            if func:
                value = func(*args, **kwargs)
                if value:
                    return value
        return None

    def _getFetchMap(self, *args, **kwargs):
        for db in self._dbs:
            func = getattr(db, 'getFetchMap', None)
            if func:
                value = func(*args, **kwargs)
                if value:
                    return value
        return {}

    def _visible(self, db, cpv, metadata):
        installed = db is self._vardb
        built = installed or db is not self._portdb
        pkg_type = 'ebuild'
        if installed:
            pkg_type = 'installed'
        elif built:
            pkg_type = 'binary'
        return Package(type_name=pkg_type, root_config=self.root_config, cpv=cpv, built=built, installed=installed, metadata=metadata).visible

    def _first_cp(self, cp):
        for db in self._dbs:
            if hasattr(db, 'cp_list'):
                matches = db.cp_list(cp)
                if matches:
                    return matches[-1]
            else:
                matches = db.match(cp)
            for cpv in matches:
                if cpv.cp == cp:
                    return cpv
        return None

    def _xmatch(self, level, atom):
        """
        This method does not expand old-style virtuals because it
        is restricted to returning matches for a single ${CATEGORY}/${PN}
        and old-style virual matches unreliable for that when querying
        multiple package databases. If necessary, old-style virtuals
        can be performed on atoms prior to calling this method.
        """
        if not isinstance(atom, portage.dep.Atom):
            atom = portage.dep.Atom(atom)
        cp = atom.cp
        if level == 'match-all':
            matches = set()
            for db in self._dbs:
                if hasattr(db, 'xmatch'):
                    matches.update(db.xmatch(level, atom))
                else:
                    matches.update(db.match(atom))
            result = list((x for x in matches if portage.cpv_getkey(x) == cp))
            db._cpv_sort_ascending(result)
        elif level == 'match-visible':
            matches = set()
            for db in self._dbs:
                if hasattr(db, 'xmatch'):
                    matches.update(db.xmatch(level, atom))
                else:
                    db_keys = list(db._aux_cache_keys)
                    for cpv in db.match(atom):
                        try:
                            metadata = zip(db_keys, db.aux_get(cpv, db_keys))
                        except KeyError:
                            self._aux_get_error(cpv)
                            continue
                        if not self._visible(db, cpv, metadata):
                            continue
                        matches.add(cpv)
            result = list((x for x in matches if portage.cpv_getkey(x) == cp))
            db._cpv_sort_ascending(result)
        elif level == 'bestmatch-visible':
            result = None
            for db in self._dbs:
                if hasattr(db, 'xmatch'):
                    cpv = db.xmatch('bestmatch-visible', atom)
                    if not cpv or portage.cpv_getkey(cpv) != cp:
                        continue
                    if not result or cpv == portage.best([cpv, result]):
                        result = cpv
                else:
                    db_keys = list(db._aux_cache_keys)
                    matches = db.match(atom)
                    try:
                        db.match_unordered
                    except AttributeError:
                        pass
                    else:
                        db._cpv_sort_ascending(matches)
                    for cpv in reversed(matches):
                        if portage.cpv_getkey(cpv) != cp:
                            continue
                        try:
                            metadata = zip(db_keys, db.aux_get(cpv, db_keys))
                        except KeyError:
                            self._aux_get_error(cpv)
                            continue
                        if not self._visible(db, cpv, metadata):
                            continue
                        if not result or cpv == portage.best([cpv, result]):
                            result = cpv
                        break
        else:
            raise NotImplementedError(level)
        return result

    def execute(self, searchkey):
        """Performs the search for the supplied search key"""
        self.searchkey = searchkey

    def _iter_search(self):
        match_category = 0
        self.packagematches = []
        if self.searchdesc:
            self.searchdesc = 1
            self.matches = {'pkg': [], 'desc': [], 'set': []}
        else:
            self.searchdesc = 0
            self.matches = {'pkg': [], 'set': []}
        writemsg_stdout('Searching...\n\n', noiselevel=-1)
        regexsearch = False
        if self.searchkey.startswith('%'):
            regexsearch = True
            self.searchkey = self.searchkey[1:]
        if self.searchkey.startswith('@'):
            match_category = 1
            self.searchkey = self.searchkey[1:]
        if '/' in self.searchkey:
            match_category = 1
        fuzzy = False
        if self.regex_auto and (not regexsearch) and (re.search('[\\^\\$\\*\\[\\]\\{\\}\\|\\?]|\\.\\+', self.searchkey) is not None):
            try:
                re.compile(self.searchkey, re.I)
            except Exception:
                pass
            else:
                regexsearch = True
        if regexsearch:
            self.searchre = re.compile(self.searchkey, re.I)
        else:
            self.searchre = re.compile(re.escape(self.searchkey), re.I)
            if self.fuzzy:
                fuzzy = True
                cutoff = float(self.search_similarity) / 100
                if match_category:
                    part_split = portage.catsplit
                else:
                    part_split = lambda match_string: (match_string,)
                part_matchers = []
                for part in part_split(self.searchkey):
                    seq_match = difflib.SequenceMatcher()
                    seq_match.set_seq2(part.lower())
                    part_matchers.append(seq_match)

                def fuzzy_search_part(seq_match, match_string):
                    seq_match.set_seq1(match_string.lower())
                    return seq_match.real_quick_ratio() >= cutoff and seq_match.quick_ratio() >= cutoff and (seq_match.ratio() >= cutoff)

                def fuzzy_search(match_string):
                    return all((fuzzy_search_part(seq_match, part) for seq_match, part in zip(part_matchers, part_split(match_string))))
        for package in self._cp_all():
            self._spinner_update()
            if match_category:
                match_string = package[:]
            else:
                match_string = package.split('/')[-1]
            if self.searchre.search(match_string):
                yield ('pkg', package)
            elif fuzzy and fuzzy_search(match_string):
                yield ('pkg', package)
            elif self.searchdesc:
                full_package = self._first_cp(package)
                if not full_package:
                    continue
                try:
                    full_desc = self._aux_get(full_package, ['DESCRIPTION'])[0]
                except KeyError:
                    self._aux_get_error(full_package)
                    continue
                if not self.searchre.search(full_desc):
                    continue
                yield ('desc', package)
        self.sdict = self.setconfig.getSets()
        for setname in self.sdict:
            self._spinner_update()
            if match_category:
                match_string = setname
            else:
                match_string = setname.split('/')[-1]
            if self.searchre.search(match_string):
                yield ('set', setname)
            elif self.searchdesc:
                if self.searchre.search(self.sdict[setname].getMetadata('DESCRIPTION')):
                    yield ('set', setname)

    def addCP(self, cp):
        """
        Add a specific cp to the search results. This modifies the
        behavior of the output method, so that it only displays specific
        packages added via this method.
        """
        self._results_specified = True
        if not self._xmatch('match-all', cp):
            return
        self.matches['pkg'].append(cp)
        self.mlen += 1

    def output(self):
        """Outputs the results of the search."""

        class msg:

            @staticmethod
            def append(msg):
                writemsg_stdout(msg, noiselevel=-1)
        msg.append('\x08\x08  \n[ Results for search key : ' + bold(self.searchkey) + ' ]\n')
        vardb = self._vardb
        metadata_keys = set(Package.metadata_keys)
        metadata_keys.update(['DESCRIPTION', 'HOMEPAGE', 'LICENSE', 'SRC_URI'])
        metadata_keys = tuple(metadata_keys)
        if self._results_specified:
            addCP_matches = []
            for mytype, matches in self.matches.items():
                for match in matches:
                    addCP_matches.append((mytype, match))
            iterator = iter(addCP_matches)
        else:
            iterator = self._iter_search()
        for mtype, match in iterator:
            self.mlen += 1
            masked = False
            full_package = None
            if mtype in ('pkg', 'desc'):
                full_package = self._xmatch('bestmatch-visible', match)
                if not full_package:
                    masked = True
                    full_package = self._xmatch('match-all', match)
                    if full_package:
                        full_package = full_package[-1]
            elif mtype == 'set':
                msg.append(green('*') + '  ' + bold(match) + '\n')
                if self.verbose:
                    msg.append('      ' + darkgreen('Description:') + '   ' + self.sdict[match].getMetadata('DESCRIPTION') + '\n\n')
            if full_package:
                try:
                    metadata = dict(zip(metadata_keys, self._aux_get(full_package, metadata_keys)))
                except KeyError:
                    self._aux_get_error(full_package)
                    continue
                desc = metadata['DESCRIPTION']
                homepage = metadata['HOMEPAGE']
                license = metadata['LICENSE']
                if masked:
                    msg.append(green('*') + '  ' + bold(match) + ' ' + red('[ Masked ]') + '\n')
                else:
                    msg.append(green('*') + '  ' + bold(match) + '\n')
                myversion = self.getVersion(full_package, search.VERSION_RELEASE)
                mysum = [0, 0]
                file_size_str = None
                mycat = match.split('/')[0]
                mypkg = match.split('/')[1]
                mycpv = match + '-' + myversion
                myebuild = self._findname(mycpv)
                if myebuild:
                    pkg = Package(built=False, cpv=mycpv, installed=False, metadata=metadata, root_config=self.root_config, type_name='ebuild')
                    pkgdir = os.path.dirname(myebuild)
                    mf = self.settings.repositories.get_repo_for_location(os.path.dirname(os.path.dirname(pkgdir)))
                    mf = mf.load_manifest(pkgdir, self.settings['DISTDIR'])
                    try:
                        uri_map = _parse_uri_map(mycpv, metadata, use=pkg.use.enabled)
                    except portage.exception.InvalidDependString as e:
                        file_size_str = 'Unknown ({})'.format(e)
                        del e
                    else:
                        try:
                            mysum[0] = mf.getDistfilesSize(uri_map)
                        except KeyError as e:
                            file_size_str = 'Unknown (missing ' + 'digest for {})'.format(e)
                            del e
                available = False
                for db in self._dbs:
                    if db is not vardb and db.cpv_exists(mycpv):
                        available = True
                        if not myebuild and hasattr(db, 'bintree'):
                            try:
                                myebuild = db.bintree.getname(mycpv)
                            except InvalidBinaryPackageFormat:
                                break
                            try:
                                mysum[0] = os.stat(myebuild).st_size
                            except OSError:
                                myebuild = None
                        break
                if myebuild and file_size_str is None:
                    file_size_str = localized_size(mysum[0])
                if self.verbose:
                    if available:
                        msg.append('      %s %s\n' % (darkgreen('Latest version available:'), myversion))
                    msg.append('      %s\n' % self.getInstallationStatus(mycat + '/' + mypkg))
                    if myebuild:
                        msg.append('      %s %s\n' % (darkgreen('Size of files:'), file_size_str))
                    msg.append('      ' + darkgreen('Homepage:') + '      ' + homepage + '\n')
                    msg.append('      ' + darkgreen('Description:') + '   ' + desc + '\n')
                    msg.append('      ' + darkgreen('License:') + '       ' + license + '\n\n')
        msg.append('[ Applications found : ' + bold(str(self.mlen)) + ' ]\n\n')
        self.mlen = 0

    def getInstallationStatus(self, package):
        if not isinstance(package, portage.dep.Atom):
            package = portage.dep.Atom(package)
        installed_package = self._vardb.match(package)
        if installed_package:
            try:
                self._vardb.match_unordered
            except AttributeError:
                installed_package = installed_package[-1]
            else:
                installed_package = portage.best(installed_package)
        else:
            installed_package = ''
        result = ''
        version = self.getVersion(installed_package, search.VERSION_RELEASE)
        if len(version) > 0:
            result = darkgreen('Latest version installed:') + ' ' + version
        else:
            result = darkgreen('Latest version installed:') + ' [ Not Installed ]'
        return result

    def getVersion(self, full_package, detail):
        if len(full_package) > 1:
            package_parts = portage.catpkgsplit(full_package)
            if detail == search.VERSION_RELEASE and package_parts[3] != 'r0':
                result = package_parts[2] + '-' + package_parts[3]
            else:
                result = package_parts[2]
        else:
            result = ''
        return result