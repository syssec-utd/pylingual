def render(self, form, form_style, context, template_pack=TEMPLATE_PACK):
    """
        Re-implement almost the same code from crispy_forms but passing
        ``form`` instance to item ``render_link`` method.
        """
    (links, content) = ('', '')
    if not self.css_id:
        self.css_id = '-'.join(['tabsholder', text_type(randint(1000, 9999))])
    for tab in self.fields:
        tab.active = False
    self.open_target_group_for_form(form)
    for tab in self.fields:
        content += render_field(tab, form, form_style, context, template_pack=template_pack)
        links += tab.render_link(form, template_pack)
    context.update({'tabs': self, 'links': links, 'content': content})
    template = self.get_template_name(template_pack)
    return render_to_string(template, context.flatten())