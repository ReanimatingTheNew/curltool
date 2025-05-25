from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
import shlex
import json
import re
import urllib.parse
from code_to_curl import code_to_curl
from curl_to_code_main import convert_curl_to_code, SUPPORTED_LANGUAGES
from new_parse_curl import parse_curl, parse_curl_original

app = Flask(__name__)
CORS(app)  # Enable CORS

# parse_curl函数已经从new_parse_curl.py导入

@app.route('/')
def index():
    """Render the main page"""
    return render_template('new_index.html')

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/examples')
def examples():
    """Examples page"""
    return render_template('examples.html')

@app.route('/api-docs')
def api_docs():
    """API docs page"""
    return render_template('api_docs.html')

# 添加特定编程语言转换页面的路由
@app.route('/curl-to-python/')
def curl_to_python():
    """Python specific conversion page"""
    return render_template('new_index.html', target_language="python")

@app.route('/curl-to-javascript/')
def curl_to_javascript():
    """JavaScript specific conversion page"""
    return render_template('new_index.html', target_language="javascript")

@app.route('/curl-to-php/')
def curl_to_php():
    """PHP specific conversion page"""
    return render_template('new_index.html', target_language="php")

@app.route('/curl-to-java/')
def curl_to_java():
    """Java specific conversion page"""
    return render_template('new_index.html', target_language="java")

@app.route('/curl-to-csharp/')
def curl_to_csharp():
    """C# specific conversion page"""
    return render_template('new_index.html', target_language="csharp")

@app.route('/curl-to-ruby/')
def curl_to_ruby():
    """Ruby specific conversion page"""
    return render_template('new_index.html', target_language="ruby")

@app.route('/curl-to-go/')
def curl_to_go():
    """Go specific conversion page"""
    return render_template('new_index.html', target_language="go")

@app.route('/curl-to-swift/')
def curl_to_swift():
    """Swift specific conversion page"""
    return render_template('new_index.html', target_language="swift")

@app.route('/curl-to-rust/')
def curl_to_rust():
    """Rust specific conversion page"""
    return render_template('new_index.html', target_language="rust")

# 教程页面路由
@app.route('/tutorials/curl-to-python/')
def tutorial_curl_to_python():
    """CURL to Python tutorial page"""
    return render_template('tutorials/curl_to_python.html')

@app.route('/tutorials/curl-authentication-examples/')
def tutorial_curl_auth():
    """CURL authentication tutorial page"""
    # Temporary redirect to Python tutorial until the page is created
    return redirect('/tutorials/curl-to-python/')

@app.route('/tutorials/api-testing-with-curl/')
def tutorial_api_testing():
    """API testing tutorial page"""
    # Temporary redirect to Python tutorial until the page is created
    return redirect('/tutorials/curl-to-python/')

@app.route('/old')
def old_ui():
    """渲染旧的UI界面"""
    return render_template('index.html')

@app.route('/robots.txt')
def robots():
    """提供robots.txt文件"""
    return app.send_static_file('robots.txt')

@app.route('/sitemap.xml')
def sitemap():
    """提供sitemap.xml文件"""
    return app.send_static_file('sitemap.xml')

@app.route('/BingSiteAuth.xml')
def bing_site_auth():
    """提供BingSiteAuth.xml文件，用于Bing网站验证"""
    return app.send_static_file('BingSiteAuth.xml')

@app.route('/2a31de34a07f42dba5238b80bbd504de.txt')
def indexnow_key():
    """提供IndexNow API密钥文件"""
    return app.send_static_file('2a31de34a07f42dba5238b80bbd504de.txt')

@app.route('/llms.txt')
def llms():
    """提供llms.txt文件，指导AI大语言模型如何处理网站内容"""
    return app.send_static_file('llms.txt')

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
        
        # 检查是否有错误
        if "error" in result:
            print("解析错误:", result["error"])
            return jsonify(result), 400
        
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
