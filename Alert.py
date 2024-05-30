'''
Author: llody 745719408@qq.com
Date: 2024-05-29 16:48:58
LastEditors: llody 745719408@qq.com
LastEditTime: 2024-05-30 11:08:17
FilePath: \K8S\组件包\云原生监控\prometheus-llody\docker部署\Alert.py
Description: 微信机器人告警脚本
'''
# -*- coding: UTF-8 -*-
import requests
import json
import datetime

def parse_time(date_string):
    if '.' in date_string:
        date_string = date_string.split('.')[0]
    if 'Z' in date_string:
        date_string = date_string.replace('Z', '')
    date_obj = datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")
    local_time = date_obj + datetime.timedelta(hours=8)
    return local_time.strftime("%Y-%m-%d %H:%M:%S.%f")

def format_message(alert_info):
    content = "## <font color=\"{color}\">{title}: {status}</font>\n"\
              "**告警项目:** <font color=\"warning\">{region}</font>\n"\
              "**告警名称:** <font color=\"warning\">{alertnames}</font>\n"\
              "**告警级别:** {levels}\n"\
              "**告警时间:** {start_time}\n".format(
                  color="red" if alert_info['status'] == 'firing' else "info",
                  title="告警通知" if alert_info['status'] == 'firing' else "恢复通知",
                  status=alert_info['status'],
                  region=alert_info['region'],
                  alertnames=alert_info['alertnames'],
                  levels=alert_info['levels'],
                  start_time=alert_info['start_time']
              )
    
    # 如果是K8S环境的告警，使用名称空间
    if alert_info['is_k8s']:
        content += "**名称空间:** {namespace}\n".format(namespace=alert_info['namespace'])
    else:
        content += "**故障实例:** {instance}\n".format(instance=alert_info['instance'])
    
    if alert_info['status'] == 'resolved':
        content += "**恢复时间:** <font color=\"green\">{end_time}</font>\n".format(end_time=alert_info['end_time'])
    
    content += "**告警详情:** <font color=\"comment\">{description}</font>".format(description=alert_info['description'])
    
    params = json.dumps({
        "msgtype": "markdown",
        "markdown": {
            "content": content
        }
    })
    
    return params

def webhook_url(params, url_key):
    url = url_key
    headers = {"Content-type": "application/json"}
    requests.post(url, data=params, headers=headers)

def send_alert(json_re, url_key):
    for i in json_re['alerts']:
        print("消息体:", i)
        is_k8s = 'namespace' in i['labels']
        alert_info = {
            'status': i['status'],
            'region': i['labels'].get('project', 'Unknown'),
            'alertnames': i['labels'].get('alertname', 'Unknown'),
            'levels': i['labels'].get('severity', 'Unknown'),
            'start_time': parse_time(i['startsAt']),
            'end_time': parse_time(i['endsAt']) if i['status'] == 'resolved' else '',
            'instance': i['labels'].get('instance', 'Unknown'),
            'namespace': i['labels'].get('namespace', 'Unknown'),
            'description': i['annotations'].get('description', i['annotations'].get('message', 'Service is wrong')),
            'is_k8s': is_k8s
        }
        message = format_message(alert_info)
        webhook_url(message, url_key)
