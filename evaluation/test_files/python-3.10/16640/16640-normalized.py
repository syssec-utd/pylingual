def search_file_result(self):
    """
        This function once the file found, display data's file and the graphic associated.
        """
    if self.ui.tabWidget.currentIndex() == TabWidget.NORMAL_MODE:
        self.result_file = self.file_dialog.getOpenFileName(caption=str('Open Report File'), directory='./outputs')
        if not self.result_file == '':
            self.ui.show_all_curves.setDisabled(False)
            self.ui.show_grid.setDisabled(False)
            self.data_processing()
            self.display_the_graphic(self.num_line, self.wavelength, self.data_wanted, self.information)
            self.authorized_display = True