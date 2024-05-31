'''
Author: llody 745719408@qq.com
Date: 2024-05-29 16:54:49
LastEditors: llody 745719408@qq.com
LastEditTime: 2024-05-30 10:40:38
FilePath: weixin_robot\main.py
Description: 
'''

import os
import sys
import json
import Alert
import argparse
from flask import Flask, request
from flask_json import FlaskJSON, as_json
from gevent import pywsgi


app = Flask(__name__)
FlaskJSON(app)

@app.route('/alertinfo', methods=['POST'])
@as_json
def alert_data():
    data = request.get_data()
    json_re = json.loads(data)  # 解析接收到的数据为JSON
    Alert.send_alert(json_re, args.key)
    return json_re

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run the alert notification service.")
    parser.add_argument("-p", "--port", type=int, default=os.getenv('PORT', 5000), help="The service port")
    parser.add_argument("-k", "--key", type=str, default=os.getenv('KEY', 'default_key'), help="The webhook url key")
    args = parser.parse_args()

    if not args.port or not args.key:
        parser.print_help()
        sys.exit(1)
    
    print("Weixin robot 启动成功，正在监听端口：{}".format(args.port))
        
    server = pywsgi.WSGIServer(('0.0.0.0', args.port), app)
    server.serve_forever()