def direct_upload(request):
    """
    direct upload method
    starts with uploading video to our server
    then sends the video file to youtube

    param:
        (optional) `only_data`: if set, a json response is returns i.e. {'video_id':'124weg'}

    return:
        if `only_data` set, a json object.
        otherwise redirects to the video display page
    """
    if request.method == 'POST':
        try:
            form = YoutubeDirectUploadForm(request.POST, request.FILES)
            if form.is_valid():
                uploaded_video = form.save()
                api = Api()
                api.authenticate()
                video_entry = api.upload_direct(uploaded_video.file_on_server.path, 'Uploaded video from zuqqa')
                swf_url = video_entry.GetSwfUrl()
                youtube_url = video_entry.id.text
                url_parts = youtube_url.split('/')
                url_parts.reverse()
                video_id = url_parts[0]
                video = Video()
                video.user = request.user
                video.video_id = video_id
                video.title = 'tmp video'
                video.youtube_url = youtube_url
                video.swf_url = swf_url
                video.save()
                video_created.send(sender=video, video=video)
                uploaded_video.delete()
                return_only_data = request.GET.get('only_data')
                if return_only_data:
                    return HttpResponse(json.dumps({'video_id': video_id}), content_type='application/json')
                else:
                    try:
                        next_url = settings.YOUTUBE_UPLOAD_REDIRECT_URL
                    except AttributeError:
                        next_url = reverse('django_youtube.views.video', kwargs={'video_id': video_id})
                    return HttpResponseRedirect(next_url)
        except:
            import sys
            logger.error('Unexpected error: %s - %s' % (sys.exc_info()[0], sys.exc_info()[1]))
            return HttpResponse('error happened')
    form = YoutubeDirectUploadForm()
    if return_only_data:
        return HttpResponse(json.dumps({'error': 500}), content_type='application/json')
    else:
        return render_to_response('django_youtube/direct-upload.html', {'form': form}, context_instance=RequestContext(request))