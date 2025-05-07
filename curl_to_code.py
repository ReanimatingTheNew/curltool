"""
curl命令转换为多种编程语言代码的模块
支持将curl命令转换为Python、JavaScript、Node.js、PHP、Go、Ruby、Java、C#、Rust和Swift
"""

import json
import re
import shlex

# 支持的语言列表
SUPPORTED_LANGUAGES = [
    'python', 'javascript', 'nodejs', 'php', 'go', 
    'ruby', 'java', 'csharp', 'rust', 'swift'
]

def parse_curl_to_dict(curl_command):
    """
    将curl命令解析为统一的字典格式，便于后续转换
    """
    # 初始化结果字典
    result = {
        "method": "GET",
        "url": "",
        "headers": {},
        "data": None,
        "form_data": None,
        "cookies": {},
        "auth": None,
        "timeout": None,
        "allow_redirects": True,
        "verify_ssl": True,
        "proxy": None
    }
    
    # 使用shlex分割命令，保留引号内的内容
    try:
        args = shlex.split(curl_command)
    except ValueError as e:
        return {"error": f"命令解析错误: {str(e)}"}
    
    if args[0].lower() != 'curl':
        return {"error": "不是有效的curl命令"}
    
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
                # 处理认证头
                elif header.lower().startswith('authorization:'):
                    auth_str = header[14:].strip()
                    if auth_str.lower().startswith('basic '):
                        result["auth"] = {"type": "basic", "token": auth_str[6:]}
                    elif auth_str.lower().startswith('bearer '):
                        result["auth"] = {"type": "bearer", "token": auth_str[7:]}
                    else:
                        result["auth"] = {"type": "custom", "value": auth_str}
                    result["headers"]["Authorization"] = auth_str
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
        if arg in ['-F', '--form']:
            if i + 1 < len(args):
                if result["form_data"] is None:
                    result["form_data"] = {}
                form_item = args[i + 1]
                
                # 处理文件上传
                if '@' in form_item and '=' in form_item:
                    key, value = form_item.split('=', 1)
                    if value.startswith('@'):
                        file_path = value[1:]
                        result["form_data"][key] = {"type": "file", "path": file_path}
                    else:
                        result["form_data"][key] = {"type": "text", "value": value}
                elif '=' in form_item:
                    key, value = form_item.split('=', 1)
                    result["form_data"][key] = {"type": "text", "value": value}
                
                i += 2
            else:
                return {"error": f"参数 {arg} 缺少值"}
            continue
            
        # 处理URL编码数据
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
            
        # 处理用户认证
        if arg in ['-u', '--user']:
            if i + 1 < len(args):
                auth_str = args[i + 1]
                if ':' in auth_str:
                    username, password = auth_str.split(':', 1)
                    result["auth"] = {"type": "basic", "username": username, "password": password}
                else:
                    result["auth"] = {"type": "basic", "username": auth_str, "password": ""}
                i += 2
            else:
                return {"error": f"参数 {arg} 缺少值"}
            continue
            
        # 处理超时
        if arg in ['--connect-timeout']:
            if i + 1 < len(args):
                try:
                    result["timeout"] = float(args[i + 1])
                except ValueError:
                    pass
                i += 2
            else:
                return {"error": f"参数 {arg} 缺少值"}
            continue
            
        # 处理重定向
        if arg in ['-L', '--location']:
            result["allow_redirects"] = True
            i += 1
            continue
            
        # 处理SSL验证
        if arg in ['-k', '--insecure']:
            result["verify_ssl"] = False
            i += 1
            continue
            
        # 处理代理
        if arg in ['-x', '--proxy']:
            if i + 1 < len(args):
                result["proxy"] = args[i + 1]
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


