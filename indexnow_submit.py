#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import os

def submit_to_indexnow():
    """
    向IndexNow API提交网站URL，以便搜索引擎更快地索引网站内容
    """
    # API端点
    api_url = "https://api.indexnow.org/IndexNow"
    
    # 您的网站和密钥信息
    host = "curl-to.com"
    key = "2a31de34a07f42dba5238b80bbd504de"
    key_location = f"https://{host}/{key}.txt"
    
    # 需要提交的URL列表（请替换为您实际需要提交的URL）
    url_list = [
        f"https://{host}/",
        f"https://{host}/api-docs",
        f"https://{host}/examples"
    ]
    
    # 构建请求数据
    payload = {
        "host": host,
        "key": key,
        "keyLocation": key_location,
        "urlList": url_list
    }
    
    # 设置请求头
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    
    # 先检查密钥文件是否可访问（这很重要）
    print(f"检查密钥文件是否可访问: {key_location}")
    try:
        key_check = requests.head(key_location, timeout=10)
        print(f"密钥文件检查状态码: {key_check.status_code}")
        if key_check.status_code != 200:
            print(f"警告: 密钥文件无法访问，IndexNow将无法验证您是网站所有者")
            print(f"请确保文件 {key}.txt 已上传到您网站的根目录")
    except Exception as e:
        print(f"警告: 无法检查密钥文件: {str(e)}")
    
    try:
        # 发送POST请求
        print("正在提交以下URL到IndexNow:")
        for url in url_list:
            print(f"  - {url}")
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))
        
        # 打印响应结果
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        # 检查响应状态 - 注意：202也是正常的响应
        if response.status_code in [200, 202]:
            if response.status_code == 200:
                print("成功! 您的URL已提交到IndexNow API并被接受")
            else:  # 202状态码
                print("请求已被接受处理! 状态码202是正常的响应")
                print("IndexNow API已接收您的提交，但尚未完成处理")
                print("请确保密钥文件可以通过上述URL访问，以便完成验证")
        else:
            print(f"提交失败，HTTP状态码: {response.status_code}")
            if response.text:
                print(f"错误信息: {response.text}")
            else:
                print("没有返回详细的错误信息")
            
    except requests.exceptions.Timeout:
        print("请求超时，服务器可能响应慢或不可用")
    except requests.exceptions.ConnectionError:
        print("连接错误，无法连接到IndexNow API服务器")
    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    submit_to_indexnow()
