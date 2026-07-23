from __future__ import annotations

from dataclasses import dataclass


INDENT = "  "
SIDE_OFFSET = " " * 14


@dataclass
class Recovery:
    value: object
    complete: bool


@dataclass
class Segment:
    tag: str
    ordered_children: list[Segment | tuple[int, object]]
    base_stack_depth: int | None = None
    start_offset: int | None = None
    end_offset: int | None = None

    def compute_offsets(self) -> None:
        offsets = []
        for child in self.ordered_children:
            if isinstance(child, Segment):
                child.compute_offsets()
                if child.start_offset is not None:
                    offsets.append(child.start_offset)
                if child.end_offset is not None:
                    offsets.append(child.end_offset)
            else:
                instr = child[1]
                if hasattr(instr, "offset"):
                    offsets.append(instr.offset)
        if offsets:
            self.start_offset = min(offsets)
            self.end_offset = max(offsets)

    def print(self, indent=0):
        print(INDENT * indent, self.tag, sep="")
        for child in self.ordered_children:
            if isinstance(child, type(self)):
                child.print(indent + 1)
            else:
                colpad = len(f"{SIDE_OFFSET}{child[0]} {child[1].opname}")
                print(f"{SIDE_OFFSET}{child[0]} {child[1].opname}" + (" " * (20 - colpad) + f"{self.base_stack_depth}" if self.base_stack_depth else ""))
        print()