"""
curl命令转换为Rust和Swift代码的模块
"""

def to_rust(curl_dict):
    """将curl命令转换为Rust代码"""
    if "error" in curl_dict:
        return f"// Error: {curl_dict['error']}"
    
    code = [
        "use reqwest::blocking::Client;",
        "use reqwest::header::{HeaderMap, HeaderValue, CONTENT_TYPE};",
        "use std::collections::HashMap;",
        "use std::fs::File;",
        "use std::io::Read;",
        "use std::time::Duration;",
        "",
        "fn main() -> Result<(), Box<dyn std::error::Error>> {"
    ]
    
    # 创建客户端
    code.append("    // 创建客户端")
    code.append("    let client = Client::builder()")
    
    # 设置超时
    if curl_dict["timeout"] is not None:
        code.append(f"        .timeout(Duration::from_secs({int(curl_dict['timeout'])}))")
    
    # 设置重定向
    if not curl_dict["allow_redirects"]:
        code.append("        .redirect(reqwest::redirect::Policy::none())")
    
    # 设置SSL验证
    if not curl_dict["verify_ssl"]:
        code.append("        .danger_accept_invalid_certs(true)")
    
    code.append("        .build()?;")
    
    # 创建请求
    code.append(f"    // 创建{curl_dict['method']}请求")
    code.append(f"    let mut request = client.{curl_dict['method'].lower()}(\"{curl_dict['url']}\");")
    
    # 设置headers
    if curl_dict["headers"]:
        code.append("    // 设置请求头")
        code.append("    let mut headers = HeaderMap::new();")
        for key, value in curl_dict["headers"].items():
            code.append(f"    headers.insert(\"{key}\", HeaderValue::from_static(\"{value}\"));")
        code.append("    request = request.headers(headers);")
    
    # 设置basic auth
    if curl_dict["auth"] is not None and curl_dict["auth"]["type"] == "basic" and "username" in curl_dict["auth"]:
        code.append("    // 设置Basic认证")
        code.append(f"    request = request.basic_auth(\"{curl_dict['auth']['username']}\", Some(\"{curl_dict['auth']['password']}\"));")
    
    # 设置请求体
    if curl_dict["data"] is not None:
        code.append("    // 设置请求体")
        if isinstance(curl_dict["data"], dict):
            if curl_dict["headers"].get("Content-Type", "").lower() == "application/json":
                # 构建JSON
                code.append("    let mut json_data = HashMap::new();")
                for key, value in curl_dict["data"].items():
                    if isinstance(value, str):
                        code.append(f"    json_data.insert(\"{key}\", \"{value}\");")
                    else:
                        code.append(f"    json_data.insert(\"{key}\", {value});")
                code.append("    request = request.json(&json_data);")
            else:
                # 构建表单数据
                code.append("    let mut form_data = HashMap::new();")
                for key, value in curl_dict["data"].items():
                    code.append(f"    form_data.insert(\"{key}\", \"{value}\");")
                code.append("    request = request.form(&form_data);")
        else:
            # 字符串形式的data
            code.append(f"    request = request.body(\"{curl_dict['data']}\");")
    
    # 设置表单数据
    elif curl_dict["form_data"] is not None:
        code.append("    // 设置multipart表单数据")
        code.append("    let mut form = reqwest::blocking::multipart::Form::new();")
        
        for key, value in curl_dict["form_data"].items():
            if value["type"] == "file":
                code.append(f"    // 添加文件 {key}")
                code.append(f"    let file_path = \"{value['path']}\";")
                code.append("    let file_name = std::path::Path::new(file_path).file_name().unwrap().to_str().unwrap();")
                code.append("    let mut file = File::open(file_path)?;")
                code.append("    let mut buffer = Vec::new();")
                code.append("    file.read_to_end(&mut buffer)?;")
                code.append("    form = form.part(\"" + key + "\", reqwest::blocking::multipart::Part::bytes(buffer).file_name(file_name.to_string()));")
            else:
                code.append(f"    // 添加表单字段 {key}")
                code.append("    form = form.text(\"" + key + "\", \"" + value["value"] + "\");")
        
        code.append("    request = request.multipart(form);")
    
    # 发送请求
    code.append("    // 发送请求")
    code.append("    let response = request.send()?;")
    
    # 获取响应
    code.append("    // 获取响应状态码")
    code.append("    println!(\"Status: {}\", response.status());")
    code.append("    ")
    code.append("    // 获取响应头")
    code.append("    println!(\"Headers: {:#?}\", response.headers());")
    code.append("    ")
    code.append("    // 获取响应内容")
    code.append("    let body = response.text()?;")
    code.append("    println!(\"Body: {}\", body);")
    code.append("    ")
    code.append("    // 尝试解析JSON")
    code.append("    match serde_json::from_str::<serde_json::Value>(&body) {")
    code.append("        Ok(json) => println!(\"JSON: {:#?}\", json),")
    code.append("        Err(_) => println!(\"Response is not valid JSON\"),")
    code.append("    }")
    
    code.append("    ")
    code.append("    Ok(())")
    code.append("}")
    
    return "\n".join(code)

