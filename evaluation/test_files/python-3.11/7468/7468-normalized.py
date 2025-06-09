def remove_dashboard_panel(self, dashboard, panel_name):
    """**Description**
            Removes a panel from the dashboard. The panel to remove is identified by the specified ``name``.

        **Arguments**
            - **name**: name of the panel to find and remove

        **Success Return Value**
            A dictionary showing the details of the edited dashboard.

        **Example**
            `examples/dashboard.py <https://github.com/draios/python-sdc-client/blob/master/examples/dashboard.py>`_
        """
    dashboard_configuration = copy.deepcopy(dashboard)

    def filter_fn(panel):
        return panel['name'] == panel_name
    panels = list(filter(filter_fn, dashboard_configuration['widgets']))
    if len(panels) > 0:
        for panel in panels:
            dashboard_configuration['widgets'].remove(panel)
        res = requests.put(self.url + self._dashboards_api_endpoint + '/' + str(dashboard['id']), headers=self.hdrs, data=json.dumps({'dashboard': dashboard_configuration}), verify=self.ssl_verify)
        return self._request_result(res)
    else:
        return [False, 'Not found']