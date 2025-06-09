def word_break(el, max_width=40, avoid_elements=_avoid_word_break_elements, avoid_classes=_avoid_word_break_classes, break_character=unichr(8203)):
    """
    Breaks any long words found in the body of the text (not attributes).

    Doesn't effect any of the tags in avoid_elements, by default
    ``<textarea>`` and ``<pre>``

    Breaks words by inserting &#8203;, which is a unicode character
    for Zero Width Space character.  This generally takes up no space
    in rendering, but does copy as a space, and in monospace contexts
    usually takes up space.

    See http://www.cs.tut.fi/~jkorpela/html/nobr.html for a discussion
    """
    if el.tag in _avoid_word_break_elements:
        return
    class_name = el.get('class')
    if class_name:
        dont_break = False
        class_name = class_name.split()
        for avoid in avoid_classes:
            if avoid in class_name:
                dont_break = True
                break
        if dont_break:
            return
    if el.text:
        el.text = _break_text(el.text, max_width, break_character)
    for child in el:
        word_break(child, max_width=max_width, avoid_elements=avoid_elements, avoid_classes=avoid_classes, break_character=break_character)
        if child.tail:
            child.tail = _break_text(child.tail, max_width, break_character)