# Dicts with complex keys
a = {(1, 2): "tuple key"}
b = {frozenset({1, 2}): "frozenset key"}
c = {True: "bool key", None: "none key", 1: "int key"}
d = {(1, (2, 3)): {"nested": [4, 5]}}
print(a, b, c, d)
