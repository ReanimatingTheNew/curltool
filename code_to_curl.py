"""
代码到curl命令转换模块
支持从Python、JavaScript和PHP代码转换为curl命令
"""

import re
import json

def python_to_curl(code):
    """
    将Python代码（主要是requests库）转换为curl命令
    """
    result = {
        "command": "curl",
        "success": True,
        "message": ""
    }
    
    # 尝试提取URL
    url_match = re.search(r'requests\.(get|post|put|delete|patch)\s*\(\s*[\'"]([^\'"]+)[\'"]', code)
    if not url_match:
        url_match = re.search(r'url\s*=\s*[\'"]([^\'"]+)[\'"]', code)
        if not url_match:
            result["success"] = False
            result["message"] = "无法识别URL"
            return result
        url = url_match.group(1)
        # 尝试从其他地方找方法
        method_match = re.search(r'method\s*=\s*[\'"]([^\'"]+)[\'"]', code)
        method = method_match.group(1).upper() if method_match else "GET"
    else:
        method = url_match.group(1).upper()
        url = url_match.group(2)
    
    # 构建基本curl命令
    curl_cmd = f"curl -X {method} '{url}'"
    
    # 提取headers
    headers_match = re.search(r'headers\s*=\s*({[^}]+})', code)
    if headers_match:
        try:
            # 尝试直接解析JSON
            headers_str = headers_match.group(1).replace("'", '"')
            # 处理可能的Python字典格式
            headers_str = re.sub(r'(\w+):', r'"\1":', headers_str)
            headers = json.loads(headers_str)
            for key, value in headers.items():
                curl_cmd += f" -H '{key}: {value}'"
        except:
            # 如果JSON解析失败，使用正则表达式
            headers_content = headers_match.group(1)
            header_matches = re.finditer(r'[\'"]([^\'"]+)[\'"]\s*:\s*[\'"]([^\'"]+)[\'"]', headers_content)
            for match in header_matches:
                key, value = match.group(1), match.group(2)
                curl_cmd += f" -H '{key}: {value}'"
    
    # 提取data或json
    data_match = re.search(r'data\s*=\s*({[^}]+}|[\'"][^\'"]+[\'"])', code)
    json_match = re.search(r'json\s*=\s*({[^}]+})', code)
    
    if json_match:
        try:
            # 尝试解析JSON
            json_str = json_match.group(1).replace("'", '"')
            json_str = re.sub(r'(\w+):', r'"\1":', json_str)
            json_data = json.loads(json_str)
            curl_cmd += f" -H 'Content-Type: application/json' -d '{json.dumps(json_data)}'"
        except:
            # 如果解析失败，直接使用原始字符串
            json_str = json_match.group(1).replace("'", '"')
            curl_cmd += f" -H 'Content-Type: application/json' -d '{json_str}'"
    elif data_match:
        data_str = data_match.group(1)
        if data_str.startswith('{'):
            # 可能是JSON
            curl_cmd += f" -d '{data_str}'"
        else:
            # 可能是表单数据或字符串
            curl_cmd += f" -d {data_str}"
    
    result["command"] = curl_cmd
    return result