def to_python(curl_dict):
    """将curl命令转换为Python代码（使用requests库）"""
    if "error" in curl_dict:
        return f"# Error: {curl_dict['error']}"
    
    code = ["import requests"]
    
    # 处理headers
    if curl_dict["headers"]:
        code.append("\nheaders = {")
        for key, value in curl_dict["headers"].items():
            code.append(f"    '{key}': '{value}',")
        code.append("}")
    
    # 处理data
    if curl_dict["data"] is not None:
        if isinstance(curl_dict["data"], dict):
            code.append("\ndata = {")
            for key, value in curl_dict["data"].items():
                if isinstance(value, str):
                    code.append(f"    '{key}': '{value}',")
                else:
                    code.append(f"    '{key}': {value},")
            code.append("}")
        else:
            # 字符串形式的data
            code.append(f"\ndata = '{curl_dict['data']}'")
    
    # 处理form_data
    if curl_dict["form_data"] is not None:
        code.append("\nfiles = {")
        for key, value in curl_dict["form_data"].items():
            if value["type"] == "file":
                code.append(f"    '{key}': open('{value['path']}', 'rb'),")
            else:
                code.append(f"    '{key}': '{value['value']}',")
        code.append("}")
    
    # 处理cookies
    if "cookies" in curl_dict and curl_dict["cookies"]:
        code.append("\ncookies = {")
        for key, value in curl_dict["cookies"].items():
            code.append(f"    '{key}': '{value}',")
        code.append("}")
    
    # 构建请求参数
    params = []
    
    # URL参数
    params.append(f"'{curl_dict['url']}'")
    
    # 添加headers参数
    if curl_dict["headers"]:
        params.append("headers=headers")
    
    # 添加data或json参数
    if curl_dict["data"] is not None:
        if isinstance(curl_dict["data"], dict) and curl_dict["headers"].get("Content-Type", "").lower() == "application/json":
            params.append("json=data")
        else:
            params.append("data=data")
    
    # 添加files参数
    if curl_dict["form_data"] is not None:
        params.append("files=files")
    
    # 添加cookies参数
    if "cookies" in curl_dict and curl_dict["cookies"]:
        params.append("cookies=cookies")
    
    # 添加auth参数
    if curl_dict["auth"] is not None and curl_dict["auth"]["type"] == "basic":
        if "username" in curl_dict["auth"]:
            params.append(f"auth=('{curl_dict['auth']['username']}', '{curl_dict['auth']['password']}')")
    
    # 添加verify参数
    if not curl_dict["verify_ssl"]:
        params.append("verify=False")
    
    # 添加allow_redirects参数
    if not curl_dict["allow_redirects"]:
        params.append("allow_redirects=False")
    
    # 添加timeout参数
    if curl_dict["timeout"] is not None:
        params.append(f"timeout={curl_dict['timeout']}")
    
    # 添加proxies参数
    if curl_dict["proxy"] is not None:
        params.append(f"proxies={{'http': '{curl_dict['proxy']}', 'https': '{curl_dict['proxy']}'}}")
    
    # 构建请求语句
    method = curl_dict["method"].lower()
    if method == "get":
        code.append(f"\nresponse = requests.get({', '.join(params)})")
    elif method == "post":
        code.append(f"\nresponse = requests.post({', '.join(params)})")
    elif method == "put":
        code.append(f"\nresponse = requests.put({', '.join(params)})")
    elif method == "delete":
        code.append(f"\nresponse = requests.delete({', '.join(params)})")
    elif method == "patch":
        code.append(f"\nresponse = requests.patch({', '.join(params)})")
    elif method == "head":
        code.append(f"\nresponse = requests.head({', '.join(params)})")
    elif method == "options":
        code.append(f"\nresponse = requests.options({', '.join(params)})")
    else:
        code.append(f"\nresponse = requests.request('{method}', {', '.join(params)})")
    
    # 添加响应处理
    code.append("\nprint(response.status_code)")
    code.append("try:")
    code.append("    print(response.json())")
    code.append("except ValueError:")
    code.append("    print(response.text)")
    
    return "\n".join(code)


