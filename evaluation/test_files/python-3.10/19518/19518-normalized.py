def style(self, index, *args):
    """
        Add style to your axis, one at a time
        args are of the form::
            <axis color>,
            <font size>,
            <alignment>,
            <drawing control>,
            <tick mark color>
        APIPARAM: chxs
        """
    args = color_args(args, 0)
    self.data['styles'].append(','.join([str(index)] + list(map(str, args))))
    return self.parent