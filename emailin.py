from flask_mail import Message, Mail

def SendEmail(reciever, message):
        try:
                mail = Mail()
                msg = Message('Asset Management', sender = 'bunmistic@gmail.com')
                        # to use email change the url to localhost
                msg.add_recipient(reciever)
                msg.body = message
                mail.send(msg)
        except:
               print("Error occurred")

