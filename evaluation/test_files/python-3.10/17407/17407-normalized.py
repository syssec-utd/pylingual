def _inject(self, fileobj):
    """Write tag data into the Theora comment packet/page."""
    fileobj.seek(0)
    page = OggPage(fileobj)
    while not page.packets[0].startswith(b'\x81theora'):
        page = OggPage(fileobj)
    old_pages = [page]
    while not (old_pages[-1].complete or len(old_pages[-1].packets) > 1):
        page = OggPage(fileobj)
        if page.serial == old_pages[0].serial:
            old_pages.append(page)
    packets = OggPage.to_packets(old_pages, strict=False)
    packets[0] = b'\x81theora' + self.write(framing=False)
    new_pages = OggPage.from_packets(packets, old_pages[0].sequence)
    OggPage.replace(fileobj, old_pages, new_pages)