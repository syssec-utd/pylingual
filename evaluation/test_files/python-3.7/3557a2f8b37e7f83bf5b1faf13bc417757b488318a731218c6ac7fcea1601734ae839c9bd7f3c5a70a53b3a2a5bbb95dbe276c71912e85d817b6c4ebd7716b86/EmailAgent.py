""" EmailAgent
  This agent reads the ResourceStatusCache table of ResourceStatusDB
  for sending emails with aggregated information about state changes,
  and then clears it.

.. literalinclude:: ../ConfigTemplate.cfg
  :start-after: ##BEGIN EmailAgent
  :end-before: ##END
  :dedent: 2
  :caption: EmailAgent options
"""
from DIRAC import gConfig, S_OK, S_ERROR
from DIRAC.Core.Base.AgentModule import AgentModule
from DIRAC.ResourceStatusSystem.Client.ResourceStatusClient import ResourceStatusClient
from DIRAC.ResourceStatusSystem.Utilities import RssConfiguration
from DIRAC.Interfaces.API.DiracAdmin import DiracAdmin
AGENT_NAME = 'ResourceStatus/EmailAgent'

class EmailAgent(AgentModule):

    def __init__(self, *args, **kwargs):
        AgentModule.__init__(self, *args, **kwargs)
        self.diracAdmin = None
        self.default_value = None
        self.rsClient = ResourceStatusClient()

    def initialize(self, *args, **kwargs):
        """EmailAgent initialization"""
        self.diracAdmin = DiracAdmin()
        return S_OK()

    @staticmethod
    def _groupBySiteName(result):
        """
        Group results by SiteName
        """
        siteNameCol = result['Columns'].index('SiteName')
        resultValue = result['Value']
        siteNameDict = {}
        for row in resultValue:
            if row[siteNameCol] not in siteNameDict:
                siteNameDict[row[siteNameCol]] = [row]
            else:
                siteNameDict[row[siteNameCol]].append(row)
        return siteNameDict

    def execute(self):
        result = self.rsClient.select('ResourceStatusCache')
        if not result['OK']:
            return S_ERROR()
        columnNames = result['Columns']
        result = self._groupBySiteName(result)
        for (site, records) in result.items():
            email = ''
            html_body = ''
            html_elements = ''
            if gConfig.getValue('/DIRAC/Setup'):
                setup = '(' + gConfig.getValue('/DIRAC/Setup') + ')\n\n'
            else:
                setup = ''
            html_header = '      <!DOCTYPE html>\n      <html>\n      <head>\n      <meta charset=\'UTF-8\'>\n        <style>\n          table{{color:#333;font-family:Helvetica,Arial,sans-serif;min-width:700px;border-collapse:collapse;border-spacing:0}}\n          td,th{{border:1px solid transparent;height:30px;transition:all .3s}}th{{background:#DFDFDF;font-weight:700}}\n          td{{background:#FAFAFA;text-align:center}}.setup{{font-size:150%;color:grey}}.Banned{{color:red}}.Error{{color:#8b0000}}\n          .Degraded{{color:gray}}.Probing{{color:#00f}}.Active{{color:green}}tr:nth-child(even)\n          td{{background:#F1F1F1}}tr:nth-child(odd)\n          td{{background:#FEFEFE}}tr td:hover{{background:#666;color:#FFF}}\n        </style>\n      </head>\n      <body>\n        <p class="setup">{setup}</p>\n      '.format(setup=setup)
            for row in records:
                statusType = row[columnNames.index('StatusType')]
                resourceName = row[columnNames.index('ResourceName')]
                status = row[columnNames.index('Status')]
                time = row[columnNames.index('Time')]
                previousStatus = row[columnNames.index('PreviousStatus')]
                html_elements += '<tr>' + '<td>' + statusType + '</td>' + '<td>' + resourceName + '</td>' + "<td class='" + status + "'>" + status + '</td>' + '<td>' + str(time) + '</td>' + "<td class='" + previousStatus + "'>" + previousStatus + '</td>' + '</tr>'
            html_body = '        <table>\n          <tr>\n              <th>Status Type</th>\n              <th>Resource Name</th>\n              <th>Status</th>\n              <th>Time</th>\n              <th>Previous Status</th>\n          </tr>\n          {html_elements}\n        </table>\n      </body>\n      </html>\n      '.format(html_elements=html_elements)
            email = html_header + html_body
            subject = 'RSS actions taken for ' + str(site) + '\n'
            self._sendMail(subject, email, html=True)
        self.rsClient.delete('ResourceStatusCache')
        return S_OK()

    def _sendMail(self, subject, body, html=False):
        userEmails = self._getUserEmails()
        if not userEmails['OK']:
            return userEmails
        fromAddress = RssConfiguration.RssConfiguration().getConfigFromAddress()
        for user in userEmails['Value']:
            resEmail = self.diracAdmin.sendMail(user, subject, body, fromAddress=fromAddress, html=html)
            if not resEmail['OK']:
                return S_ERROR('Cannot send email to user "%s"' % user)
        return S_OK()

    def _getUserEmails(self):
        configResult = RssConfiguration.getnotificationGroups()
        if not configResult['OK']:
            return configResult
        try:
            notificationGroups = configResult['Value']['notificationGroups']
        except KeyError:
            return S_ERROR('%s/notificationGroups not found')
        notifications = RssConfiguration.getNotifications()
        if not notifications['OK']:
            return notifications
        notifications = notifications['Value']
        userEmails = []
        for notificationGroupName in notificationGroups:
            try:
                userEmails.extend(notifications[notificationGroupName]['users'])
            except KeyError:
                self.log.error('%s not present' % notificationGroupName)
        return S_OK(userEmails)