def authenticate_twitch_oauth():
    """Opens a web browser to allow the user to grant Streamlink
       access to their Twitch account."""
    client_id = TWITCH_CLIENT_ID
    redirect_uri = 'https://streamlink.github.io/twitch_oauth.html'
    url = 'https://api.twitch.tv/kraken/oauth2/authorize?response_type=token&client_id={0}&redirect_uri={1}&scope=user_read+user_subscriptions&force_verify=true'.format(client_id, redirect_uri)
    console.msg('Attempting to open a browser to let you authenticate Streamlink with Twitch')
    try:
        if not webbrowser.open_new_tab(url):
            raise webbrowser.Error
    except webbrowser.Error:
        console.exit('Unable to open a web browser, try accessing this URL manually instead:\n{0}'.format(url))