def javascript_to_curl(code):
    """
    将JavaScript代码（主要是fetch或axios）转换为curl命令
    """
    result = {
        "command": "curl",
        "success": True,
        "message": ""
    }
    
    # 检查是fetch还是axios
    is_fetch = 'fetch' in code
    is_axios = 'axios' in code
    
    if is_fetch:
        # 提取URL
        url_match = re.search(r'fetch\s*\(\s*[\'"]([^\'"]+)[\'"]', code)
        if not url_match:
            result["success"] = False
            result["message"] = "无法识别fetch的URL"
            return result
        
        url = url_match.group(1)
        
        # 提取方法
        method_match = re.search(r'method\s*:\s*[\'"]([^\'"]+)[\'"]', code)
        method = method_match.group(1).upper() if method_match else "GET"
        
        # 构建基本curl命令
        curl_cmd = f"curl -X {method} '{url}'"
        
        # 提取headers
        headers_match = re.search(r'headers\s*:\s*({[^}]+})', code)
        if headers_match:
            try:
                # 尝试直接解析JSON
                headers_str = headers_match.group(1).replace("'", '"')
                headers = json.loads(headers_str)
                for key, value in headers.items():
                    curl_cmd += f" -H '{key}: {value}'"
            except:
                # 如果JSON解析失败，使用正则表达式
                headers_content = headers_match.group(1)
                header_matches = re.finditer(r'[\'"]([^\'"]+)[\'"]\s*:\s*[\'"]([^\'"]+)[\'"]', headers_content)
                for match in header_matches:
                    key, value = match.group(1), match.group(2)
                    curl_cmd += f" -H '{key}: {value}'"
        
        # 提取body
        body_match = re.search(r'body\s*:\s*([^,}]+)', code)
        if body_match:
            body_content = body_match.group(1).strip()
            if body_content.startswith('JSON.stringify'):
                # 处理JSON.stringify
                json_match = re.search(r'JSON\.stringify\s*\(\s*({[^}]+})\s*\)', body_content)
                if json_match:
                    json_str = json_match.group(1).replace("'", '"')
                    curl_cmd += f" -d '{json_str}'"
            else:
                # 其他类型的body
                curl_cmd += f" -d '{body_content}'"
    
    elif is_axios:
        # 提取URL
        url_match = re.search(r'axios\s*\.\s*(get|post|put|delete|patch)\s*\(\s*[\'"]([^\'"]+)[\'"]', code)
        if not url_match:
            url_match = re.search(r'url\s*:\s*[\'"]([^\'"]+)[\'"]', code)
            if not url_match:
                result["success"] = False
                result["message"] = "无法识别axios的URL"
                return result
            url = url_match.group(1)
            # 尝试从其他地方找方法
            method_match = re.search(r'method\s*:\s*[\'"]([^\'"]+)[\'"]', code)
            method = method_match.group(1).upper() if method_match else "GET"
        else:
            method = url_match.group(1).upper()
            url = url_match.group(2)
        
        # 构建基本curl命令
        curl_cmd = f"curl -X {method} '{url}'"
        
        # 提取headers
        headers_match = re.search(r'headers\s*:\s*({[^}]+})', code)
        if headers_match:
            try:
                # 尝试直接解析JSON
                headers_str = headers_match.group(1).replace("'", '"')
                headers = json.loads(headers_str)
                for key, value in headers.items():
                    curl_cmd += f" -H '{key}: {value}'"
            except:
                # 如果JSON解析失败，使用正则表达式
                headers_content = headers_match.group(1)
                header_matches = re.finditer(r'[\'"]([^\'"]+)[\'"]\s*:\s*[\'"]([^\'"]+)[\'"]', headers_content)
                for match in header_matches:
                    key, value = match.group(1), match.group(2)
                    curl_cmd += f" -H '{key}: {value}'"
        
        # 提取data
        data_match = re.search(r'data\s*:\s*({[^}]+})', code)
        if data_match:
            data_str = data_match.group(1).replace("'", '"')
            curl_cmd += f" -d '{data_str}'"
    
    else:
        result["success"] = False
        result["message"] = "不支持的JavaScript代码格式，目前仅支持fetch和axios"
        return result
    
    result["command"] = curl_cmd
    return result

def php_to_curl(code):
    """
    将PHP代码（主要是curl函数）转换为curl命令
    """
    result = {
        "command": "curl",
        "success": True,
        "message": ""
    }
    
    # 提取URL
    url_match = re.search(r'curl_setopt\s*\(\s*\$ch\s*,\s*CURLOPT_URL\s*,\s*[\'"]([^\'"]+)[\'"]', code)
    if not url_match:
        result["success"] = False
        result["message"] = "无法识别PHP curl的URL"
        return result
    
    url = url_match.group(1)
    
    # 提取方法
    method_match = re.search(r'curl_setopt\s*\(\s*\$ch\s*,\s*CURLOPT_CUSTOMREQUEST\s*,\s*[\'"]([^\'"]+)[\'"]', code)
    method = method_match.group(1) if method_match else "GET"
    
    # 检查是否是POST
    is_post = re.search(r'curl_setopt\s*\(\s*\$ch\s*,\s*CURLOPT_POST\s*,\s*true', code)
    if is_post:
        method = "POST"
    
    # 构建基本curl命令
    curl_cmd = f"curl -X {method} '{url}'"
    
    # 提取headers
    headers_match = re.search(r'curl_setopt\s*\(\s*\$ch\s*,\s*CURLOPT_HTTPHEADER\s*,\s*array\s*\(([^\)]+)\)', code)
    if headers_match:
        headers_content = headers_match.group(1)
        header_matches = re.finditer(r'[\'"]([^\'"]+)[\'"]', headers_content)
        for match in header_matches:
            header = match.group(1)
            if ': ' in header:
                curl_cmd += f" -H '{header}'"
    
    # 提取POST数据
    post_data_match = re.search(r'curl_setopt\s*\(\s*\$ch\s*,\s*CURLOPT_POSTFIELDS\s*,\s*[\'"]([^\'"]+)[\'"]', code)
    if post_data_match:
        post_data = post_data_match.group(1)
        curl_cmd += f" -d '{post_data}'"
    
    # 提取JSON数据
    json_data_match = re.search(r'curl_setopt\s*\(\s*\$ch\s*,\s*CURLOPT_POSTFIELDS\s*,\s*json_encode\s*\(([^\)]+)\)', code)
    if json_data_match:
        json_data = json_data_match.group(1)
        curl_cmd += f" -d '{json_data}'"
    
    result["command"] = curl_cmd
    return result

def code_to_curl(code, language):
    """
    根据代码语言选择合适的转换函数
    """
    if language.lower() == 'python':
        return python_to_curl(code)
    elif language.lower() in ['javascript', 'js']:
        return javascript_to_curl(code)
    elif language.lower() == 'php':
        return php_to_curl(code)
    else:
        return {
            "command": "",
            "success": False,
            "message": f"不支持的语言: {language}，目前仅支持Python、JavaScript和PHP"
        }
