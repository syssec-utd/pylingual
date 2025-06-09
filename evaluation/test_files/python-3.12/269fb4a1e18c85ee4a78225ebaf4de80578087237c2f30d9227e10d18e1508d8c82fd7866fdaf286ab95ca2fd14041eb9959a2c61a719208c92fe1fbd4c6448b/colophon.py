from datetime import date
from plone import api
from plone.app.layout.viewlets import common
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class ColophonViewlet(common.ViewletBase):
    index = ViewPageTemplateFile('colophon.pt')

    def update(self):
        super(ColophonViewlet, self).update()
        self.year = date.today().year
        self.is_anonymous = api.user.is_anonymous()
        self.has_gdpr = api.portal.get_registry_record('imio.gdpr.interfaces.IGDPRSettings.is_text_ready', default=False)