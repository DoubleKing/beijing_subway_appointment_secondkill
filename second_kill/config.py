# encoding=utf8
import os
import json


class Config(object):
	def __init__(self, config_file='config.json'):
		self._path = os.path.join(os.getcwd(), config_file)
		if not os.path.exists(self._path):
			raise ("No such file: config.json")
		f = open(self._path)
		config_data = json.load(f)
		f.close()
		self.start_time = config_data["start_time"]
		self.next_day_end_time = config_data["next_day_end_time"]
		self.authorization = config_data["authorization"]
		self.timeSlot = config_data["timeSlot"]
		self.lineName = config_data["lineName"]
		self.stationName = config_data["stationName"]


global_config = Config()
