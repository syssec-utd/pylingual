def add_page(self, page=None):
    """ May generate and add a PDFPage separately, or use this to generate
            a default page."""
    if page is None:
        self.page = PDFPage(self.orientation_default, self.layout_default, self.margins)
    else:
        self.page = page
    self.page._set_index(len(self.pages))
    self.pages.append(self.page)
    currentfont = self.font
    self.set_font(font=currentfont)
    self.session._reset_colors()