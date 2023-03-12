#import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from email.mime.application import MIMEApplication
import socks
import os

#'proxy_port' should be an integer
#'PROXY_TYPE_SOCKS4' can be replaced to HTTP or PROXY_TYPE_SOCKS5
#socks.setdefaultproxy(socks.PROXY_TYPE_HTTP, "10.158.100.9", 8080)
#socks.wrapmodule(smtplib)

#os.environ["http_proxy"] = "http://10.158.100.9:8080"
#os.environ["https_proxy"] = "http://10.158.100.9:8080"

def sendemail(sender, passwd, to_receiver: list, cc_receiver: list, title='邮件标题', content='邮件内容', attachment='', attchname=''):
    """
    QQ mail support only
    sender，发送者
    passwd，发送人qq邮箱授权码。这个授权码,是在qq邮箱里账户设置里设置的三方授权码。用pop3
    to_receiver，接受人，可以传列表，给多个人发
    cc_receiver，抄送人，可以传列表，给多个人发
    title，邮箱标题
    content，邮件内容
    attachment，附件。传一个地址
    """
    # 1、设置发送者
    msg = MIMEMultipart()  # MIMEMultipart类可以放任何内容
    my_sender = sender
    my_pass = passwd
    # 接受者
    my_to_receiver = to_receiver
    my_cc_receiver = cc_receiver
    receiver = my_to_receiver + my_cc_receiver
    msg['From'] = formataddr(('发送者', my_sender))
    msg['To'] = ",".join(my_to_receiver)
    msg['Cc'] = ",".join(my_cc_receiver)

    # 2、设置邮件标题
    msg['Subject'] = title
    # 3、邮件内容
    my_content = content  # 邮件内容
    msg.attach(MIMEText(my_content, 'plain', 'utf-8'))  # 把内容加进去
    # 4、添加附件
    fujian = attachment  # 定义附件
    if fujian == '':  # 如果没传附件地址，就直接略过
        pass
    else:
        my_att = MIMEApplication(open(fujian, 'rb').read())  # 用二进制读附件
        my_att.add_header('Content-Disposition', 'attachment', filename=('gbk', '', attchname))
        msg.attach(my_att)  # 添加附件
    # 5、发送邮件
    try:
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(my_sender, my_pass)
        server.sendmail(my_sender, receiver, msg.as_string())
        print("邮件发送成功")
        server.quit()

    except Exception as n:
        print("Error: 无法发送邮件")
        print(n)

def qq_send_mail(date, file):
    sender_main = '531832298@qq.com'
    passwd_main = 'hvkujfgdeyrlbgfh' #这个授权码,是在qq邮箱里账户设置里设置的三方授权码。用pop3，就是Python脚本中登录邮箱时的密码，而不是你平时登录邮箱时的那个密码
    to_receiver_main = ['531832298@qq.com']
    CC_receiver_main = ['2959945199@qq.com']
    title_main = date
    content_main = """
        微博热搜榜
        """
    #attachment_main = r'C:\N-20S1PF344DFM-Data\yaweili\Downloads\2023-03-04.mp4'
    attachment_main = file

    attachment_name = os.path.basename(attachment_main)

    sendemail(
        sender=sender_main,
        passwd=passwd_main,
        to_receiver=to_receiver_main,
        cc_receiver=CC_receiver_main,
        title=title_main,
        content=content_main,
        attachment = attachment_main,
        attchname = attachment_name
    )

if __name__ == '__main__':

    qq_send_mail('2023-03-04', r'C:\N-20S1PF344DFM-Data\yaweili\Downloads\2023-03-04.mp4')

