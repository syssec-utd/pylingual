from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from markup.Module import Module
from markup.Transform import Transform
import markup.Markers as Markers

class SkipBlocks(Module):
    """
    Module for skip lines
    """
    priority = 0

    def transform(self, data):
        transforms = []
        linenum = 0
        for line in data:
            stripped = line.strip()
            if stripped == Markers.markup_markdown_begin:
                for x in transforms:
                    x.oper = 'drop'
                transform = Transform(linenum, 'drop')
                transforms.append(transform)
            elif stripped == Markers.markup_markdown_end:
                for dropped in range(linenum, len(data)):
                    transform = Transform(linenum=dropped, oper='drop')
                    transforms.append(transform)
                return transforms
            else:
                transform = Transform(linenum, 'noop')
                transforms.append(transform)
            linenum = linenum + 1
        return transforms