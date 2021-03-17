# import python poplib module
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import poplib

# input email address, password, and pop3 server domain or ip address
email = input('Email: ')
password = input('Password: ')
pop3_server = input('POP3 server: ')

# connect to pop3 server:
server = poplib.POP3(pop3_server)

# open debug switch to print debug info between client and pop3 server
server.set_debuglevel(1)

# get pop3 server welcome message.
pop3_server_welcome_msg = server.getwelcome().decode('utf-8')

# print out the pop3 server welcome message.
print(server.getwelcome().decode('utf-8'))

# user account authentication
server.user(email)
server.pass_(password)

# stat() function return email count and occupied disk size
print('Messages: %s. Size: %s' % server.stat())

# list() function return all email list
resp, mails, octets = server.list()
print(mails)

# retrieve the newest email index number
index = len(mails)

# server.retr function can get the contents of the email with index variable value index number.
resp, lines, octets = server.retr(index)

# lines stores each line of the original text of the message
# so that you can get the original text of the entire message use the join function and lines variable.
msg_content = b'\r\n'.join(lines).decode('utf-8')

# now parse out the email object
msg = Parser().parsestr(msg_content)

# get email from, to, subject attribute value.
email_from = msg.get('From')
email_to = msg.get('To')
email_subject = msg.get('Subject')
print('From ' + email_from)
print('To ' + email_to)
print('Subject ' + email_subject)

# delete the email from pop3 server directly by email index.
# server.dele(index)
# close pop3 server connection.
server.quit()


# variable indent_number is used to decide number of indent of each level in the mail multiple bory part.
def print_info(msg, indent_number=0):
    if indent_number == 0:
        # loop to retrieve from, to, subject from email header.
        for header in ['From', 'To', 'Subject']:
            # get header value
            value = msg.get(header, '')
            if value:
                # for subject header.
                if header == 'Subject':
                    # decode the subject value
                    value = decode_str(value)
                # for from and to header.
                else:
                    # parse email address
                    hdr, addr = parseaddr(value)
                    # decode the name value.
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            print('%s%s: %s' % (' ' * indent_number, header, value))
    # if message has multiple part.
    if (msg.is_multipart()):
        # get multiple parts from message body.
        parts = msg.get_payload()
        # loop for each part
        for n, part in enumerate(parts):
            print('%spart %s' % (' ' * indent_number, n))
            print('%s--------------------' % (' ' * indent_number))
            # print multiple part information by invoke print_info function recursively.
            print_info(part, indent + 1)
    # if not multiple part.
    else:
        # get message content mime type
        content_type = msg.get_content_type()
        # if plain text or html content type.
        if content_type == 'text/plain' or content_type == 'text/html':
            # get email content
            content = msg.get_payload(decode=True)
            # get content string charset
            charset = guess_charset(msg)
            # decode the content with charset if provided.
            if charset:
                content = content.decode(charset)
            print('%sText: %s' % (' ' * indent_number, content + '...'))
        else:
            print('%sAttachment: %s' % (' ' * indent_number, content_type))


# the subject of the messgae or the name contained in the Email is encoded string.
# , which must decode for it to display properly, this function just provide the feature
def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


# check email content string encoding charset.
def guess_charset(msg):
    # get charset from message object.
    charset = msg.get_charset()
    # if can not get charset
    if charset is None:
        # get message header content-type value and retrieve the charset from the value.
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset
