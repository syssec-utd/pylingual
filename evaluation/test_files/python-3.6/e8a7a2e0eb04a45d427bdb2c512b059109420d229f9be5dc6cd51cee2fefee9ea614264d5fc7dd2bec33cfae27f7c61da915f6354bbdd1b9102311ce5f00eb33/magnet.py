"""
    femagtools.magnet
    ~~~~~~~~~~~~~~~~~

    Creating and managing magnet material



"""

class Magnet:

    def __init__(self, mlist=[]):
        """initialize this object from a list of magnet objects"""
        self.magnets = {}
        for m in mlist:
            if 'id' in m:
                self.magnets[str(m['id'])] = m
            elif 'name' in m:
                self.magnets[m['name']] = m

    def find(self, id):
        """find magnet by id or name"""
        try:
            return self.magnets[id]
        except ValueError:
            pass
        except KeyError:
            pass
        return self.find_by_name(id)

    def find_by_name(self, name):
        """find magnet by name"""
        try:
            for k in self.magnets.keys():
                if self.magnets[k]['name'] == name:
                    return self.magnets[k]
        except KeyError:
            pass
        return {}

    def __str__(self):
        return str([self.magnets[m] for m in self.magnets])