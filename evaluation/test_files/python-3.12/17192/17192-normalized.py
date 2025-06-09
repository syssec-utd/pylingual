def remove(request, video_id):
    """
    Removes the video from youtube and from db
    Requires POST
    """
    try:
        next_url = settings.YOUTUBE_DELETE_REDIRECT_URL
    except AttributeError:
        next_url = reverse('django_youtube.views.upload')
    try:
        Video.objects.get(video_id=video_id).delete()
    except:
        from django.contrib import messages
        messages.add_message(request, messages.ERROR, _('Video could not be deleted.'))
    return HttpResponseRedirect(next_url)