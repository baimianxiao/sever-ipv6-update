# -*- encoding:utf-8 -*-
import os
import re
import socket

import time
import json

from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

import dnspodApi


def start_task():
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}]开始定时任务")
    sched = BlockingScheduler()
    timing_update()
    sched.add_job(timing_update, 'interval', seconds=timeInterval)
    sched.start()


def timing_update():
    local_ipv6 = get_local_ipv6()
    dns_ipv6 = get_dns_ipv6(SubDomain + "." + Domain)
    if local_ipv6 != dns_ipv6:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}]检测到服务器ipv6与DNS记录不同,开始更新解析")
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}]本地ipv6：" + local_ipv6)
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}]DNS记录：" + dns_ipv6)
        dnspodApi.change_dns(SecretId, SecretKey, Domain, SubDomain, RecordType, RecordId, local_ipv6, TTL)
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}]线程休眠等待解析生效")
        time.sleep(TTL + 100)
    else:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}]DNS记录与本地ipv6一致，无需更新解析")


def get_local_ipv6() -> str:
    """获取本地ipv6地址"""
    output = os.popen("ipconfig /all").read()
    result = re.findall(r"(([a-f0-9]{1,4}:){7}[a-f0-9]{1,4})", output, re.I)
    return result[0][0]


def get_dns_ipv6(url) -> str:
    """获取域名解析的ipv6地址"""
    result = socket.getaddrinfo(str(url), None, socket.AF_INET6)[0][4][0]
    return result


def get_json(path):
    """读取json"""
    with open(path, 'r') as file:
        json_data = json.load(file)
    return json_data


def write_json(path, data):
    """写入json"""
    with open(path, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    return True


config = {
    "SecretId": "SecretId",
    "SecretKey": "SecretKey",
    "Domain": "域名",
    "SubDomain": "主机记录",
    "RecordType": "记录类型",
    "TTL": 600,
    "RecordId": 1316792446,
    "timeInterval": 300
}
# 判断配置文件是否存在
if not os.path.exists("config.json"):
    print("配置文件不存在\n已生成配置文件\n请在修改config.json后重新运行该程序")
    write_json("./", config)
else:
    print("配置文件存在")

config = get_json("config.json")

# 获取SecretId和SecretKet
SecretId = config["SecretId"]
SecretKey = config["SecretKey"]

# 获取DNS设置
Domain = config["Domain"]
SubDomain = config["SubDomain"]
RecordType = config["RecordType"]
TTL = config["TTL"]
RecordId = config["RecordId"]
timeInterval = config["timeInterval"]

# 开始定时任务
start_task()
