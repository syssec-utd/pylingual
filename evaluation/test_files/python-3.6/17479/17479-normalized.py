def validate_integer(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
    """Check if text Entry is valid (number).

        I have no idea what all these arguments are doing here but took this from
        https://stackoverflow.com/questions/8959815/restricting-the-value-in-tkinter-entry-widget
        """
    if action == '1':
        if text in '0123456789.-+':
            try:
                int(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False
    else:
        return True