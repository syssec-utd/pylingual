def has_changed(self):
    """Return True if data differs from initial."""
    if self.formsets:
        for formset in self.formsets.values():
            for form in formset.forms:
                if form.has_changed():
                    return True
    return bool(self.changed_data)