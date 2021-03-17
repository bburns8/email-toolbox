import yagmail

receiver = 'test@smartCDR.com'
body = 'Hello from Yagmail!'
filename = 'download.jpg'

yag = yagmail.SMTP('bburns858@gmail.com')
yag.send(
    to=receiver,
    subject='Yagmail test with attachment',
    contents=body,
    attachments=filename,
)
