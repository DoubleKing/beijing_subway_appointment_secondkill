# encoding=utf8
from second_kill.config import global_config
from second_kill.logger import g_logger
from second_kill.timer import Timer
import time
import multiprocessing
import requests
import json
from datetime import date, timedelta
import random
from urllib import unquote
from requests_toolbelt.utils import dump
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def create_appointment(authorization, tomorrow, timeSlot):
	headers = {
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
		'authorization': authorization,
		'content-type': 'application/json;charset=UTF-8'}
	data_dic = {"lineName": global_config.lineName, "snapshotWeekOffset": 0, "stationName": global_config.stationName,
				"enterDate": tomorrow, "snapshotTimeSlot": "0630-0930", "timeSlot": timeSlot}
	data = json.dumps(data_dic)
	r = requests.post('https://webapi.mybti.cn/Appointment/CreateAppointment', headers=headers, data=data)
	g_logger.info(dump.dump_all(r).decode('utf-8'))


# [{"timeSlotQueryString":"沙河站-20210115-0740-0750","balance":0,"status":1,"appointmentId":null},{"timeSlotQueryString":"沙河站-20210115-0750-0800","balance":0,"status":1,"appointmentId":null},{"timeSlotQueryString":"沙河站-20210115-0800-0810","balance":0,"status":1,"appointmentId":null}]
def is_has_appointment(res):
	length = len(res)
	for r in res:
		if r["appointmentId"]:
			return True
	return False


def create_appointment_if_has_balance(res, authorization, tomorrow):
	length = len(res)
	for r in res:
		if r["balance"] or r["status"] != 1:
			timeSlot = r["timeSlotQueryString"][-9:]
			create_appointment(authorization, tomorrow, timeSlot)


def get_balance(authorization, tomorrow):
	try:
		headers = {
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
			'authorization': authorization,
			'content-type': 'application/json;charset=UTF-8'}
		data_dic = {"timeSlot": global_config.timeSlot, "stationName": global_config.stationName,
					"enterDates": [tomorrow]}
		data = json.dumps(data_dic)
		r = requests.post('https://webapi.mybti.cn/Appointment/GetBalance', headers=headers, data=data)
		# print r.status_code
		g_logger.info(dump.dump_all(r).decode('utf-8'))
		if r.status_code != 200:
			return False
		res = json.loads(r.text)

		if is_has_appointment(res):
			# 已经有预约返回成功
			return True
		else:
			create_appointment_if_has_balance(res, authorization, tomorrow)
	except Exception as e:
		global_config.info(e)
		return False
	return False


def request_process(authorization, tomorrow):
	t = Timer()
	# 到开始时间开始刷票
	t.start()
	while True:
		if get_balance(authorization, tomorrow):
			# 刷到票退出进程
			break
		else:
			# 防止过快的请求服务器
			time.sleep(round(random.uniform(0.3, 0.6), 2))
		# 到截止时间刷不到票退出进程
		if int(round(time.time() * 1000)) > t.end_date_time_ms:
			break


def request_process_pool():
	tomorrow = (date.today() + timedelta(days=1)).strftime("%Y%m%d")
	authorization = global_config.authorization
	pool = multiprocessing.Pool(processes=len(authorization))
	for i in xrange(len(authorization)):
		# 每个账号启动一个进程刷明天的票
		pool.apply_async(request_process, (authorization[i], tomorrow))
	pool.close()
	pool.join()


if __name__ == '__main__':
	a = """

		  .oooooo..o                     oooo         o8o  oooo  oooo  
		 d8P'    `Y8                     `888         `"'  `888  `888  
		 Y88bo.       .ooooo.   .ooooo.   888  oooo  oooo   888   888  
		  `"Y8888o.  d88' `88b d88' `"Y8  888 .8P'   `888   888   888  
		      `"Y88b 888ooo888 888        888888.     888   888   888  
		 oo     .d8P 888    .o 888   .o8  888 `88b.   888   888   888  
		 8""88888P'  `Y8bod8P' `Y8bod8P' o888o o888o o888o o888o o888o 
    """
	print(a)
	today = -1
	while True:
		localtime = time.localtime(time.time())
		# 周天、周一、周二、周三、周四启动刷票（预约进站名额）进程池
		if localtime.tm_wday in [0, 1, 2, 3, 6] and localtime.tm_mday != today:
			today = localtime.tm_mday
			request_process_pool()
		time.sleep(1)
