#!/usr/bin/python
# -*- coding:utf-8 -*-
from utils.config_util import ConfigUtil
from email.mime.text import MIMEText
from email.header import Header
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import smtplib
import datetime


class MailUtil:
    def __init__(self):
        conf = ConfigUtil()
        self.mail_addr = conf.get_config(conf='mail_addr',section='mail_conf')
        self.smtp_server = conf.get_config(conf='smtp_server', section='mail_conf')
        self.password = conf.get_config(conf='password', section='mail_conf')
        self.url = conf.get_config(conf='url')
        self.SECRET_KEY = conf.get_config(conf='SECRET_KEY')

    def send_confirm_mail(self, username, email):
        content = u"""
    <p>你好,{username}!</p>
    <p>    您已使用本邮箱注册成为数据狗的点点滴滴,感谢您对数据狗的点点滴滴的关注,请在30分钟内点击下面的链接激活该邮箱,如非本人操作请忽略该邮件</p>
        <br><a href = {url}>====>> 没问题,该邮箱是我注册的 <<==== </a><br><br>
        您也可以通过复制下面的链接在浏览器中直接访问,激活邮箱<br>
        <a href = {url}>{url}</a><br>
<br><th>
    致礼!<br>
    -- {date}<br>
    by 数据狗的点点滴滴<br>
        """
        ser = Serializer(self.SECRET_KEY, expires_in=1800)
        token = ser.dumps(email)

        msg = MIMEText(content.format(
            username=username,
            url=self.url + '/auth/confirm/' + token,
            date=datetime.datetime.now().strftime('%Y-%m-%d')
        ), 'html', 'utf-8')

        msg['Subject'] = Header('数据狗——注册激活邮件', 'utf-8')
        msg['From'] = self.mail_addr
        msg['To'] = email

        smtp = smtplib.SMTP()
        smtp.connect(self.smtp_server)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(self.mail_addr, self.password)
        smtp.sendmail(self.mail_addr, email, msg.as_string())
        smtp.quit()


if __name__ == '__main__':
    MailUtil().send_confirm_mail('renjie', 'zjurj@outlook.com')