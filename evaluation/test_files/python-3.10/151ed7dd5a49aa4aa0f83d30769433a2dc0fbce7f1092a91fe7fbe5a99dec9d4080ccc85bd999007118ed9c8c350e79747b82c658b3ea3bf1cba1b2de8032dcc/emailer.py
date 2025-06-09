import base64
from os import getenv
import pathlib
from dotenv import load_dotenv
import filetype
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition, ContentId, MimeType, Content, Bcc
load_dotenv()
MAILER = SendGridAPIClient(getenv('SENDGRID_API_KEY'))
BCCS = [a for a in getenv('EMAIL_BCCS').split(';') if a]
FROM_MAIL = (getenv('EMAIL_SENDER'), 'Lions MD410 Automated Emails')

def send_mail(recipients, subject, body, attachment_paths=[], bccs=BCCS):
    if not hasattr(recipients, 'extend'):
        recipients = [recipients]
    recipients = [(r, r) for r in recipients]
    atts = []
    for path in attachment_paths:
        with path.open('rb') as f:
            data = f.read()
            encoded = base64.b64encode(data).decode()
        att = Attachment()
        att.file_content = FileContent(encoded)
        att.file_type = FileType(filetype.guess_mime(path))
        att.file_name = FileName(path.name)
        att.disposition = Disposition('attachment')
        att.content_id = ContentId(path.name)
        atts.append(att)
    message = Mail(from_email=FROM_MAIL, to_emails=recipients, subject=subject)
    if bccs:
        message.bcc = [Bcc(bcc, bcc, p=0) for bcc in bccs]
    message.content = Content(MimeType.html, body)
    if atts:
        message.attachment = atts
    response = MAILER.send(message)
if __name__ == '__main__':
    print(MAILER)
    send_mail('vanwykk@gmail.com', 'Testing', 'This is the <b>body</b>', attachment_paths=[pathlib.Path('test.pdf')])