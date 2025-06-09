def update_tab_bar_visibility(self):
    """ update visibility of the tabBar depending of the number of tab

        0 or 1 tab, tabBar hidden
        2+ tabs, tabBar visible

        send a self.close if number of tab ==0

        need to be called explicitly, or be connected to tabInserted/tabRemoved
        """
    if self.tab_widget.count() <= 1:
        self.tab_widget.tabBar().setVisible(False)
    else:
        self.tab_widget.tabBar().setVisible(True)
    if self.tab_widget.count() == 0:
        self.close()