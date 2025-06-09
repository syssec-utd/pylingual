def safe_start_ingest(event):
    """Start a capture process but make sure to catch any errors during this
    process, log them but otherwise ignore them.
    """
    try:
        ingest(event)
    except Exception:
        logger.error('Something went wrong during the upload')
        logger.error(traceback.format_exc())
        recording_state(event.uid, 'upload_error')
        update_event_status(event, Status.FAILED_UPLOADING)
        set_service_status_immediate(Service.INGEST, ServiceStatus.IDLE)