def _request_activity_data(self, athlete, filename):
    """Actually do the request for activity filename
        This call is slow and therefore this method is memory cached.

        Keyword arguments:
        athlete -- Full name of athlete
        filename -- filename of request activity (e.g. '2015_04_29_09_03_16.json')
        """
    response = self._get_request(self._activity_endpoint(athlete, filename)).json()
    activity = pd.DataFrame(response['RIDE']['SAMPLES'])
    activity = activity.rename(columns=ACTIVITY_COLUMN_TRANSLATION)
    activity.index = pd.to_timedelta(activity.time, unit='s')
    activity.drop('time', axis=1, inplace=True)
    return activity[[i for i in ACTIVITY_COLUMN_ORDER if i in activity.columns]]