def write_to_file(self):
    """
        This function calls "gui_batch.py" with inputs values to write the batch file.
        """
    bt = BatchFile(self.batch_name_value, self.p_values, self.x_value, self.y_value, self.g_value, self.s_value, self.z_value, self.wavelength_values, self.verbose_value, self.phytoplankton_path, self.bottom_path, self.nb_cpu, self.executive_path, self.saa_values, self.sza_values, self.report_parameter_value)
    bt.write_batch_to_file(str(self.batch_name_value + '_batch.txt'))