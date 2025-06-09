def replace(cls, fileobj, old_pages, new_pages):
    """Replace old_pages with new_pages within fileobj.

        old_pages must have come from reading fileobj originally.
        new_pages are assumed to have the 'same' data as old_pages,
        and so the serial and sequence numbers will be copied, as will
        the flags for the first and last pages.

        fileobj will be resized and pages renumbered as necessary. As
        such, it must be opened r+b or w+b.
        """
    first = old_pages[0].sequence
    for page, seq in zip(new_pages, range(first, first + len(new_pages))):
        page.sequence = seq
        page.serial = old_pages[0].serial
    new_pages[0].first = old_pages[0].first
    new_pages[0].last = old_pages[0].last
    new_pages[0].continued = old_pages[0].continued
    new_pages[-1].first = old_pages[-1].first
    new_pages[-1].last = old_pages[-1].last
    new_pages[-1].complete = old_pages[-1].complete
    if not new_pages[-1].complete and len(new_pages[-1].packets) == 1:
        new_pages[-1].position = -1
    new_data = b''.join((cls.write(p) for p in new_pages))
    delta = len(new_data)
    fileobj.seek(old_pages[0].offset, 0)
    insert_bytes(fileobj, delta, old_pages[0].offset)
    fileobj.seek(old_pages[0].offset, 0)
    fileobj.write(new_data)
    new_data_end = old_pages[0].offset + delta
    old_pages.reverse()
    for old_page in old_pages:
        adj_offset = old_page.offset + delta
        delete_bytes(fileobj, old_page.size, adj_offset)
    if len(old_pages) != len(new_pages):
        fileobj.seek(new_data_end, 0)
        serial = new_pages[-1].serial
        sequence = new_pages[-1].sequence + 1
        cls.renumber(fileobj, serial, sequence)