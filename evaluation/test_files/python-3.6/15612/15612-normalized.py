def writeJSON(self, filename):
    """Writes the data to the given file::

            DatapointArray([{"t": unix timestamp, "d": data}]).writeJSON("myfile.json")

        The data can later be loaded using loadJSON.
        """
    with open(filename, 'w') as f:
        json.dump(self, f)