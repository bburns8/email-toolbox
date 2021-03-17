import os
import email
import imaplib
import traceback
from pathlib import PurePath
from DTOs import DataManagerEmail, DataManagerFile
from utils.logger import logger
from utils.exceptions import ImportException
from app import app


class EmailConsumer:
    def __init__(self, server, port, username, password):
        self._server = server
        self._port = port
        self._username = username
        self._password = password
        self._conn = None

    def get_emails(self, max_count):
        try:
            self._connect()
            emails = []
            while len(emails) < max_count:
                email = self._get_email()
                if not email:
                    break
                emails.append(email)
            return emails
        except ImportException as e:
            logger.error('[Email Consumer] Error while retrieving emails: ' + e.message)
            raise
        except:
            logger.error('[Email Consumer] Error while retrieving emails: ' + traceback.format_exc())
            raise ImportException('Unable to retrieve emails')
        finally:
            self._disconnect()

    def _get_email(self):

        if not self._select_inbox():
            raise ImportException('Unable to select inbox')

        email_ids = self._get_email_ids()
        if not email_ids:
            logger.info('[Email Consumer] No unread emails in inbox')

        return self._get_first_email_with_attachments(email_ids)

    def _select_inbox(self):
        typ, data = self._conn.select('inbox')
        if typ == 'OK':
            return True
        logger.error('[Email Consumer] Unable to select inbox')
        return False

    def _get_email_ids(self):
        typ, data = self._conn.search(None, 'ALL')
        if typ != 'OK':
            logger.error('[Email Consumer] Unable to get list of inbox emails')
            return []

        return data[0].split()

    def _get_first_email_with_attachments(self, email_ids):
        for msg_id in email_ids:
            message = self._fetch_message(msg_id)
            if not message:
                continue

            body = message[0][1]
            mail = email.message_from_string(body.decode('utf-8'))

            subject = mail['Subject']
            sender = mail['From']

            attachments = self._get_attachments_for_mail(mail, subject, sender)
            if not attachments:
                continue

            self._delete_from_server(msg_id)

            return DataManagerEmail(msg_id, subject, sender, attachments)

        logger.info('[Email Consumer] No messages with attachments')
        return None

    def _fetch_message(self, msg_id):
        typ, massage_parts = self._conn.fetch(msg_id, '(RFC822)')
        if typ == 'OK':
            return massage_parts

        logger.error('[Email Consumer] Error fetching message for id: ' + msg_id)
        return None

    def _get_attachments_for_mail(self, mail, subject, sender):
        attachments = []

        for part in mail.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            filename = part.get_filename()

            if bool(filename):
               attachments.append(self._save_attachment(part, filename, sender, subject))

        return attachments

    def _delete_from_server(self, msgid):
        msg_id = msgid.decode('utf-8')
        if 'GMAIL' in self._server.upper():
            typ, massage_parts = self._conn.store("1:{0}".format(msg_id), '+X-GM-LABELS', '\\Trash')  # move to trash
        else:
            typ, massage_parts = self._conn.store("1:{0}".format(msg_id), '+FLAGS', '(\Deleted)')

        if typ != 'OK':
            logger.error('[Email Consumer] Error updating message for id: ' + msg_id + ' for delete')
            return
        logger.debug('[Email Consumer] Message set to delete for id: ' + msg_id)

        typ, massage_parts = self._conn.expunge()
        if typ != 'OK':
            logger.error('[Email Consumer] Error deleting message id: ' + msg_id)
            return
        logger.debug('[Email Consumer] Deleted message for id: ' + msg_id)
        return

    def _connect(self):
        try:
            self._conn = imaplib.IMAP4_SSL(self._server, self._port)
            typ, acc_details = self._conn.login(self._username, self._password)
            if typ == 'OK':
                return True
        except:
            logger.error('Unable to connect to server: ' + traceback.format_exc())
            raise ImportException('Unable to connect to server')

        logger.error('[Email Consumer] Unable to login to email')
        return False

    def _disconnect(self):
        if self._conn:
            self._conn.close()
            self._conn.logout()
            self._conn = None

    @staticmethod
    def _save_attachment(part, filename, sender, subject):
        data_file = DataManagerFile(filename, str(PurePath(app.config.TEMP_DIR).joinpath(filename)),
                                    sender, subject)
        data = part.get_payload(decode=True)
        with open(data_file.path, 'wb') as f:
            f.write(data)

        data_file.size = os.path.getsize(data_file.path)
        return data_file