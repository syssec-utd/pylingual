def parse_email(data, strip_attachment_payloads=False):
    """
    A simplified email parser

    Args:
        data: The RFC 822 message string, or MSG binary
        strip_attachment_payloads (bool): Remove attachment payloads

    Returns (dict): Parsed email data
    """
    if type(data) == bytes:
        if is_outlook_msg(data):
            data = convert_outlook_msg(data)
        data = data.decode('utf-8', errors='replace')
    parsed_email = mailparser.parse_from_string(data)
    headers = json.loads(parsed_email.headers_json).copy()
    parsed_email = json.loads(parsed_email.mail_json).copy()
    parsed_email['headers'] = headers
    if 'received' in parsed_email:
        for received in parsed_email['received']:
            if 'date_utc' in received:
                if received['date_utc'] is None:
                    del received['date_utc']
                else:
                    received['date_utc'] = received['date_utc'].replace('T', ' ')
    if 'from' not in parsed_email:
        if 'From' in parsed_email['headers']:
            parsed_email['from'] = parsed_email['Headers']['From']
        else:
            parsed_email['from'] = None
    if parsed_email['from'] is not None:
        parsed_email['from'] = parse_email_address(parsed_email['from'][0])
    if 'date' in parsed_email:
        parsed_email['date'] = parsed_email['date'].replace('T', ' ')
    else:
        parsed_email['date'] = None
    if 'reply_to' in parsed_email:
        parsed_email['reply_to'] = list(map(lambda x: parse_email_address(x), parsed_email['reply_to']))
    else:
        parsed_email['reply_to'] = []
    if 'to' in parsed_email:
        parsed_email['to'] = list(map(lambda x: parse_email_address(x), parsed_email['to']))
    else:
        parsed_email['to'] = []
    if 'cc' in parsed_email:
        parsed_email['cc'] = list(map(lambda x: parse_email_address(x), parsed_email['cc']))
    else:
        parsed_email['cc'] = []
    if 'bcc' in parsed_email:
        parsed_email['bcc'] = list(map(lambda x: parse_email_address(x), parsed_email['bcc']))
    else:
        parsed_email['bcc'] = []
    if 'delivered_to' in parsed_email:
        parsed_email['delivered_to'] = list(map(lambda x: parse_email_address(x), parsed_email['delivered_to']))
    if 'attachments' not in parsed_email:
        parsed_email['attachments'] = []
    else:
        for attachment in parsed_email['attachments']:
            if 'payload' in attachment:
                payload = attachment['payload']
                try:
                    if 'content_transfer_encoding' in attachment:
                        if attachment['content_transfer_encoding'] == 'base64':
                            payload = decode_base64(payload)
                        else:
                            payload = str.encode(payload)
                    attachment['sha256'] = hashlib.sha256(payload).hexdigest()
                except Exception as e:
                    logger.debug('Unable to decode attachment: {0}'.format(e.__str__()))
        if strip_attachment_payloads:
            for attachment in parsed_email['attachments']:
                if 'payload' in attachment:
                    del attachment['payload']
    if 'subject' not in parsed_email:
        parsed_email['subject'] = None
    parsed_email['filename_safe_subject'] = get_filename_safe_string(parsed_email['subject'])
    if 'body' not in parsed_email:
        parsed_email['body'] = None
    return parsed_email