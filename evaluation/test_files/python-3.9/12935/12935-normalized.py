def insert_patches(self, patches):
    """ Insert list of patches at the front of the curent patches list """
    patchlines = []
    for patch_name in patches:
        patchline = PatchLine(patch_name)
        patch = patchline.get_patch()
        if patch:
            self.patch2line[patch] = patchline
        patchlines.append(patchline)
    patchlines.extend(self.patchlines)
    self.patchlines = patchlines