"""
curl命令转换为多种编程语言代码的模块
支持将curl命令转换为Python、JavaScript、Node.js、PHP、Go、Ruby、Java、C#、Rust和Swift
"""

import json
import re
import curler

# 支持的语言列表
SUPPORTED_LANGUAGES = [
    'python', 'javascript', 'nodejs', 'php', 'go',
    'ruby', 'java', 'csharp', 'rust', 'swift'
]

def parse_curl_to_dict(curl_command):
    """
    将curl命令解析为统一的字典格式，便于后续转换
    使用curler库来解析curl命令
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
    
    # 验证输入
    if not curl_command or not curl_command.strip():
        return {"error": "请提供curl命令"}
        
    # 确保命令以curl开头
    curl_command = curl_command.strip()
    if not curl_command.lower().startswith('curl '):
        if curl_command.lower() == 'curl':
            return {"error": "curl命令缺少URL参数"}
        else:
            # 尝试添加curl前缀
            if not re.match(r'^[\'\"]*curl\s', curl_command.lower()):
                curl_command = 'curl ' + curl_command
    
    try:
        # 使用curler库解析curl命令
        parsed_curl = curler.parse_curl(curl_command)
        
        # 填充结果字典
        result["method"] = parsed_curl.method
        result["url"] = parsed_curl.url
        result["headers"] = parsed_curl.headers
        result["verify_ssl"] = not parsed_curl.insecure
        
        # 处理数据
        if parsed_curl.data:
            # 尝试解析为JSON
            try:
                if isinstance(parsed_curl.data, str) and parsed_curl.data.strip().startswith('{'):
                    result["data"] = json.loads(parsed_curl.data)
                else:
                    result["data"] = parsed_curl.data
            except json.JSONDecodeError:
                result["data"] = parsed_curl.data
        elif parsed_curl.data_binary:
            result["data"] = parsed_curl.data_binary
            
        # 处理cookies
        if parsed_curl.cookies:
            result["cookies"] = parsed_curl.cookies
            
        # 处理代理
        if parsed_curl.proxy:
            result["proxy"] = parsed_curl.proxy
            
        # 处理认证信息
        if parsed_curl.user:
            username, password = parsed_curl.user
            result["auth"] = {
                "type": "basic",
                "username": username,
                "password": password
            }
            
        return result
    except Exception as e:
        return {"error": f"解析curl命令出错: {str(e)}"}


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
