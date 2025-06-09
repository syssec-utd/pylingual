"""Overloads all variable read operations."""
import gast
from nvidia.dali._autograph.core import converter
from nvidia.dali._autograph.pyct import anno
from nvidia.dali._autograph.pyct import templates

class VariableAccessTransformer(converter.Base):
    """Rewrites basic symbol reads.

  This transformer rewrites variable reads with a "read" operator which allows
  tracking activity.

  Example:

  For a basic statement:

      a = b + c

  This is translated to:

      a = ld(b) + ld(c)

  Augmented assignment operations also introduce a `ld` operator:

      a += b

  The assignment target also receives an operator to properly represent the
  read:

      a = ld(a)
      a += ld(b)
  """

    def visit_Name(self, node):
        if not anno.hasanno(node, anno.Static.ORIG_DEFINITIONS):
            return node
        if isinstance(node.ctx, gast.Load):
            node = templates.replace_as_expression('ag__.ld(var_)', var_=node)
        return node

    def visit_Delete(self, node):
        node = self.generic_visit(node)
        rewrite_targets = []
        for tgt in node.targets:
            if isinstance(tgt, gast.Name):
                rewrite_targets.append(tgt)
        if not rewrite_targets:
            return node
        results = []
        for tgt in rewrite_targets:
            template = '\n        var_ = ag__.Undefined(var_name)\n      '
            results.extend(templates.replace(template, var_=tgt, var_name=gast.Constant(tgt.id, kind=None)))
        remaining_targets = [n for n in node.targets if n not in rewrite_targets]
        if remaining_targets:
            results.append(gast.Delete(targets=remaining_targets))
        return results

    def visit_AugAssign(self, node):
        if isinstance(node.target, gast.Name):
            template = '\n        var_ = ag__.ld(var_)\n        original\n      '
            node = templates.replace(template, var_=node.target, original=node)
        else:
            node = self.generic_visit(node)
        return node

def transform(node, ctx):
    return VariableAccessTransformer(ctx).visit(node)