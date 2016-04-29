#!/usr/bin/python3

import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header



sender = '2222@163.com'
receivers = ['2222@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱




mail_msg = """
<p>发自 以色列 耶路撒冷</p>
<p>苦菜沾盐水、土豆、煮老的鸡蛋和一块烤羊颈骨，简单几道菜是以色列逾越节家宴上的必备菜式。</p>
<p><strong>逾越节是以色列三大重要宗教节日之一，在犹太人的文化中代表着重生与自由。</strong>它通常是在公历的四至五月份，具体时间依照当年犹太历（和中国的农历相似）的变动略有调整。今年，4 月 22 日至 29 日是以色列的逾越节。为了体验这个节庆，我特意从贝尔谢巴来到耶路撒冷，这是我第三年在正统派犹太人家过节。</p>
<blockquote>根据《旧约圣经》中《出埃及记》记载：以色列人在埃及受到法老的奴役，痛苦不堪。而后上帝召唤摩西，<strong>带领以色列人逃离埃及</strong>，前往应许之地迦南（今巴勒斯坦地区和以色列）。</blockquote>
<p>逾越节的习俗全部来自《旧约圣经》，<strong>他们吃无酵饼，用来纪念犹太人逃出埃及时的迫切，甚至都等不及面粉发酵；吃苦菜，用来铭记犹太人逃出埃及时所经受的苦难。<img class="content-image" src="https://pic4.zhimg.com/d198ded1ff6f5071335a706d509353cb_b.jpg" alt="" /></strong></p>

"""

msgRoot = MIMEText(mail_msg,'html','utf-8')
subject = '中国人去朝鲜旅游有什么注意事项？ - 知乎'
msgRoot['Subject'] = subject


# 指定图片为当前目录
'''fp = open('test.png', 'rb')
msgImage = MIMEImage(fp.read())
fp.close()

# 定义图片 ID，在 HTML 文本中引用
msgImage.add_header('Content-ID', '<image1>')
msgRoot.attach(msgImage)
'''
#try:
smtpObj = smtplib.SMTP()
smtpObj.connect('smtp.163.com', 25)
smtpObj.login(sender, '*******')
smtpObj.sendmail(sender, receivers, msgRoot.as_string())
print ("邮件发送成功")
smtpObj.close()

#except smtplib.SMTPException:
#    print ("Error: 无法发送邮件")