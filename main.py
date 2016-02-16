from __future__ import unicode_literals
import logging

logging.basicConfig()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from imapclient import IMAPClient

ssl = True

from envparse import env



env.read_envfile()

if __name__ == '__main__':
    logger.info('start IMAP')

    server = IMAPClient(env('HOST'), use_uid=True, ssl=ssl)

    logger.info(' [+] LOGIN')
    server.login(env('USERNAME'), env('PASSWORD'))

    select_info = server.select_folder('INBOX')
    print('%d messages in INBOX' % select_info['EXISTS'])

    messages = server.search(['NOT', 'DELETED'])
    print("%d messages that aren't deleted" % len(messages))

    print()
    print("Messages:")
    # https://tools.ietf.org/html/rfc3501.html#section-6.4.5
    response = server.fetch(messages, ['FLAGS', 'ENVELOPE', ])
    for msgid, data in response.iteritems():
        print(''' ---ID %d ---
HEADER: %s
flags=%s''' % (msgid, data[b'ENVELOPE'], data[b'FLAGS']))
