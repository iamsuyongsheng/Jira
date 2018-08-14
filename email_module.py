# encoding=utf-8
# ----------------------------------------
# 语言：Python2.7
# 功能：邮件模板
# ----------------------------------------
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jira_module import get_cc_address, get_cc_assignees
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

DEFAULT_SENDER = 'suyongsheng@163.com'  # 默认发送者


# 读取邮件内容配置
def get_email_conf(conf_name):
	try:
		email_conf = json.load(open(conf_name))
	except Exception, e:
		print "读取Json文件异常:" + e.message
	else:
		return email_conf


def get_t_table(jira_dict):
	t_table = ''
	for jira in jira_dict:
		email_temp = '''
					<tr>
		            <td><span class="check">%s</span></td>
		            <td><a href=%s class="check">%s</a></td>
		            <td><span class="check">%s</span></td>
		            <td><span class="check">%s</span></td>
					<td><span class="check">%s</span></td>
	                <td><span class="check">%s</span></td>
	                <td><span class="check">%s</span></td>
		            <td><span class="check">%s</span></td>
					<td><span class="check">%s</span></td>
		            </tr>
			''' % (jira['issuetype'],jira['issuelink'],jira['issuekey'],jira['summary'],jira['priority'],
		           jira['assignee'],jira['reporter'],jira['created'],jira['updated'],jira['duedate'])
		t_table += email_temp
	return t_table


# email 模块
def send_email(email_dict, jira_dict):
	if email_dict is None:
		print "读取到的email配置为空"
		return

	print "[" + email_dict['subject'] + "] 正在构造邮件,请稍等..."

	if email_dict['content']:
		content = email_dict['content']
	else:
		content = '[默认提示]以下Jira需要被关注'
	t_table = get_t_table(jira_dict)
	cc_address = get_cc_address(jira_dict)
	cc_assignees = get_cc_assignees(jira_dict)
	subject = email_dict['subject']
	receiver = cc_address + email_dict['defaultReceiver']  # 将爬取到的assignee添加到收件人列表
	to_addrs = receiver.split(';')
	# 构造邮件对象MIMEMultipart对象
	msg = MIMEMultipart('mixed')
	msg['Subject'] = subject
	# 收件人为多个收件人,通过join将列表转换为以,为间隔的字符串
	msg['To'] = ",".join(to_addrs)

	# 构造html
	html = """
		<!DOCTYPE html>
		<html>
		<head>
		    <meta charset="utf-8">
		    <title>Jira自动汇总</title>
		    <style type="text/css">
		        *{
		            margin: 0;
		            padding: 0;
		        }
		        body{
		            font: italic 20px Georgia, serif;
		            letter-spacing: normal;
		            background-color: #f0f0f0;
		        }
		        #content{
		            width: 800px;
		            padding: 40px;
		        }
		        #table1{
		            font: bold 16px/1.4em "Trebuchet MS", sans-serif;
		        }
		        #table1 thead th{
		            padding: 15px;
		            border: 1px solid #93CE37;
		            border-bottom: 3px solid #9ED929;
		            text-shadow: 1px 1px 1px #568F23;
		            color: #fff;
		            background-color: #9DD929;
		            border-radius: 5px 5px 0px 0px;
		        }
		        #table1 thead th:empty{
		            background-color: transparent;
		            border: none;
		        }
		        #table1 tbody th{
		            padding: 0px 10px;
		            border: 1px solid #93CE37;
		            border-right: 3px solid #9ED929;
		            text-shadow: 1px 1px 1px #568F23;
		            color: #666;
		            background-color: #9DD929;
		            border-radius: 5px 0px 0px 5px;
		        }
		        #table1 tbody td{
		            padding: 10px;
		            border: 2px solid #E7EFE0;
		            text-align: center;
		            text-shadow: 1px 1px 1px #fff;
		            color: #666;
		            background-color: #DEF3CA;
		            border-radius: 2px;
		        }
		    </style>
		</head>
		<body>
		<b>原因 : </b>%s<br>
		<b>名单 : </b><span style="color:blue;font-weight:bold"><b>%s</b></span><br/><br/>
		请在列同学及时关注并更新 jira状态.( 本邮件为自动发送,请勿回复 )
		<div id="content">
		    <table id="table1">
		        <thead>
		            <tr>
						<th scope="col" abbr="Starter">Issue Type</th>
		                <th scope="col" abbr="Starter">Key</th>
		                <th scope="col" abbr="Medium">Summary</th>
		                <th scope="col" abbr="Business">Priority</th>
		                <th scope="col" abbr="Deluxe">Assignee</th>
						<th scope="col" abbr="Deluxe">Reporter</th>
						<th scope="col" abbr="Deluxe">Created</th>
						<th scope="col" abbr="Deluxe">Updated</th>
						<th scope="col" abbr="Deluxe">Due Date</th>
		            </tr>
		        </thead>
		        <tbody>
					%s
		        </tbody>
		    </table>
		</div>
		<address>
		Written by <a href="mailto:suyongsheng@163.com">Su Yongsheng</a>.<br>
		Visit me at : Xiaobailou 203<br>
		</address>
		</body>
		</html>
		""" % (content, cc_assignees, t_table)

	text_html = MIMEText(html, 'html', 'utf-8')
	msg.attach(text_html)
	try:
		smtp = smtplib.SMTP()
		smtp.connect("mail.srv")
		smtp.sendmail(DEFAULT_SENDER, to_addrs, msg.as_string())
		smtp.close()
		print "[%s] send email success" % subject
	except Exception, e:
		print "Error:[%s] unable to send email becauseof " % subject + e.message


# 报警邮件
def send_alarm_email(errMsg):
	subject = 'Jira自动化报警邮件'
	receiver = 'suyongsheng@163.com'
	to_addrs = receiver.split(';')
	msg = MIMEMultipart('mixed')
	msg['Subject'] = subject
	msg['To'] = ",".join(to_addrs)

	# 构造html
	html = """
		<!DOCTYPE html>
		<html>
		<body>
		<h1 id="blink"><b>Jira邮件发送异常</b></h1>
		<p><b><font size="5">报警原因:%s</font></b></p>
		<script language="javascript">
		    function changeColor(){
		        var color="#f00|#000";
		        color=color.split("|");
		        document.getElementById("blink").style.color=color[parseInt(Math.random() * color.length)];
		    }
		    setInterval("changeColor()",200);
		</script>
		</body>
		</html>
		""" % (errMsg)

	text_html = MIMEText(html, 'html', 'utf-8')
	msg.attach(text_html)
	try:
		smtp = smtplib.SMTP()
		smtp.connect("mail.srv")
		smtp.sendmail(DEFAULT_SENDER, to_addrs, msg.as_string())
		smtp.close()
		print "[%s] send alarm email success" % subject
	except Exception, e:
		print "Error:[%s] unable to send alarm email becauseof " % subject + e.message
