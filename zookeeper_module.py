# encoding=utf-8
# ----------------------------------------
# 语言：Python2.7
# 功能：从zookeeper读取配置
# 位置:/company/cash/jira/config
# ----------------------------------------
import zookeeper
from data_module import get_hour


# 获取zookeeper配置
def get_zk_data():
	zk = zookeeper.init("zk.staging.srv:8080")  # 初始化zookeeper
	try:
		zk_children = zookeeper.get_children(zk, "/company/cash/jira")
		#  如果test节点存在,则不会运行config节点,方便对新配置进行测试
		if 'test' in zk_children:
			zk_test = zookeeper.get(zk, "/company/cash/jira/test")
			if zk_test[0] is not '':
				print '测试节点不为空,将使用测试节点的配置...'
				return zk_test[0]
	except Exception, e:
		print e.message
	#   目前只判断了test和config两个节点,后期如果有较多人使用,则添加扫描其他节点
	zk_config = zookeeper.get(zk, "/company/cash/jira/config")
	zookeeper.close(zk)
	return zk_config[0]


# 清空test配置,保证每天定时能够顺利执行
def del_test_data():
	hour = int(get_hour())
	zk = zookeeper.init("zk.staging.srv:8080")
	try:
		if 0 <= hour <= 7:  # 00:00~08:00之间的test配置会被清空
			zk_children = zookeeper.get_children(zk, "/company/cash/jira")
			if 'test' in zk_children:
				zk_test = zookeeper.get(zk, "/company/cash/jira/test")
				# 如果test节点存在且不为空,则清空配置
				if zk_test[0] is not '':
					zookeeper.set(zk, "/company/cash/jira/test", "")
	except Exception, ex:
		print ex.message
	zookeeper.close
