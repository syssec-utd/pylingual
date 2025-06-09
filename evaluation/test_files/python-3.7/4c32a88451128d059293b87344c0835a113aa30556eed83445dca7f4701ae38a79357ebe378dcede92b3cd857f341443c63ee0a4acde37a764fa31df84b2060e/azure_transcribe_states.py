class AzureTranscribeStates(object):
    """
    Class for storing the states of Azure Transcribe.
    """
    NOT_STARTED = 'NotStarted'
    RUNNING = 'Running'
    FAILED = 'Failed'
    SUCCEEDED = 'Succeeded'