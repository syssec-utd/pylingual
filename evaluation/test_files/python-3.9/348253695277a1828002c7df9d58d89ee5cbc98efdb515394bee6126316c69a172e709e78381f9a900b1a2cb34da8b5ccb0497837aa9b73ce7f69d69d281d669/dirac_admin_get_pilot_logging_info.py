"""
Retrieve logging info of a Grid pilot

Example:
  $ dirac-admin-get-pilot-logging-info https://marlb.in2p3.fr:9000/26KCLKBFtxXKHF4_ZrQjkw
  Pilot Reference: dirac-admin-get-pilot-logging-info https://marlb.in2p3.fr:9000/26KCLKBFtxXKHF4_ZrQjkw
  ===================== glite-job-logging-info Success =====================
  LOGGING INFORMATION:
  Printing info for the Job : https://marlb.in2p3.fr:9000/26KCLKBFtxXKHF4_ZrQjkw
      ---
  Event: RegJob
  - Arrived   =  Mon Feb 21 13:27:50 2011 CET
  - Host      =  marwms.in2p3.fr
  - Jobtype   =  SIMPLE
  - Level     =  SYSTEM
  - Ns        =  https://marwms.in2p3.fr:7443/glite_wms_wmproxy_server
  - Nsubjobs  =  0
  - Parent    =  https://marlb.in2p3.fr:9000/WQHVOB1mI4oqrlYz2ZKtgA
  - Priority  =  asynchronous
  - Seqcode   =  UI=000000:NS=0000000001:WM=000000:BH=0000000000:JSS=000000:LM=000000:LRMS=000000:APP=000000:LBS=000000
  - Source    =  NetworkServer
"""
from DIRAC.Core.Base.Script import Script

@Script()
def main():
    Script.registerArgument(['PilotID:  Grid ID of the pilot'])
    (_, args) = Script.parseCommandLine(ignoreErrors=True)
    from DIRAC import exit as DIRACExit
    from DIRAC.Interfaces.API.DiracAdmin import DiracAdmin
    diracAdmin = DiracAdmin()
    exitCode = 0
    errorList = []
    for gridID in args:
        result = diracAdmin.getPilotLoggingInfo(gridID)
        if not result['OK']:
            errorList.append((gridID, result['Message']))
            exitCode = 2
        else:
            print('Pilot Reference: %s', gridID)
            print(result['Value'])
            print()
    for error in errorList:
        print('ERROR %s: %s' % error)
    DIRACExit(exitCode)
if __name__ == '__main__':
    main()