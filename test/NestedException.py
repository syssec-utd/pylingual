# Nested try statements with empty handlers (issue 109), and nested raises with an early return. A try body that is
# only `pass` has no bytecode from 3.12, so they call `f()`.


def nested_empty():
    try:
        try:
            try:
                f()
            except Exception as e:
                pass
        except Exception as e:
            pass
    except Exception as e:
        try:
            try:
                f()
            except Exception as e:
                pass
        except Exception as e:
            try:
                f()
            except Exception as e:
                pass


def nested_empty_named():
    try:
        try:
            f()
        except LookupError as caught:
            pass
    except LookupError as caught:
        try:
            f()
        except LookupError as caught:
            pass


def nested_raise(kind=0):
    events = []
    try:
        try:
            try:
                if kind == 1:
                    raise TypeError("escape")
                if kind == 2:
                    return ["early"]
                raise ValueError("inner")
            except ValueError as inner:
                events.append(str(inner))
                raise KeyError("middle")
        except KeyError as middle:
            events.append("middle")
            raise RuntimeError("outer")
    except RuntimeError as outer:
        try:
            try:
                raise LookupError("handler")
            except LookupError as nested:
                events.append(str(nested))
        except Exception as unexpected:
            events.append("unexpected")
        events.append("outer")
    return events
