import email
import imaplib
import smtplib
from email.mime.text import MIMEText

from Crypto.PublicKey import RSA

import crypto_sign

smtp_host = 'smtp.gmail.com'
smtp_port = 465


def send_email(from_addr, to_addr, username, password, subject, text, key_path):
    with open(key_path, "rb") as f:
        key = RSA.import_key(f.read())
        print(f.read())

    # key = RSA.generate(4096)

    pub_key = key.public_key().export_key()

    message = MIMEText(text)
    message['subject'] = subject
    message['from'] = from_addr
    message['to'] = to_addr
    message.add_header("pub_key", str(pub_key))
    message.add_header('sign', str(crypto_sign.sign_text(str(pub_key), text)))

    server = smtplib.SMTP_SSL(smtp_host, smtp_port)
    server.login(username, password)
    server.sendmail(from_addr, to_addr, message.as_string())
    server.quit()


def receive_mail(username, password, folder):
    mail = imaplib.IMAP4_SSL(smtp_host)
    mail.login(username, password)
    mail.select(folder)

    status, data = mail.search(None, 'ALL')
    mail_ids = []
    for block in data:
        mail_ids += block.split()

    for i in mail_ids:
        status, data = mail.fetch(i, '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                message = email.message_from_bytes(response_part[1])
                mail_from = message['from']
                mail_to = message['to']
                mail_subject = message['subject']
                sign = message['sign']
                pub_key = message['pub_key']

                if message.is_multipart():
                    mail_content = ''
                    for part in message.get_payload():
                        if part.get_content_type() == 'text/plain':
                            mail_content += part.get_payload()
                else:
                    mail_content = message.get_payload()

                print(f'From: {mail_from}')
                print(f'To: {mail_to}')
                print(f'Subject: {mail_subject}')
                print(f'Content: {mail_content}')
                print(f'Sign: {sign}')
                print(f'pub_key: {pub_key}')
                print(f'Verified: {crypto_sign.check_signature(sign, pub_key, mail_content)}')
