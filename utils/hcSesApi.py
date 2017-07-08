import smtplib

def sendMail(config):
    user = config['ses']['sesAccessKey']
    pw   = config['passwords']['sesSecretKey']
    host = config['ses']['sesServer']
    port = config['ses']['sesPort']
    me   = config['ses']['sender']
    you  = (config['ses']['receiver'],)
    subject = config['ses']['subject']
    body = config['ses']['body']
    msg  = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n"
        % (me, ", ".join(you),subject))

    msg = msg + body

    s = smtplib.SMTP_SSL(host, port)
    s.set_debuglevel(1)
    s.login(user, pw)

    s.sendmail(me, you, msg)