def to_javascript(curl_dict):
    """将curl命令转换为JavaScript代码（使用fetch API）"""
    if "error" in curl_dict:
        return f"// Error: {curl_dict['error']}"
    
    code = []
    
    # 构建选项对象
    code.append("const options = {")
    code.append(f"  method: '{curl_dict['method']}',")
    
    # 处理headers
    if curl_dict["headers"]:
        code.append("  headers: {")
        for key, value in curl_dict["headers"].items():
            code.append(f"    '{key}': '{value}',")
        code.append("  },")
    
    # 处理body
    if curl_dict["data"] is not None:
        if isinstance(curl_dict["data"], dict):
            if curl_dict["headers"].get("Content-Type", "").lower() == "application/json":
                code.append(f"  body: JSON.stringify({json.dumps(curl_dict['data'])}),")
            else:
                # 构建URLSearchParams
                code.append("  body: new URLSearchParams({")
                for key, value in curl_dict["data"].items():
                    if isinstance(value, str):
                        code.append(f"    '{key}': '{value}',")
                    else:
                        code.append(f"    '{key}': {value},")
                code.append("  }).toString(),")
        else:
            # 字符串形式的data
            code.append(f"  body: '{curl_dict['data']}',")
    
    # 处理form_data
    if curl_dict["form_data"] is not None:
        code.append("  body: (() => {")
        code.append("    const formData = new FormData();")
        for key, value in curl_dict["form_data"].items():
            if value["type"] == "file":
                # 在JavaScript中，我们需要用户选择文件
                code.append(f"    // Note: You need to get the file from an input element")
                code.append(f"    // formData.append('{key}', fileInput.files[0]);")
                code.append(f"    // For now, we're just adding a placeholder")
                code.append(f"    formData.append('{key}', new Blob(['placeholder']), '{value['path'].split('/')[-1]}');")
            else:
                code.append(f"    formData.append('{key}', '{value['value']}');")
        code.append("    return formData;")
        code.append("  })(),")
    
    # 处理credentials（包含cookies）
    if "cookies" in curl_dict and curl_dict["cookies"] or curl_dict["auth"] is not None:
        code.append("  credentials: 'include',")
    
    # 处理redirect
    if not curl_dict["allow_redirects"]:
        code.append("  redirect: 'manual',")
    
    code.append("};")
    
    # 构建fetch调用
    code.append(f"\nfetch('{curl_dict['url']}', options)")
    code.append("  .then(response => {")
    code.append("    console.log('Status:', response.status);")
    code.append("    return response.text().then(text => {")
    code.append("      try {")
    code.append("        return JSON.parse(text);")
    code.append("      } catch (e) {")
    code.append("        return text;")
    code.append("      }")
    code.append("    });")
    code.append("  })")
    code.append("  .then(data => {")
    code.append("    console.log('Response:', data);")
    code.append("  })")
    code.append("  .catch(error => {")
    code.append("    console.error('Error:', error);")
    code.append("  });")
    
    return "\n".join(code)


