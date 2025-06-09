def to_dict(self):
    """
        Sets the current encoder output to Python `dict` and returns
        the cursor.  This makes it possible to set the output encoding
        and iterate over the results:

        .. code-block:: python

            with giraffez.Cmd() as cmd:
                for row in cmd.execute(query).to_dict():
                    print(row)

        Or can be passed as a parameter to an object that consumes an iterator:

        .. code-block:: python

            result = cmd.execute(query)
            list(result.to_dict())
        """
    self.conn.set_encoding(ROW_ENCODING_DICT)
    self.processor = lambda x, y: y
    return self