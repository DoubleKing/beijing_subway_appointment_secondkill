# encoding=utf8
import time

import datetime
from logger import g_logger
from config import global_config


class Timer(object):
	def __init__(self, sleep_interval=0.5):
		self.sleep_interval = sleep_interval
		today = datetime.date.today()
		tomorrow = today + datetime.timedelta(days=1)
		start_time = global_config.start_time
		next_day_end_time = global_config.next_day_end_time
		print today.year.__str__() + '-' + today.month.__str__() + '-' + today.day.__str__() + ' ' + start_time

		start_date_time = datetime.datetime.strptime(today.year.__str__() + '-' + today.month.__str__() + '-' + today.day.__str__() + ' ' + start_time,
											"%Y-%m-%d %H:%M:%S.%f")
		end_date_time = datetime.datetime.strptime(tomorrow.year.__str__() + '-' + tomorrow.month.__str__() + '-' + tomorrow.day.__str__() + ' ' + next_day_end_time,
										  "%Y-%m-%d %H:%M:%S.%f")

		self.start_date_time = start_date_time
		self.start_date_time_ms = int(
			time.mktime(start_date_time.timetuple()) * 1000.0 + start_date_time.microsecond / 1000)
		self.end_date_time_ms = int(time.mktime(end_date_time.timetuple()) * 1000.0 + end_date_time.microsecond / 1000)

	def local_time(self):
		return int(round(time.time() * 1000))

	def start(self):
		g_logger.info('wait for time:{}'.format(self.start_date_time))
		while True:

			if self.local_time() >= self.start_date_time_ms:
				g_logger.info('run')
				break
			else:
				time.sleep(self.sleep_interval)