def to_swift(curl_dict):
    """将curl命令转换为Swift代码"""
    if "error" in curl_dict:
        return f"// Error: {curl_dict['error']}"
    
    code = [
        "import Foundation",
        "",
        "// 创建URL请求",
        "guard let url = URL(string: \"" + curl_dict["url"] + "\") else {",
        "    print(\"Invalid URL\")",
        "    exit(1)",
        "}",
        "",
        "var request = URLRequest(url: url)"
    ]
    
    # 设置请求方法
    code.append(f"request.httpMethod = \"{curl_dict['method']}\"")
    
    # 设置超时
    if curl_dict["timeout"] is not None:
        code.append(f"request.timeoutInterval = {curl_dict['timeout']}")
    
    # 设置headers
    if curl_dict["headers"]:
        code.append("\n// 设置请求头")
        for key, value in curl_dict["headers"].items():
            code.append(f"request.setValue(\"{value}\", forHTTPHeaderField: \"{key}\")")
    
    # 设置cookies
    if "cookies" in curl_dict and curl_dict["cookies"]:
        code.append("\n// 设置Cookies")
        cookie_parts = []
        for key, value in curl_dict["cookies"].items():
            cookie_parts.append(f"{key}={value}")
        code.append(f"request.setValue(\"{'; '.join(cookie_parts)}\", forHTTPHeaderField: \"Cookie\")")
    
    # 设置basic auth
    if curl_dict["auth"] is not None and curl_dict["auth"]["type"] == "basic" and "username" in curl_dict["auth"]:
        code.append("\n// 设置Basic认证")
        code.append(f"let loginString = \"{curl_dict['auth']['username']}:{curl_dict['auth']['password']}\"")
        code.append("let loginData = loginString.data(using: .utf8)!")
        code.append("let base64LoginString = loginData.base64EncodedString()")
        code.append("request.setValue(\"Basic \\(base64LoginString)\", forHTTPHeaderField: \"Authorization\")")
    
    # 设置请求体
    if curl_dict["data"] is not None:
        code.append("\n// 设置请求体")
        if isinstance(curl_dict["data"], dict):
            if curl_dict["headers"].get("Content-Type", "").lower() == "application/json":
                # 构建JSON
                code.append("let jsonData: [String: Any] = [")
                for key, value in curl_dict["data"].items():
                    if isinstance(value, str):
                        code.append(f"    \"{key}\": \"{value}\",")
                    else:
                        code.append(f"    \"{key}\": {value},")
                code.append("]")
                code.append("do {")
                code.append("    let jsonData = try JSONSerialization.data(withJSONObject: jsonData, options: [])")
                code.append("    request.httpBody = jsonData")
                code.append("} catch {")
                code.append("    print(\"Error creating JSON data: \\(error)\")")
                code.append("    exit(1)")
                code.append("}")
            else:
                # 构建表单数据
                code.append("var components = URLComponents()")
                code.append("components.queryItems = [")
                for key, value in curl_dict["data"].items():
                    code.append(f"    URLQueryItem(name: \"{key}\", value: \"{value}\"),")
                code.append("]")
                code.append("request.httpBody = components.query?.data(using: .utf8)")
        else:
            # 字符串形式的data
            code.append(f"request.httpBody = \"{curl_dict['data']}\".data(using: .utf8)")
    
    # 设置表单数据
    elif curl_dict["form_data"] is not None:
        code.append("\n// 设置multipart表单数据")
        code.append("let boundary = \"Boundary-\\(UUID().uuidString)\"")
        code.append("request.setValue(\"multipart/form-data; boundary=\\(boundary)\", forHTTPHeaderField: \"Content-Type\")")
        code.append("")
        code.append("var body = Data()")
        
        for key, value in curl_dict["form_data"].items():
            code.append(f"\n// 添加表单项 {key}")
            code.append("body.append(\"--\\(boundary)\\r\\n\".data(using: .utf8)!)")
            
            if value["type"] == "file":
                file_name = value["path"].split("/")[-1]
                code.append(f"body.append(\"Content-Disposition: form-data; name=\\\"{key}\\\"; filename=\\\"{file_name}\\\"\\r\\n\".data(using: .utf8)!)")
                code.append("body.append(\"Content-Type: application/octet-stream\\r\\n\\r\\n\".data(using: .utf8)!)")
                code.append("// 注意：在实际应用中，您需要读取文件内容并添加")
                code.append(f"// let fileURL = URL(fileURLWithPath: \"{value['path']}\")")
                code.append("// let fileData = try! Data(contentsOf: fileURL)")
                code.append("// body.append(fileData)")
                code.append("// 这里使用占位符")
                code.append("body.append(\"[File content placeholder]\\r\\n\".data(using: .utf8)!)")
            else:
                code.append(f"body.append(\"Content-Disposition: form-data; name=\\\"{key}\\\"\\r\\n\\r\\n\".data(using: .utf8)!)")
                code.append(f"body.append(\"{value['value']}\\r\\n\".data(using: .utf8)!)")
        
        code.append("\n// 添加结束边界")
        code.append("body.append(\"--\\(boundary)--\\r\\n\".data(using: .utf8)!)")
        code.append("request.httpBody = body")
    
    # 创建会话
    code.append("\n// 创建会话")
    code.append("let configuration = URLSessionConfiguration.default")
    
    # 设置是否验证SSL
    if not curl_dict["verify_ssl"]:
        code.append("// 注意：在生产环境中不建议禁用SSL验证")
        code.append("// 这里仅作示例，实际应用中应使用适当的证书验证")
        code.append("// configuration.tlsMinimumSupportedProtocolVersion = .tlsProtocol1")
    
    code.append("let session = URLSession(configuration: configuration)")
    
    # 发送请求
    code.append("\n// 发送请求")
    code.append("let task = session.dataTask(with: request) { data, response, error in")
    code.append("    if let error = error {")
    code.append("        print(\"Error: \\(error)\")")
    code.append("        return")
    code.append("    }")
    code.append("    ")
    code.append("    guard let httpResponse = response as? HTTPURLResponse else {")
    code.append("        print(\"Invalid response\")")
    code.append("        return")
    code.append("    }")
    code.append("    ")
    code.append("    print(\"Status Code: \\(httpResponse.statusCode)\")")
    code.append("    print(\"Headers: \\(httpResponse.allHeaderFields)\")")
    code.append("    ")
    code.append("    if let data = data, let responseString = String(data: data, encoding: .utf8) {")
    code.append("        print(\"Response Body: \\(responseString)\")")
    code.append("        ")
    code.append("        // 尝试解析JSON")
    code.append("        do {")
    code.append("            if let json = try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any] {")
    code.append("                print(\"JSON Response: \\(json)\")")
    code.append("            }")
    code.append("        } catch {")
    code.append("            print(\"Response is not valid JSON\")")
    code.append("        }")
    code.append("    }")
    code.append("}")
    
    code.append("\n// 启动任务")
    code.append("task.resume()")
    
    code.append("\n// 保持程序运行，直到请求完成")
    code.append("RunLoop.main.run(until: Date(timeIntervalSinceNow: 10))")
    
    return "\n".join(code)
