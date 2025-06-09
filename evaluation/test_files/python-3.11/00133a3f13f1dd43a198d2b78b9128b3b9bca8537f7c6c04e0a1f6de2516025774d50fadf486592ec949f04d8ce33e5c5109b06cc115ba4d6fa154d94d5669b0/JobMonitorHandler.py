import json
import datetime
from DIRAC import gConfig, gLogger
from DIRAC.Core.Utilities import DictCache
from DIRAC.Core.Utilities.Graphs.Palette import Palette
from DIRAC.RequestManagementSystem.Client.Request import Request
from DIRAC.RequestManagementSystem.Client.ReqClient import ReqClient
from DIRAC.WorkloadManagementSystem.Client.JobMonitoringClient import JobMonitoringClient
from DIRAC.WorkloadManagementSystem.Client.JobManagerClient import JobManagerClient
from DIRAC.WorkloadManagementSystem.Client.PilotManagerClient import PilotManagerClient
from DIRAC.WorkloadManagementSystem.Client.WMSAdministratorClient import WMSAdministratorClient
from DIRAC.WorkloadManagementSystem.Client.SandboxStoreClient import SandboxStoreClient
from WebAppDIRAC.Lib.WebHandler import WebHandler, WErr

class JobMonitorHandler(WebHandler):
    DEFAULT_AUTHORIZATION = 'authenticated'
    __dataCache = DictCache.DictCache()

    def web_getJobData(self):
        req = self._request()
        result = JobMonitoringClient().getJobPageSummaryWeb(req, self.globalSort, self.pageNumber, self.numberOfJobs)
        if not result['OK']:
            return {'success': 'false', 'result': [], 'total': 0, 'error': result['Message']}
        result = result['Value']
        if 'TotalRecords' not in result:
            return {'success': 'false', 'result': [], 'total': -1, 'error': 'Data structure is corrupted'}
        if not result['TotalRecords']:
            return {'success': 'false', 'result': [], 'total': 0, 'error': 'There were no data matching your selection'}
        if 'ParameterNames' not in result or 'Records' not in result:
            return {'success': 'false', 'result': [], 'total': -1, 'error': 'Data structure is corrupted'}
        if not result['ParameterNames']:
            return {'success': 'false', 'result': [], 'total': -1, 'error': 'ParameterNames field is missing'}
        if not result['Records']:
            return {'success': 'false', 'result': [], 'total': 0, 'Message': 'There are no data to display'}
        callback = []
        jobs = result['Records']
        head = result['ParameterNames']
        headLength = len(head)
        for i in jobs:
            tmp = {}
            for j in range(0, headLength):
                tmp[head[j]] = i[j]
            callback.append(tmp)
        total = result['TotalRecords']
        extra = None
        if 'Extras' in result:
            extra = result['Extras']
            timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M [UTC]')
            extra['date'] = timestamp
        return {'success': 'true', 'result': callback, 'total': total, 'extra': extra}

    def web_getSelectionData(self):
        callback = {}
        user = self.getUserName()
        if not self.isRegisteredUser():
            callback['prod'] = [['Insufficient rights']]
        else:
            cacheKey = (self.getUserGroup(), self.getUserSetup())
            callback = JobMonitorHandler.__dataCache.get(cacheKey)
            if not callback:
                callback = {}
                result = JobMonitoringClient().getJobGroups()
                if result['OK']:
                    prod = []
                    prods = result['Value']
                    if prods:
                        prods.sort(reverse=True)
                        prod = [[i] for i in prods]
                    else:
                        prod = [['Nothing to display']]
                else:
                    gLogger.error(f"JobMonitoringClient().getJobGroups() return error: {result['Message']}")
                    prod = [['Error happened on service side']]
                callback['prod'] = prod
                result = JobMonitoringClient().getSites()
                if result['OK']:
                    tier1 = gConfig.getValue('/WebApp/PreferredSites', [])
                    site = []
                    if result['Value']:
                        s = list(result['Value'])
                        for i in tier1:
                            site.append([str(i)])
                        for i in s:
                            if i not in tier1:
                                site.append([str(i)])
                    else:
                        site = [['Nothing to display']]
                else:
                    gLogger.error(f"JobMonitoringClient().getSites() return error: {result['Message']}")
                    site = [['Error happened on service side']]
                callback['site'] = site
                result = JobMonitoringClient().getStates()
                if result['OK']:
                    stat = []
                    if result['Value']:
                        for i in result['Value']:
                            stat.append([str(i)])
                    else:
                        stat = [['Nothing to display']]
                else:
                    gLogger.error(f"JobMonitoringClient().getStates() return error: {result['Message']}")
                    stat = [['Error happened on service side']]
                callback['status'] = stat
                result = JobMonitoringClient().getMinorStates()
                if result['OK']:
                    stat = []
                    if result['Value']:
                        for i in result['Value']:
                            stat.append([i])
                    else:
                        stat = [['Nothing to display']]
                else:
                    gLogger.error(f"JobMonitoringClient().getMinorStates() return error: {result['Message']}")
                    stat = [['Error happened on service side']]
                callback['minorstat'] = stat
                result = JobMonitoringClient().getApplicationStates()
                if result['OK']:
                    app = []
                    if result['Value']:
                        for i in result['Value']:
                            app.append([i])
                    else:
                        app = [['Nothing to display']]
                else:
                    gLogger.error(f"JobMonitoringClient().getApplicationstates() return error: {result['Message']}")
                    app = [['Error happened on service side']]
                callback['app'] = app
                result = JobMonitoringClient().getJobTypes()
                if result['OK']:
                    types = []
                    if result['Value']:
                        for i in result['Value']:
                            types.append([i])
                    else:
                        types = [['Nothing to display']]
                else:
                    gLogger.error(f"JobMonitoringClient().getJobTypes() return error: {result['Message']}")
                    types = [['Error happened on service side']]
                callback['types'] = types
                if not self.isRegisteredUser():
                    callback['owner'] = [['Insufficient rights']]
                else:
                    result = JobMonitoringClient().getOwners()
                    if result['OK']:
                        owner = []
                        if result['Value']:
                            for i in result['Value']:
                                owner.append([str(i)])
                        else:
                            owner = [['Nothing to display']]
                    elif 'NormalUser' in self.getProperties():
                        owner = [[user]]
                        callback['owner'] = owner
                    else:
                        gLogger.error(f"JobMonitoringClient().getOwners() return error: {result['Message']}")
                        owner = [['Error happened on service side']]
                    callback['owner'] = owner
                result = JobMonitoringClient().getOwnerGroup()
                if result['OK']:
                    callback['OwnerGroup'] = [[group] for group in result['Value']]
                JobMonitorHandler.__dataCache.add(cacheKey, 360, callback)
        return callback

    def _request(self):
        self.numberOfJobs = int(self.get_argument('limit', '25'))
        self.pageNumber = int(self.get_argument('start', '0'))
        self.globalSort = [['JobID', 'DESC']]
        req = {}
        jobids = list(json.loads(self.get_argument('JobID', '[]')))
        if jobids:
            req['JobID'] = jobids
        pilotids = list(json.loads(self.get_argument('PilotJobReference', '[]')))
        if pilotids:
            req['PilotJobReference'] = pilotids
        prodids = list(json.loads(self.get_argument('jobGroup', '[]')))
        if prodids:
            req['JobGroup'] = prodids
        sites = list(json.loads(self.get_argument('site', '[]')))
        if sites:
            req['Site'] = sites
        status = list(json.loads(self.get_argument('status', '[]')))
        if status:
            req['Status'] = status
        minorstat = list(json.loads(self.get_argument('minorStatus', '[]')))
        if minorstat:
            req['MinorStatus'] = minorstat
        apps = list(json.loads(self.get_argument('appStatus', '[]')))
        if apps:
            req['ApplicationStatus'] = apps
        types = list(json.loads(self.get_argument('jobType', '[]')))
        if types:
            req['JobType'] = types
        owner = list(json.loads(self.get_argument('owner', '[]')))
        if owner:
            req['Owner'] = owner
        ownerGroup = list(json.loads(self.get_argument('OwnerGroup', '[]')))
        if ownerGroup:
            req['OwnerGroup'] = ownerGroup
        if self.get_argument('startDate', ''):
            req['FromDate'] = self.get_argument('startDate')
            if self.get_argument('startTime', ''):
                req['FromDate'] += ' ' + self.get_argument('startTime')
        if self.get_argument('endDate', ''):
            req['ToDate'] = self.get_argument('endDate')
            if self.get_argument('endTime', ''):
                req['ToDate'] += ' ' + self.get_argument('endTime')
        if self.get_argument('date', ''):
            req['LastUpdate'] = self.get_argument('date')
        sort = json.loads(self.get_argument('sort', '[]'))
        if sort:
            self.globalSort = []
            for i in sort:
                if 'LastSignOfLife' not in i['property']:
                    self.globalSort += [[str(i['property']), str(i['direction'])]]
        gLogger.debug('Request', str(req))
        return req

    def web_jobAction(self, JobID):
        ids = JobID.split(',')
        ids = [int(i) for i in ids]
        RPC = JobManagerClient()
        if self.get_argument('action') == 'delete':
            result = RPC.deleteJob(ids)
        elif self.get_argument('action') == 'kill':
            result = RPC.killJob(ids)
        elif self.get_argument('action') == 'reschedule':
            result = RPC.rescheduleJob(ids)
        elif self.get_argument('action') == 'reset':
            result = RPC.resetJob(ids)
        if result['OK']:
            return {'success': 'true', 'result': ''}
        if 'InvalidJobIDs' in result:
            return {'success': 'false', 'error': f"Invalid JobIDs: {result['InvalidJobIDs']}"}
        if 'NonauthorizedJobIDs' in result:
            return {'success': 'false', 'error': 'You are nonauthorized to %s jobs with JobID: %s' % (self.get_argument('action'), result['NonauthorizedJobIDs'])}
        return {'success': 'false', 'error': result['Message']}

    def web_jobData(self, id: int, data_kind: str) -> dict:
        if data_kind == 'getJDL':
            if (result := JobMonitoringClient().getJobJDL(id, False))['OK']:
                return {'success': 'true', 'result': result['Value']}
            return {'success': 'false', 'error': result['Message']}
        if data_kind == 'getBasicInfo':
            if (result := JobMonitoringClient().getJobSummary(id))['OK']:
                items = [[key, value] for key, value in result['Value'].items()]
                return {'success': 'true', 'result': items}
            return {'success': 'false', 'error': result['Message']}
        if data_kind == 'getParams':
            if (result := JobMonitoringClient().getJobParameters(id))['OK']:
                attr = result['Value'].get(id, {})
                items = []
                for i in attr.items():
                    if i[0] == 'Log URL':
                        items.append([i[0], i[1].replace('>', ' target="_blank">')])
                    elif i[0] != 'StandardOutput':
                        items.append([i[0], i[1]])
                return {'success': 'true', 'result': items}
            return {'success': 'false', 'error': result['Message']}
        if data_kind == 'getLoggingInfo':
            if (result := JobMonitoringClient().getJobLoggingInfo(id))['OK']:
                return {'success': 'true', 'result': result['Value']}
            return {'success': 'false', 'error': result['Message']}
        if data_kind == 'getStandardOutput':
            if (result := JobMonitoringClient().getJobParameters(id))['OK']:
                attr = result['Value'].get(id, {})
                if 'StandardOutput' in attr:
                    return {'success': 'true', 'result': attr['StandardOutput']}
                return {'success': 'false', 'error': 'Not accessible yet'}
            return {'success': 'false', 'error': result['Message']}
        if data_kind == 'getPending':
            if (result := ReqClient().readRequestsForJobs([id]))['OK']:
                items = {}
                if id in result['Value']['Successful']:
                    result = result['Value']['Successful'][id].getDigest()
                    if result['OK']:
                        items['PendingRequest'] = result['Value']
                    else:
                        raise WErr.fromSERROR(result)
                    return {'success': 'true', 'result': items}
                if id in result['Value']['Failed']:
                    return {'success': 'false', 'error': result['Value']['Failed'][id]}
                return {'success': 'false', 'error': 'No request found with unknown reason'}
            return {'success': 'false', 'error': result['Message']}
        if data_kind == 'getLogURL':
            if (result := JobMonitoringClient().getJobParameters(id))['OK']:
                attr = result['Value'].get(id, {})
                if 'Log URL' in attr:
                    httpsUrl = attr['Log URL'].split('"')[1]
                    if 'https:' not in httpsUrl:
                        httpsUrl = httpsUrl.replace('http', 'https')
                    return {'success': 'true', 'result': httpsUrl}
                return {'success': 'false', 'error': 'No URL found'}
            return {'success': 'false', 'error': result['Message']}
        if data_kind == 'getStagerReport':
            if (result := JobMonitoringClient().getJobParameters(id))['OK']:
                attr = result['Value'].get(id, {})
                if 'StagerReport' in attr:
                    return {'success': 'true', 'result': attr['StagerReport']}
                return {'success': 'false', 'error': 'StagerReport not available'}
            return {'success': 'false', 'error': result['Message']}
        if data_kind == 'getPilotStdOut':
            if not (result := WMSAdministratorClient().getJobPilotOutput(id))['OK']:
                return {'success': 'false', 'error': result['Message']}
            if 'StdOut' in result['Value']:
                return {'success': 'true', 'result': result['Value']['StdOut']}
        if data_kind == 'getPilotStdErr':
            if not (result := WMSAdministratorClient().getJobPilotOutput(id))['OK']:
                return {'success': 'false', 'error': result['Message']}
            if 'StdErr' in result['Value']:
                return {'success': 'true', 'result': result['Value']['StdErr']}
        if data_kind == 'getPilotLoggingInfo':
            pilotClient = PilotManagerClient()
            if (retVal := pilotClient.getPilots(id))['OK']:
                pilotReference = list(retVal['Value'])[0]
                if (retVal := pilotClient.getPilotLoggingInfo(pilotReference))['OK']:
                    return {'success': 'true', 'result': retVal['Value']}
                return {'success': 'false', 'error': retVal['Message']}
            return {'success': 'false', 'error': retVal['Message']}
        return {}

    def web_getStatisticsData(self, statsField):
        req = self._request()
        paletteColor = Palette()
        selector = statsField
        if selector == 'Minor Status':
            selector = 'MinorStatus'
        elif selector == 'Application Status':
            selector = 'ApplicationStatus'
        elif selector == 'Job Group':
            selector = 'JobGroup'
        elif selector == 'Owner Group':
            selector = 'OwnerGroup'
        elif selector == 'Job Type':
            selector = 'JobType'
        if (result := JobMonitoringClient().getJobStats(selector, req))['OK']:
            callback = []
            result = dict(result['Value'])
            keylist = sorted(result)
            if selector == 'Site':
                tier1 = gConfig.getValue('/WebApp/PreferredSites', [])
                if tier1:
                    tier1.sort()
                    for i in tier1:
                        if i in result:
                            countryCode = i.rsplit('.', 1)[1]
                            callback.append({'key': i, 'value': result[i], 'code': countryCode, 'color': paletteColor.getColor(countryCode)})
            for key in keylist:
                if selector == 'Site' and tier1:
                    if key not in tier1:
                        try:
                            countryCode = key.rsplit('.', 1)[1]
                        except BaseException:
                            countryCode = 'Unknown'
                        callback.append({'key': key, 'value': result[key], 'code': countryCode, 'color': paletteColor.getColor(key)})
                elif selector == 'Site' and (not tier1):
                    try:
                        countryCode = key.rsplit('.', 1)[1]
                    except BaseException:
                        countryCode = 'Unknown'
                    callback.append({'key': key, 'value': result[key], 'code': countryCode, 'color': paletteColor.getColor(key)})
                else:
                    callback.append({'key': key, 'value': result[key], 'code': '', 'color': paletteColor.getColor(key)})
            return {'success': 'true', 'result': callback}
        return {'success': 'false', 'error': result['Message']}

    def web_getSandbox(self, jobID: int=None, sandbox: str='Output', check=None):
        if not jobID:
            return {'success': 'false', 'error': 'Maybe you forgot the jobID ?'}
        client = SandboxStoreClient(useCertificates=True, delegatedDN=self.getUserDN(), delegatedGroup=self.getUserGroup())
        result = client.downloadSandboxForJob(jobID, sandbox, inMemory=True)
        if not result['OK']:
            return {'success': 'false', 'error': f"Error: {result['Message']}"}
        if check:
            return {'success': 'true'}
        data = result['Value']
        fname = f'{str(jobID)}_{sandbox}Sandbox.tar'
        self.set_header('Content-type', 'application/x-tar')
        self.set_header('Content-Disposition', f'attachment; filename="{fname}"')
        self.set_header('Content-Length', len(data))
        self.set_header('Cache-Control', 'no-cache, no-store, must-revalidate, max-age=0')
        self.set_header('Pragma', 'no-cache')
        return data