def to_nodejs(curl_dict):
    """将curl命令转换为Node.js代码（使用http/https模块）"""
    if "error" in curl_dict:
        return f"// Error: {curl_dict['error']}"
    
    code = []
    
    # 判断URL协议
    if curl_dict["url"].startswith("https"):
        code.append("const https = require('https');")
        module = "https"
    else:
        code.append("const http = require('http');")
        module = "http"
    
    code.append("const url = require('url');")
    code.append("const fs = require('fs');")
    
    # 处理URL
    code.append(f"\nconst parsedUrl = new URL('{curl_dict['url']}');")
    
    # 处理选项
    code.append("\nconst options = {")
    code.append("  hostname: parsedUrl.hostname,")
    code.append("  port: parsedUrl.port || (parsedUrl.protocol === 'https:' ? 443 : 80),")
    code.append("  path: parsedUrl.pathname + parsedUrl.search,")
    code.append(f"  method: '{curl_dict['method']}',")
    
    # 处理headers
    if curl_dict["headers"]:
        code.append("  headers: {")
        for key, value in curl_dict["headers"].items():
            code.append(f"    '{key}': '{value}',")
        code.append("  },")
    
    # 处理认证
    if curl_dict["auth"] is not None and curl_dict["auth"]["type"] == "basic" and "username" in curl_dict["auth"]:
        code.append(f"  auth: '{curl_dict['auth']['username']}:{curl_dict['auth']['password']}',")
    
    # 处理重定向
    if not curl_dict["allow_redirects"]:
        code.append("  followRedirect: false,")
    
    # 处理SSL验证
    if not curl_dict["verify_ssl"]:
        code.append("  rejectUnauthorized: false,")
    
    # 处理超时
    if curl_dict["timeout"] is not None:
        code.append(f"  timeout: {int(curl_dict['timeout'] * 1000)},")
    
    code.append("};")
    
    # 构建请求
    code.append("\nconst req = " + module + ".request(options, (res) => {")
    code.append("  console.log(`Status Code: ${res.statusCode}`);")
    code.append("  console.log(`Headers: ${JSON.stringify(res.headers)}`);")
    code.append("  ")
    code.append("  let data = '';")
    code.append("  ")
    code.append("  res.on('data', (chunk) => {")
    code.append("    data += chunk;")
    code.append("  });")
    code.append("  ")
    code.append("  res.on('end', () => {")
    code.append("    try {")
    code.append("      const jsonData = JSON.parse(data);")
    code.append("      console.log(jsonData);")
    code.append("    } catch (e) {")
    code.append("      console.log(data);")
    code.append("    }")
    code.append("  });")
    code.append("});")
    
    code.append("\nreq.on('error', (error) => {")
    code.append("  console.error(`Error: ${error.message}`);")
    code.append("});")
    
    # 处理请求体
    if curl_dict["data"] is not None:
        if isinstance(curl_dict["data"], dict):
            if curl_dict["headers"].get("Content-Type", "").lower() == "application/json":
                code.append(f"\nconst postData = JSON.stringify({json.dumps(curl_dict['data'])});")
            else:
                # 构建查询字符串
                parts = []
                for key, value in curl_dict["data"].items():
                    parts.append(f"{key}={value}")
                code.append(f"\nconst postData = '{"&".join(parts)}';")
        else:
            # 字符串形式的data
            code.append(f"\nconst postData = '{curl_dict['data']}';")
        code.append("\nreq.write(postData);")
    
    # 处理form_data
    if curl_dict["form_data"] is not None:
        code.append("\n// Note: For multipart/form-data, you may want to use a library like 'form-data'")
        code.append("// npm install form-data")
        code.append("// const FormData = require('form-data');")
        code.append("// const form = new FormData();")
        for key, value in curl_dict["form_data"].items():
            if value["type"] == "file":
                code.append(f"// form.append('{key}', fs.createReadStream('{value['path']}'));")
            else:
                code.append(f"// form.append('{key}', '{value['value']}');")
        code.append("// form.pipe(req);")
        code.append("// Instead, we're using a simplified approach here:")
        code.append("const boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW';")
        code.append("let formBody = '';")
        for key, value in curl_dict["form_data"].items():
            code.append(f"formBody += `--${{boundary}}\r\n`;")
            if value["type"] == "file":
                code.append(f"formBody += `Content-Disposition: form-data; name=\"{key}\"; filename=\"{value['path'].split('/')[-1]}\"\r\n`;")
                code.append(f"formBody += `Content-Type: application/octet-stream\r\n\r\n`;")
                code.append(f"// Note: In a real implementation, you would read the file content here")
                code.append(f"formBody += `[File content of {value['path']} would be here]\r\n`;")
            else:
                code.append(f"formBody += `Content-Disposition: form-data; name=\"{key}\"\r\n\r\n`;")
                code.append(f"formBody += `{value['value']}\r\n`;")
        code.append(f"formBody += `--${{boundary}}--\r\n`;")
        code.append("req.setHeader('Content-Type', `multipart/form-data; boundary=${boundary}`);")
        code.append("req.write(formBody);")
    
    code.append("\nreq.end();")
    
    return "\n".join(code)


