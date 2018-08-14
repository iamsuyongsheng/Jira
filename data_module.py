# encoding=utf-8
# ----------------------------------------
# 语言：Python2.7
# 功能：获取日期&时间
# ----------------------------------------
import datetime
NOW = datetime.datetime.now()


# 获取当前月份
def get_month():
	month = NOW.month
	return month


# 获取当前日期
def get_day():
	day = NOW.day
	return day


# 获取当前小时
def get_hour():
	hour = NOW.hour
	return hour


# 获取当前分钟
def get_minute():
	minute = NOW.minute
	return minute


# 获取当前星期
def get_weekday():
	weekday = NOW.weekday() + 1  # 1~7:分别代表周一~周日
	return int(weekday)