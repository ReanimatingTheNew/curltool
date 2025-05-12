import curler
import json
import re
import urllib.parse

def parse_curl(curl_command):
    """将curl命令解析为JSON格式，使用curler库"""
    # 输出调试信息
    print(f"解析curl命令: {curl_command}")
    
    # 验证输入
    curl_command = curl_command.strip()
    if not curl_command:
        return {"error": "请提供curl命令"}
    
    # 确保命令以curl开头
    if not curl_command.lower().startswith('curl '):
        if curl_command.lower() == 'curl':
            return {"error": "curl命令缺少URL参数"}
        else:
            # 尝试添加curl前缀
            if not re.match(r'^[\'\"]*curl\s', curl_command.lower()):
                curl_command = 'curl ' + curl_command
                print(f"添加curl前缀后的命令: {curl_command}")
    
    try:
        # 使用curler库解析curl命令
        parsed_curl = curler.parse_curl(curl_command)
        print(f"curler解析结果: {parsed_curl}")
        
        # 构建标准的返回格式
        result = {
            "method": parsed_curl.method,
            "url": parsed_curl.url,
            "headers": parsed_curl.headers,
            "data": None,
        }
        
        # 处理请求数据
        if parsed_curl.data:
            # 尝试解析为JSON
            try:
                # 如果数据是JSON字符串
                if isinstance(parsed_curl.data, str) and parsed_curl.data.strip().startswith('{'):
                    result["data"] = json.loads(parsed_curl.data)
                else:
                    result["data"] = parsed_curl.data
            except json.JSONDecodeError:
                # 如果不是JSON，尝试解析为表单数据
                try:
                    form_data = {}
                    for param in parsed_curl.data.split('&'):
                        if '=' in param:
                            key, value = param.split('=', 1)
                            form_data[key] = urllib.parse.unquote_plus(value)
                    if form_data:
                        result["data"] = form_data
                    else:
                        result["data"] = parsed_curl.data
                except Exception:
                    result["data"] = parsed_curl.data
        elif parsed_curl.data_binary:
            result["data"] = parsed_curl.data_binary
            
        # 处理Cookie
        if parsed_curl.cookies:
            result["cookies"] = parsed_curl.cookies
        
        # 处理verify_ssl参数
        result["verify_ssl"] = not parsed_curl.insecure
        
        return result
    except Exception as e:
        print(f"解析curl命令时出错: {str(e)}")
        # 如果curler解析失败，尝试使用原始方法解析
        return parse_curl_original(curl_command)

# 原始解析方法，作为备用
def parse_curl_original(curl_command):
    """(备用)将curl命令解析为JSON格式的原始方法"""
    print(f"使用原始方法解析curl命令: {curl_command}")
    result = {
        "method": "GET",
        "url": "",
        "headers": {},
        "data": None,
        "cookies": {}
    }
    
    # 使用shlex分割命令，保留引号内的内容
    try:
        # 处理空格问题
        curl_command = curl_command.strip()
        args = shlex.split(curl_command)
    except ValueError as e:
        return {"error": f"命令解析错误: {str(e)}"}
    
    if len(args) == 0 or args[0].lower() != 'curl':
        return {"error": "不是有效的curl命令"}
        
    # 如果只有curl命令没有其他参数，返回错误
    if len(args) == 1:
        return {"error": "curl命令缺少URL参数"}
    
    i = 1
    while i < len(args):
        arg = args[i]
        
        # 处理URL（没有前缀的参数被视为URL）
        if not arg.startswith('-'):
            result["url"] = arg
            i += 1
            continue
            
        # 处理请求方法
        if arg in ['-X', '--request']:
            if i + 1 < len(args):
                result["method"] = args[i + 1]
                i += 2
            else:
                return {"error": f"参数 {arg} 缺少值"}
            continue
            
        # 处理请求头
        if arg in ['-H', '--header']:
            if i + 1 < len(args):
                header = args[i + 1]
                # 处理cookie头
                if header.lower().startswith('cookie:'):
                    cookie_str = header[7:].strip()
                    cookies = {}
                    for cookie in cookie_str.split(';'):
                        if '=' in cookie:
                            key, value = cookie.split('=', 1)
                            cookies[key.strip()] = value.strip()
                    result["cookies"].update(cookies)
                else:
                    # 处理普通头
                    if ':' in header:
                        key, value = header.split(':', 1)
                        result["headers"][key.strip()] = value.strip()
                i += 2
            else:
                return {"error": f"参数 {arg} 缺少值"}
            continue
            
        # 处理数据
        if arg in ['-d', '--data', '--data-ascii', '--data-binary', '--data-raw']:
            if i + 1 < len(args):
                data = args[i + 1]
                # 尝试解析为JSON
                try:
                    result["data"] = json.loads(data)
                except json.JSONDecodeError:
                    # 如果不是JSON，保留原始字符串
                    result["data"] = data
                i += 2
            else:
                return {"error": f"参数 {arg} 缺少值"}
            continue
            
        # 处理表单数据
        if arg in ['--data-urlencode']:
            if i + 1 < len(args):
                if result["data"] is None:
                    result["data"] = {}
                data = args[i + 1]
                if '=' in data:
                    key, value = data.split('=', 1)
                    if isinstance(result["data"], dict):
                        result["data"][key] = value
                    else:
                        # 如果之前的数据不是字典，转换为字典
                        result["data"] = {key: value}
                i += 2
            else:
                return {"error": f"参数 {arg} 缺少值"}
            continue
            
        # 处理cookie
        if arg in ['-b', '--cookie']:
            if i + 1 < len(args):
                cookie_str = args[i + 1]
                for cookie in cookie_str.split(';'):
                    if '=' in cookie:
                        key, value = cookie.split('=', 1)
                        result["cookies"][key.strip()] = value.strip()
                i += 2
            else:
                return {"error": f"参数 {arg} 缺少值"}
            continue
            
        # 跳过其他选项
        if arg.startswith('-') and i + 1 < len(args) and not args[i + 1].startswith('-'):
            i += 2
        else:
            i += 1
    
    # 如果没有找到cookies，删除空的cookies字典
    if not result["cookies"]:
        del result["cookies"]
        
    return result
