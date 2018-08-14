# JIRA自动化教程(Python爬虫)
## 该脚本实现了:
1.按指定的条件搜索出对应的Jira列表,并将这些Jira的所有信息读取出来;
2.提取出有效信息,并按照写好的html模板将信息填入其中;
3.将该邮件发给Jira列表里包括的assignee人员和配置的默认收件人,assignee也会单独表明提醒;

## 适用于：
1.适合习惯看邮件,不习惯打开链接看jira的盆友;
2.每天跟踪进度,避免遗漏jira;
3.及时提醒/关闭已完成的jira;
4.jira有时效性,某些jira不及时关闭会影响组内kpi;
5.其他...

## zookeeper节点说明:
config : 正式配置, 每天早上7点跑的定时任务是从这里读取配置的;
test : 在上正式配置时, 先配置在这里测试下配置是否有问题,确认没问题再配到config节点(test节点配置不为空时,不会使用config的配置);
switch : 是否发送全员的一个临时配置, 不用管这个;
配置说明 : Json格式
{
"TodoList": { --------------任务key,具有唯一性
"key": "TodoList", --------------任务key,具有唯一性
"subject": "有待完成的任务", --------------邮件标题
"defaultReceiver": "suyongsheng@163.com", --------------默认收件人,可为空,多个收件人可用 ; 分隔,最终的收件人列表是:默认收件人+搜索出来的jira的assignee
"conditions": "assignee = suyongsheng AND resolution = Unresolved order by updated DESC", -------------- jira搜索条件,最终邮件里有哪些jira全靠这个搜索条件
"content": "目前还未解决的任务,每天会提醒一次,完成后记得关闭哦", --------------邮件正文备注,或者说明下这些jira为什么被搜到并发出邮件
"singleOrBatch": "single", --------------收件人配置,枚举值,single:单个发送,搜索出来的邮件assignee包含多个人,则单独发送给这些人,邮件正文只包含这些人的jira;batch:批量发送,收件人包含jira所有的assignee
"triggerDay": "0", --------------触发时间:1~7 分别代表周一~周日,0 代表每天
"status": "VALID", --------------是否生效,INVALID表示该配置不再生效
"memo": "配置备注" --------------配置备注,不会出现在邮件正文
}
}

# 配合Jenkins使用，可实现全自动化。
