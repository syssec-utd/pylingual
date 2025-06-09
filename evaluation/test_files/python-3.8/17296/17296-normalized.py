def build(self, **kwargs):
    """Build/return a list of [(bead, x, y, z), ...]"""
    if not self.coords:
        if self.beads and self.template:
            stuff = zip(self.beads, self.template)
            self.coords = [[i, x, y, z] for (i, (x, y, z)) in stuff if i != '-']
        else:
            if self.beads:
                beads = list(self.beads)
            else:
                beads = [HEADBEADS[i] for i in self.head]
                beads.extend([LINKBEADS[n] + str(i + 1) for (i, n) in enumerate(self.link)])
                for (i, t) in enumerate(self.tail):
                    beads.extend([n + chr(65 + i) + str(j + 1) for (j, n) in enumerate(t)])
            taillength = max([0] + [len(i) for i in self.tail])
            length = len(self.head) + taillength
            rl = range(len(self.head))
            struc = [(0, 0, length - i) for i in rl]
            rl = range(len(self.link))
            struc.extend([(i % 2, i // 2, taillength) for i in rl])
            for (j, tail) in enumerate(self.tail):
                rl = range(len(tail))
                struc.extend([(j % 2, j // 2, taillength - 1 - i) for i in rl])
            (mx, my, mz) = [(max(i) + min(i)) / 2 for i in zip(*struc)]
            self.coords = [[i, 0.25 * (x - mx), 0.25 * (y - my), z] for (i, (x, y, z)) in zip(beads, struc)]
    diam = kwargs.get('diam', self.diam)
    radius = diam * 0.45
    minmax = [(min(i), max(i)) for i in list(zip(*self.coords))[1:]]
    (mx, my, mz) = [sum(i) / 2.0 for i in minmax]
    scale = radius / math.sqrt((minmax[0][0] - mx) ** 2 + (minmax[1][0] - my) ** 2)
    for i in self.coords:
        i[1] = scale * (i[1] - mx)
        i[2] = scale * (i[2] - my)
        i[3] -= minmax[2][0]
    return self.coords