"""Container to stack elements with spacing."""
from pynecone.components.libs.chakra import ChakraComponent
from pynecone.var import Var

class CircularProgress(ChakraComponent):
    """The CircularProgress component is used to indicate the progress for determinate and indeterminate processes."""
    tag = 'CircularProgress'
    cap_is_round: Var[bool]
    is_indeterminate: Var[bool]
    max_: Var[int]
    min_: Var[int]
    thickness: Var[int]
    track_color: Var[str]
    value: Var[int]
    value_text: Var[str]

class CircularProgressLabel(ChakraComponent):
    """Label of CircularProcess."""
    tag = 'CircularProgressLabel'