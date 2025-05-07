from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import shlex
import json
import re
from code_to_curl import code_to_curl
from curl_to_code_main import convert_curl_to_code, SUPPORTED_LANGUAGES

app = Flask(__name__)
CORS(app)  # 启用跨域支持

def parse_curl(curl_command):
    """将curl命令解析为JSON格式"""
    result = {
        "method": "GET",
        "url": "",
        "headers": {},
        "data": None,
        "cookies": {}
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

@app.route('/')
def index():
    """渲染主页"""
    return render_template('index.html')

@app.route('/robots.txt')
def robots():
    """提供robots.txt文件"""
    return app.send_static_file('robots.txt')

@app.route('/sitemap.xml')
def sitemap():
    """提供sitemap.xml文件"""
    return app.send_static_file('sitemap.xml')

@app.route('/api/convert', methods=['POST'])
def convert():
    """API端点：将curl命令转换为JSON"""
    print("收到API请求，内容类型:", request.content_type)
    print("请求数据:", request.data)
    
    try:
        data = request.get_json(force=True)
        print("解析后的JSON数据:", data)
        
        if not data or 'curl' not in data:
            print("错误: 缺少curl参数")
            return jsonify({"error": "请提供curl命令"}), 400
        
        curl_command = data['curl']
        print("curl命令:", curl_command)
        
        result = parse_curl(curl_command)
        print("解析结果:", result)
        
        return jsonify(result)
    except Exception as e:
        print("处理请求时出错:", str(e))
        return jsonify({"error": f"处理请求时出错: {str(e)}"}), 500

@app.route('/convert', methods=['POST'])
def convert_web():
    """Web表单提交处理：将curl命令转换为JSON"""
    curl_command = request.form.get('curl', '')
    
    if not curl_command:
        return jsonify({"error": "请提供curl命令"}), 400
    
    result = parse_curl(curl_command)
    return jsonify(result)

@app.route('/api/reverse', methods=['POST'])
def reverse_convert():
    """API端点：将代码转换为curl命令"""
    print("收到反向转换API请求，内容类型:", request.content_type)
    print("请求数据:", request.data)
    
    try:
        data = request.get_json(force=True)
        print("解析后的JSON数据:", data)
        
        if not data or 'code' not in data or 'language' not in data:
            print("错误: 缺少code或language参数")
            return jsonify({"error": "请提供代码和语言"}), 400
        
        code = data['code']
        language = data['language']
        print(f"代码语言: {language}")
        
        result = code_to_curl(code, language)
        print("解析结果:", result)
        
        return jsonify(result)
    except Exception as e:
        print("处理请求时出错:", str(e))
        return jsonify({"error": f"处理请求时出错: {str(e)}"}), 500

@app.route('/api/languages', methods=['GET'])
def get_supported_languages():
    """API端点：获取支持的编程语言列表"""
    return jsonify({"languages": SUPPORTED_LANGUAGES})

@app.route('/api/curl-to-code', methods=['POST'])
def curl_to_code():
    """API端点：将curl命令转换为指定编程语言的代码"""
    print("收到curl转代码API请求，内容类型:", request.content_type)
    print("请求数据:", request.data)
    
    try:
        data = request.get_json(force=True)
        print("解析后的JSON数据:", data)
        
        if not data or 'curl' not in data or 'language' not in data:
            print("错误: 缺少curl或language参数")
            return jsonify({"error": "请提供curl命令和目标语言"}), 400
        
        curl_command = data['curl']
        language = data['language'].lower()
        print(f"目标语言: {language}")
        
        if language not in SUPPORTED_LANGUAGES:
            return jsonify({"error": f"不支持的语言: {language}", "supported": SUPPORTED_LANGUAGES}), 400
        
        code = convert_curl_to_code(curl_command, language)
        print("转换结果长度:", len(code))
        
        return jsonify({"code": code, "language": language})
    except Exception as e:
        print("处理请求时出错:", str(e))
        return jsonify({"error": f"处理请求时出错: {str(e)}"}), 500

@app.route('/reverse', methods=['POST'])
def reverse_convert_web():
    """Web表单提交处理：将代码转换为curl命令"""
    code = request.form.get('code', '')
    language = request.form.get('language', '')
    
    if not code or not language:
        return jsonify({"error": "请提供代码和语言"}), 400
    
    result = code_to_curl(code, language)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
