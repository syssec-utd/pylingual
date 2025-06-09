""" Base test cases
"""
from Products.CMFPlone import setuphandlers
from plone.testing import z2
from plone.app.testing import TEST_USER_ID
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import setRoles

class EEAFixture(PloneSandboxLayer):
    """ EEA Testing Policy
    """

    def setUpZope(self, app, configurationContext):
        """ Setup Zope
        """
        import eea.website.policy
        self.loadZCML(package=eea.website.policy)
        z2.installProduct(app, 'eea.kitkat')
        z2.installProduct(app, 'eea.dexterity.indicators')
        z2.installProduct(app, 'eea.dexterity.themes')
        z2.installProduct(app, 'eea.progress.workflow')
        z2.installProduct(app, 'eea.website.policy')

    def setUpPloneSite(self, portal):
        """ Setup Plone
        """
        applyProfile(portal, 'eea.website.policy:default')
        wftool = portal['portal_workflow']
        wftool.setDefaultChain('simple_publication_workflow')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        try:
            applyProfile(portal, 'plone.app.contenttypes:plone-content')
        except KeyError:
            setuphandlers.setupPortalContent(portal)
        portal.invokeFactory('Folder', 'sandbox', title='Sandbox')

    def tearDownZope(self, app):
        """ Uninstall Zope
        """
        z2.uninstallProduct(app, 'eea.kitkat')
        z2.uninstallProduct(app, 'eea.dexterity.indicators')
        z2.uninstallProduct(app, 'eea.dexterity.themes')
        z2.uninstallProduct(app, 'eea.progress.workflow')
        z2.uninstallProduct(app, 'eea.website.policy')
EEAFIXTURE = EEAFixture()
FUNCTIONAL_TESTING = FunctionalTesting(bases=(EEAFIXTURE,), name='EEApolicy:Functional')