def to_php(curl_dict):
    """将curl命令转换为PHP代码（使用curl扩展）"""
    if "error" in curl_dict:
        return f"// Error: {curl_dict['error']}"
    
    code = ["<?php"]
    
    # 初始化curl
    code.append("\n// Initialize cURL session")
    code.append("$ch = curl_init();")
    
    # 设置URL
    code.append(f"\n// Set URL\ncurl_setopt($ch, CURLOPT_URL, '{curl_dict['url']}');")
    
    # 设置返回结果而非输出
    code.append("\n// Return the response instead of outputting it")
    code.append("curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);")
    
    # 设置请求方法
    if curl_dict["method"] != "GET":
        code.append(f"\n// Set request method\ncurl_setopt($ch, CURLOPT_CUSTOMREQUEST, '{curl_dict['method']}');")
    
    # 如果是POST请求，设置POST标志
    if curl_dict["method"] == "POST":
        code.append("\n// Set POST flag")
        code.append("curl_setopt($ch, CURLOPT_POST, true);")
    
    # 设置headers
    if curl_dict["headers"]:
        code.append("\n// Set request headers")
        code.append("$headers = array(")
        for key, value in curl_dict["headers"].items():
            code.append(f"    '{key}: {value}',")
        code.append(");")
        code.append("curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);")
    
    # 设置请求体
    if curl_dict["data"] is not None:
        code.append("\n// Set request body")
        if isinstance(curl_dict["data"], dict):
            if curl_dict["headers"].get("Content-Type", "").lower() == "application/json":
                code.append(f"$data = json_encode({php_array_from_dict(curl_dict['data'])});")
            else:
                # 使用http_build_query
                code.append(f"$data = http_build_query({php_array_from_dict(curl_dict['data'])});")
        else:
            # 字符串形式的data
            code.append(f"$data = '{curl_dict['data']}';")
        code.append("curl_setopt($ch, CURLOPT_POSTFIELDS, $data);")
    
    # 设置表单数据
    if curl_dict["form_data"] is not None:
        code.append("\n// Set form data")
        code.append("$postfields = array(")
        for key, value in curl_dict["form_data"].items():
            if value["type"] == "file":
                code.append(f"    '{key}' => new CURLFile('{value['path']}'),")
            else:
                code.append(f"    '{key}' => '{value['value']}',")
        code.append(");")
        code.append("curl_setopt($ch, CURLOPT_POSTFIELDS, $postfields);")
    
    # 设置cookies
    if "cookies" in curl_dict and curl_dict["cookies"]:
        code.append("\n// Set cookies")
        cookie_parts = []
        for key, value in curl_dict["cookies"].items():
            cookie_parts.append(f"{key}={value}")
        code.append(f"curl_setopt($ch, CURLOPT_COOKIE, '{'; '.join(cookie_parts)}');")
    
    # 设置认证
    if curl_dict["auth"] is not None and curl_dict["auth"]["type"] == "basic" and "username" in curl_dict["auth"]:
        code.append("\n// Set basic authentication")
        code.append(f"curl_setopt($ch, CURLOPT_USERPWD, '{curl_dict['auth']['username']}:{curl_dict['auth']['password']}');")
    
    # 设置重定向
    if not curl_dict["allow_redirects"]:
        code.append("\n// Disable following redirects")
        code.append("curl_setopt($ch, CURLOPT_FOLLOWLOCATION, false);")
    else:
        code.append("\n// Enable following redirects")
        code.append("curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);")
    
    # 设置SSL验证
    if not curl_dict["verify_ssl"]:
        code.append("\n// Disable SSL verification")
        code.append("curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);")
        code.append("curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);")
    
    # 设置超时
    if curl_dict["timeout"] is not None:
        code.append("\n// Set timeout")
        code.append(f"curl_setopt($ch, CURLOPT_TIMEOUT, {int(curl_dict['timeout'])});")
    
    # 设置代理
    if curl_dict["proxy"] is not None:
        code.append("\n// Set proxy")
        code.append(f"curl_setopt($ch, CURLOPT_PROXY, '{curl_dict['proxy']}');")
    
    # 执行请求
    code.append("\n// Execute the request")
    code.append("$response = curl_exec($ch);")
    code.append("$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);")
    
    # 检查错误
    code.append("\n// Check for errors")
    code.append("if (curl_errno($ch)) {")
    code.append("    echo 'Error: ' . curl_error($ch);")
    code.append("}")
    
    # 输出响应
    code.append("\n// Output the response")
    code.append("echo \"HTTP Status Code: $httpCode\n\";")
    code.append("echo \"Response:\n\";")
    code.append("echo $response;")
    
    # 关闭curl会话
    code.append("\n// Close cURL session")
    code.append("curl_close($ch);")
    
    code.append("\n?>")
    
    return "\n".join(code)


def php_array_from_dict(d):
    """将Python字典转换为PHP数组语法"""
    if not isinstance(d, dict):
        return f"'{d}'"
    
    parts = []
    for key, value in d.items():
        if isinstance(value, dict):
            parts.append(f"'{key}' => {php_array_from_dict(value)}")
        elif isinstance(value, (list, tuple)):
            items = [php_array_from_dict(item) for item in value]
            parts.append(f"'{key}' => array({', '.join(items)})")
        elif isinstance(value, bool):
            parts.append(f"'{key}' => {str(value).lower()}")
        elif isinstance(value, (int, float)):
            parts.append(f"'{key}' => {value}")
        else:
            parts.append(f"'{key}' => '{value}'")
    
    return f"array({', '.join(parts)})"
