def delete(self, request, *args, **kwargs):
    """
        Calls pre and post delete hooks for DelteViews.
        """
    self.object = self.get_object()
    success_url = self.get_success_url()
    self.pre_delete(self.object)
    self.object.delete()
    self.post_delete(self.object)
    return HttpResponseRedirect(success_url)