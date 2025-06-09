import datetime
from . import Framework

class DeploymentStatus(Framework.TestCase):

    def setUp(self):
        super().setUp()
        self.deployment = self.g.get_user().get_repo('PyGithub').get_deployment(263877258)
        self.status = self.deployment.get_status(388454671)

    def testAttributes(self):
        self.assertEqual(self.status.id, 388454671)
        created_at = datetime.datetime(2020, 8, 26, 14, 32, 51)
        self.assertEqual(self.status.created_at, created_at)
        self.assertEqual(self.status.creator.login, 'jacquev6')
        self.assertEqual(self.status.deployment_url, 'https://api.github.com/repos/jacquev6/PyGithub/deployments/263877258')
        self.assertEqual(self.status.description, 'Deployment queued')
        self.assertEqual(self.status.environment, 'test')
        self.assertEqual(self.status.environment_url, 'https://example.com/environment')
        self.assertEqual(self.status.repository_url, 'https://api.github.com/repos/jacquev6/PyGithub')
        self.assertEqual(self.status.state, 'queued')
        self.assertEqual(self.status.target_url, 'https://example.com/deployment.log')
        self.assertEqual(self.status.updated_at, created_at)
        self.assertEqual(self.status.url, 'https://api.github.com/repos/jacquev6/PyGithub/deployments/263877258/statuses/388454671')
        self.assertEqual(self.status.node_id, 'MDE2OkRlcGxveW1lbnRTdGF0dXMzODg0NTQ2NzE=')
        self.assertEqual(repr(self.status), 'DeploymentStatus(url="https://api.github.com/repos/jacquev6/PyGithub/deployments/263877258/statuses/388454671", id=388454671)')

    def testCreate(self):
        newStatus = self.deployment.create_status('queued', target_url='https://example.com/deployment.log', description='Deployment queued', environment='test', environment_url='https://example.com/environment', auto_inactive=True)
        self.assertEqual(newStatus.id, 388454671)
        self.assertEqual(newStatus.state, 'queued')
        self.assertEqual(newStatus.repository_url, 'https://api.github.com/repos/jacquev6/PyGithub')

    def testGetStatuses(self):
        statuses = self.deployment.get_statuses()
        self.assertListKeyEqual(statuses, lambda s: s.id, [388454671, 388433743, 388432880])