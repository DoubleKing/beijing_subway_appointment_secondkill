# beijing_subway_appointment_secondkill
北京地铁预约辅助程序



## 主要功能

进行背景地铁预约进站码的刷票



## 依赖库

 需要使用到的库已经放在requirements.txt，使用pip安装的可以使用指令
`pip install -r requirements.txt` 



## 使用教程

### 第一步获取认证

使用chrome或者火狐 按F12   登陆https://webui.mybti.cn/#/login 

登陆之后获取http请求头authorization字段值

### 第二步配置

把第二步中获取的authorization配置到config.json中，并且配置抢预约的时间和地铁站

`{
  "start_time": "11:59:59.500",
  "next_day_end_time": "07:20:00.000",
  "authorization": [
    "ABCDYzM0MGEtODQzOC00NjlkLTljODMtZWZlZTZhZTYwMTRmLDE2MTE1MjYxNzk1NDMsZ0k5SktCM2Q0Q0dRb1lWZzdGWVZ1WHpnakNRPQ==",
    "EFGHZDBhMTEtMmM2MC00OGI2LTg3MGMtNjE3N2Q0NjlhNjIxLDE2MTA5NzE3MDUwOTIsTXFIeHlKb2JMRFovSTcrQnpPNFRkdXhzSTc4PQ=="
  ],
  "timeSlot": "0740-0810",
  "lineName": "昌平线",
  "stationName": "沙河站"
}`



### 第三步运行

`python main.py`



## 注意事项

authorization大概一周就会过期，注意一周后重新更换新的authorization