"""
Output language of the control flow model.

A skeleton is the nesting of a code object's statements, in source order: `<s0> { <s1> } else { <s2> }`. The block
grammar (block_grammar.py) keeps the model's skeletons valid. Trained models store their actions, so changing a token
needs new models.
"""

OPEN, CLOSE = "{", "}"  # body of the statement or keyword before OPEN
LOOP = "loop"  # the next statement is a `while` header
# keywords for lines without bytecode of their own; dict order is the training vocabulary order
KEYWORD_TEXT = {
    "else": "else:",
    "try": "try:",
    "finally": "finally:",
    "except": "except:",
    "while_true": "while True:",
    "break": "break",
    "continue": "continue",
    "case_": "case _:",
}
BLOCK_KEYWORDS = ("else", "try", "finally", "except", "while_true", "case_")  # followed by a body


def ref(i: int) -> str:
    """Reference to statement i."""
    return f"<s{i}>"


def parse_ref(token: str) -> int | None:
    """Statement index of a reference, None for other tokens."""
    if token.startswith("<s") and token.endswith(">") and token[2:-1].isdigit():
        return int(token[2:-1])
    return None
