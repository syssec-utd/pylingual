def add_btn_ok(self, label_ok):
    """
        Adds an OK button to allow the user to exit the dialog.
        
        This widget can be triggered by setting the label ``label_ok`` to a string.
        
        This widget will be mostly centered on the screen, but below the main label
        by the double of its height.
        """
    self.wbtn_ok = button.Button('btn_ok', self, self.window, self.peng, pos=lambda sw, sh, bw, bh: (sw / 2 - bw / 2, sh / 2 - bh / 2 - bh * 2), size=[0, 0], label=label_ok, borderstyle=self.borderstyle)
    self.wbtn_ok.size = lambda sw, sh: (self.wbtn_ok._label.font_size * 8, self.wbtn_ok._label.font_size * 2)
    self.addWidget(self.wbtn_ok)

    def f():
        self.doAction('click_ok')
        self.exitDialog()
    self.wbtn_ok.addAction('click', f)