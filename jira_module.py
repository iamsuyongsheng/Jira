# encoding=utf-8
# ----------------------------------------
# 语言：Python2.7
# 功能：jira模板,含登录和获取列表
# ----------------------------------------
import base64
import json

from jira import JIRA

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

JIRA_SERVER = 'http://jira.n.company.com'  # jira服务器
JIRA_FIELDS = 'issuetype,issuekey,summary,priority,status,resolution,assignee,reporter,created,duedate,updated'
MAX_RESULTS = 100  # 最多读取100条记录


# jira登录
def _login():
	login_info = json.load(open('../configurations/login.conf'))  # 加载登录信息
	# 需要先解码再使用
	login_info['user'] = base64.decodestring(login_info['user'])
	login_info['pwd'] = base64.decodestring(login_info['pwd'])
	basic_auth = (login_info['user'], login_info['pwd'])
	try:
		jira = JIRA(server=JIRA_SERVER, basic_auth=basic_auth)
	except Exception, e:
		print "Jira登录异常:" + e.message
	else:
		return jira


# 根据条件查找并返回issues
def get_issues(conditions):
	jira = _login()
	dict_list = []
	conditions = conditions.split(';')  # 支持多个条件组合查询,以;分割
	for condition in conditions:
		issues = jira.search_issues(condition, maxResults=MAX_RESULTS, fields=JIRA_FIELDS)
		for issue in issues:
			issue_type = str(issue.fields.issuetype)
			issue_key = str(issue)
			summary = str(issue.fields.summary.encode('utf-8'))
			priority = str(issue.fields.priority)
			status = str(issue.fields.status)
			resolution = str(issue.fields.resolution)
			assignee = str(issue.fields.assignee)
			reporter = str(issue.fields.reporter)
			created = str(issue.fields.created)[0:19]  # 截取时间
			due_date = str(issue.fields.duedate)[0:19]
			updated = str(issue.fields.updated)[0:19]
			issue_link = 'http://jira.n.company.com/browse/' + issue_key
			address = str(issue.fields.assignee.emailAddress)
			display_name = str(issue.fields.assignee.displayName)

			# 创建jira字典并返回
			issue_dict = {
				'issuetype': issue_type,
				'issuekey': issue_key,
				'summary': summary,
				'priority': priority,
				'status': status,
				'resolution': resolution,
				'assignee': assignee,
				'reporter': reporter,
				'created': created,
				'duedate': due_date,
				'updated': updated,
				'issuelink': issue_link,
				'address': address,
				'displayName': display_name
			}
			dict_list.append(issue_dict)
	return dict_list


# 按照assignee排列搜索出issues,返回字典格式
def get_issues_by_assignee(conditions):
	sorted_issues = get_issues(conditions)
	print sorted_issues
	print "get issues by assignee"
	issues_by_assignee = {}  # key:assignee,value:jiras of assignee
	for issue in sorted_issues:
		assignee = issue['assignee']
		if assignee in issues_by_assignee.keys():
			issues_by_assignee[assignee].append(issue)
		else:
			temp_dict = []
			temp_dict.append(issue)
			issues_by_assignee[assignee] = temp_dict
		print str(issues_by_assignee)
	if issues_by_assignee is None:
		print "issues_by_assignee is null"
	return issues_by_assignee


# 获取去重后的收信人列表
def get_cc_address(jira_dict):
	cc_address = ''
	for jira in jira_dict:
		address = jira['address']
		if address not in cc_address:
			cc_address += address + ";"
	return cc_address


# 获取收信人姓名
def get_cc_assignees(jira_dict):
	cc_assignees = ''
	for jira in jira_dict:
		assignee = jira['assignee']
		if assignee not in cc_assignees:
			cc_assignees += "@" + jira['displayName'] + " "  # jira里的姓名以@分隔
	return cc_assignees
