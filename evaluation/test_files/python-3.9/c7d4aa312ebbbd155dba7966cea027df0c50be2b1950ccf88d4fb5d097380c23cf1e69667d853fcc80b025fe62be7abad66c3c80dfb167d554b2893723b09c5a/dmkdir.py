"""
Creates a directory in the FileCatalog.
Takes either an absolute path or a path relative to the
user's current file catalogue directory.

Examples:
    $ dmkdir some_lfn_dir (relative path)
    $ dmkdir ./some_lfn_dir (relative path)
    $ dmkdir /voname/somesubdir/anotherone/newdir
"""
from DIRAC.Interfaces.Utilities.DCommands import DSession
from DIRAC.Interfaces.Utilities.DCommands import DCatalog
from DIRAC.Interfaces.Utilities.DCommands import pathFromArguments
from DIRAC.Interfaces.Utilities.DCommands import createCatalog
from DIRAC.Interfaces.Utilities.DConfigCache import ConfigCache
from DIRAC.Core.Base.Script import Script

@Script()
def main():
    configCache = ConfigCache()
    Script.registerArgument(['Path: path to new directory'])
    Script.parseCommandLine(ignoreErrors=True)
    configCache.cacheConfig()
    args = Script.getPositionalArgs()
    session = DSession()
    catalog = createCatalog()
    result = catalog.createDirectory(pathFromArguments(session, args))
    if result['OK']:
        if result['Value']['Failed']:
            for p in result['Value']['Failed']:
                print(f'ERROR - "{p}":', result['Value']['Failed'][p])
    else:
        print('ERROR:', result['Message'])
if __name__ == '__main__':
    main()