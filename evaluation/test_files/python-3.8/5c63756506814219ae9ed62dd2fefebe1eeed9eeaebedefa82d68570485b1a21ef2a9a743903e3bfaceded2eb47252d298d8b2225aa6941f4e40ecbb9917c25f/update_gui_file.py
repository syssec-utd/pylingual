"""
Script to update correctly the main GUI (.py) file from the Qt design (.ui) file
"""
from GridCal.Gui.update_gui_common import convert_resource_file, convert_ui_file
if __name__ == '__main__':
    for f in ['gui.ui']:
        convert_ui_file(source=f)