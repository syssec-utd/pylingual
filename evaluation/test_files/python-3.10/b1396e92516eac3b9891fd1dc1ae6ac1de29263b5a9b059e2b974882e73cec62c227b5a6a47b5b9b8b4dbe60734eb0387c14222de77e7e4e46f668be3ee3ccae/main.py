import werkzeug
from odoo import http

class ProjectBrowser(http.Controller):

    def get_record_url(self, model, domain, action_xml_id):
        env = http.request.env()
        records = env[model].search(domain)
        record_id = records and records.id or -1
        action_id = env.ref(action_xml_id).id
        return '/web#id={}&view_type=form&model={}&action={}'.format(record_id, model, action_id)

    def get_task_url(self, key):
        return self.get_record_url('project.task', [('key', '=ilike', key)], 'project.action_view_task')

    def get_project_url(self, key):
        return self.get_record_url('project.project', [('key', '=ilike', key)], 'project.open_view_project_all_config')

    @http.route(['/projects/<string:key>'], type='http', auth='user')
    def open_project(self, key, **kwargs):
        return werkzeug.utils.redirect(self.get_project_url(key), 301)

    @http.route(['/tasks/<string:key>'], type='http', auth='user')
    def open_task(self, key, **kwargs):
        return werkzeug.utils.redirect(self.get_task_url(key), 301)