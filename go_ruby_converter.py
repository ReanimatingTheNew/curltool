"""
curl命令转换为Go和Ruby代码的模块
"""

def to_go(curl_dict):
    """将curl命令转换为Go代码"""
    if "error" in curl_dict:
        return f"// Error: {curl_dict['error']}"
    
    code = [
        "package main",
        "",
        "import (",
        "\t\"bytes\"",
        "\t\"crypto/tls\"",
        "\t\"encoding/json\"",
        "\t\"fmt\"",
        "\t\"io\"",
        "\t\"io/ioutil\"",
        "\t\"mime/multipart\"",
        "\t\"net/http\"",
        "\t\"net/url\"",
        "\t\"os\"",
        "\t\"path/filepath\"",
        "\t\"strings\"",
        "\t\"time\"",
        ")",
        "",
        "func main() {"
    ]
    
    # 创建客户端
    code.append("\t// 创建HTTP客户端")
    code.append("\tclient := &http.Client{")
    
    # 设置超时
    if curl_dict["timeout"] is not None:
        code.append(f"\t\tTimeout: {curl_dict['timeout']} * time.Second,")
    
    # 设置重定向策略
    if not curl_dict["allow_redirects"]:
        code.append("\t\tCheckRedirect: func(req *http.Request, via []*http.Request) error {")
        code.append("\t\t\treturn http.ErrUseLastResponse")
        code.append("\t\t},")
    
    # 设置SSL验证
    if not curl_dict["verify_ssl"]:
        code.append("\t\tTransport: &http.Transport{")
        code.append("\t\t\tTLSClientConfig: &tls.Config{InsecureSkipVerify: true},")
        code.append("\t\t},")
    
    code.append("\t}")
    
    # 创建请求
    if curl_dict["form_data"] is not None:
        code.append("\t// 创建multipart表单")
        code.append("\tvar requestBody bytes.Buffer")
        code.append("\tmultipartWriter := multipart.NewWriter(&requestBody)")
        
        for key, value in curl_dict["form_data"].items():
            if value["type"] == "file":
                code.append(f"\t// 添加文件 {key}")
                code.append(f"\tfilePath := \"{value['path']}\"")
                code.append("\tfile, err := os.Open(filePath)")
                code.append("\tif err != nil {")
                code.append("\t\tfmt.Println(\"Error opening file:\", err)")
                code.append("\t\treturn")
                code.append("\t}")
                code.append("\tdefer file.Close()")
                code.append("\t")
                code.append("\tfileInfo, _ := file.Stat()")
                code.append("\tfileField, err := multipartWriter.CreateFormFile(\"" + key + "\", filepath.Base(filePath))")
                code.append("\tif err != nil {")
                code.append("\t\tfmt.Println(\"Error creating form file:\", err)")
                code.append("\t\treturn")
                code.append("\t}")
                code.append("\t")
                code.append("\t_, err = io.Copy(fileField, file)")
                code.append("\tif err != nil {")
                code.append("\t\tfmt.Println(\"Error copying file to form:\", err)")
                code.append("\t\treturn")
                code.append("\t}")
            else:
                code.append(f"\t// 添加表单字段 {key}")
                code.append(f"\tfield, err := multipartWriter.CreateFormField(\"{key}\")")
                code.append("\tif err != nil {")
                code.append("\t\tfmt.Println(\"Error creating form field:\", err)")
                code.append("\t\treturn")
                code.append("\t}")
                code.append(f"\t_, err = field.Write([]byte(\"{value['value']}\"))")
                code.append("\tif err != nil {")
                code.append("\t\tfmt.Println(\"Error writing to form field:\", err)")
                code.append("\t\treturn")
                code.append("\t}")
        
        code.append("\t// 关闭multipart写入器")
        code.append("\terr := multipartWriter.Close()")
        code.append("\tif err != nil {")
        code.append("\t\tfmt.Println(\"Error closing multipart writer:\", err)")
        code.append("\t\treturn")
        code.append("\t}")
        
        code.append(f"\t// 创建请求")
        code.append(f"\treq, err := http.NewRequest(\"{curl_dict['method']}\", \"{curl_dict['url']}\", &requestBody)")
        code.append("\tif err != nil {")
        code.append("\t\tfmt.Println(\"Error creating request:\", err)")
        code.append("\t\treturn")
        code.append("\t}")
        
        code.append("\t// 设置Content-Type头")
        code.append("\treq.Header.Set(\"Content-Type\", multipartWriter.FormDataContentType())")
    
    elif curl_dict["data"] is not None:
        if isinstance(curl_dict["data"], dict):
            if curl_dict["headers"].get("Content-Type", "").lower() == "application/json":
                code.append("\t// 创建JSON请求体")
                code.append("\tjsonData := map[string]interface{}{")
                for key, value in curl_dict["data"].items():
                    if isinstance(value, str):
                        code.append(f"\t\t\"{key}\": \"{value}\",")
                    else:
                        code.append(f"\t\t\"{key}\": {value},")
                code.append("\t}")
                code.append("\t")
                code.append("\tjsonBytes, err := json.Marshal(jsonData)")
                code.append("\tif err != nil {")
                code.append("\t\tfmt.Println(\"Error marshaling JSON:\", err)")
                code.append("\t\treturn")
                code.append("\t}")
                code.append("\t")
                code.append(f"\t// 创建请求")
                code.append(f"\treq, err := http.NewRequest(\"{curl_dict['method']}\", \"{curl_dict['url']}\", bytes.NewBuffer(jsonBytes))")
                code.append("\tif err != nil {")
                code.append("\t\tfmt.Println(\"Error creating request:\", err)")
                code.append("\t\treturn")
                code.append("\t}")
                
                code.append("\t// 设置Content-Type头")
                code.append("\treq.Header.Set(\"Content-Type\", \"application/json\")")
            else:
                code.append("\t// 创建表单数据")
                code.append("\tformData := url.Values{}")
                for key, value in curl_dict["data"].items():
                    code.append(f"\tformData.Set(\"{key}\", \"{value}\")")
                code.append("\t")
                code.append(f"\t// 创建请求")
                code.append(f"\treq, err := http.NewRequest(\"{curl_dict['method']}\", \"{curl_dict['url']}\", strings.NewReader(formData.Encode()))")
                code.append("\tif err != nil {")
                code.append("\t\tfmt.Println(\"Error creating request:\", err)")
                code.append("\t\treturn")
                code.append("\t}")
                
                code.append("\t// 设置Content-Type头")
                code.append("\treq.Header.Set(\"Content-Type\", \"application/x-www-form-urlencoded\")")
        else:
            code.append("\t// 创建请求体")
            code.append(f"\treqBody := strings.NewReader(`{curl_dict['data']}`)")
            code.append(f"\t// 创建请求")
            code.append(f"\treq, err := http.NewRequest(\"{curl_dict['method']}\", \"{curl_dict['url']}\", reqBody)")
            code.append("\tif err != nil {")
            code.append("\t\tfmt.Println(\"Error creating request:\", err)")
            code.append("\t\treturn")
            code.append("\t}")
            
            # 如果有Content-Type头，使用它
            if "Content-Type" in curl_dict["headers"]:
                code.append(f"\t// 设置Content-Type头")
                code.append(f"\treq.Header.Set(\"Content-Type\", \"{curl_dict['headers']['Content-Type']}\")")
    else:
        code.append(f"\t// 创建请求")
        code.append(f"\treq, err := http.NewRequest(\"{curl_dict['method']}\", \"{curl_dict['url']}\", nil)")
        code.append("\tif err != nil {")
        code.append("\t\tfmt.Println(\"Error creating request:\", err)")
        code.append("\t\treturn")
        code.append("\t}")
    
    # 设置headers
    if curl_dict["headers"]:
        code.append("\t// 设置请求头")
        for key, value in curl_dict["headers"].items():
            # 跳过Content-Type，因为它可能已经设置过了
            if key != "Content-Type" or (curl_dict["data"] is None and curl_dict["form_data"] is None):
                code.append(f"\treq.Header.Set(\"{key}\", \"{value}\")")
    
    # 设置cookies
    if "cookies" in curl_dict and curl_dict["cookies"]:
        code.append("\t// 设置Cookies")
        for key, value in curl_dict["cookies"].items():
            code.append(f"\treq.AddCookie(&http.Cookie{{Name: \"{key}\", Value: \"{value}\"}})")
    
    # 设置basic auth
    if curl_dict["auth"] is not None and curl_dict["auth"]["type"] == "basic" and "username" in curl_dict["auth"]:
        code.append("\t// 设置Basic认证")
        code.append(f"\treq.SetBasicAuth(\"{curl_dict['auth']['username']}\", \"{curl_dict['auth']['password']}\")")
    
    # 发送请求
    code.append("\t// 发送请求")
    code.append("\tresp, err := client.Do(req)")
    code.append("\tif err != nil {")
    code.append("\t\tfmt.Println(\"Error sending request:\", err)")
    code.append("\t\treturn")
    code.append("\t}")
    code.append("\tdefer resp.Body.Close()")
    
    # 获取响应
    code.append("\t// 获取响应状态码")
    code.append("\tfmt.Println(\"Status:\", resp.Status)")
    code.append("\t")
    code.append("\t// 获取响应头")
    code.append("\tfmt.Println(\"Headers:\")")
    code.append("\tfor name, values := range resp.Header {")
    code.append("\t\tfor _, value := range values {")
    code.append("\t\t\tfmt.Printf(\"%s: %s\\n\", name, value)")
    code.append("\t\t}")
    code.append("\t}")
    code.append("\t")
    code.append("\t// 读取响应体")
    code.append("\tbody, err := ioutil.ReadAll(resp.Body)")
    code.append("\tif err != nil {")
    code.append("\t\tfmt.Println(\"Error reading response body:\", err)")
    code.append("\t\treturn")
    code.append("\t}")
    code.append("\t")
    code.append("\tfmt.Println(\"Response Body:\")")
    code.append("\tfmt.Println(string(body))")
    code.append("\t")
    code.append("\t// 尝试解析JSON")
    code.append("\tvar jsonData interface{}")
    code.append("\tif err := json.Unmarshal(body, &jsonData); err == nil {")
    code.append("\t\tjsonFormatted, _ := json.MarshalIndent(jsonData, \"\", \"  \")")
    code.append("\t\tfmt.Println(\"JSON Response:\")")
    code.append("\t\tfmt.Println(string(jsonFormatted))")
    code.append("\t} else {")
    code.append("\t\tfmt.Println(\"Response is not valid JSON\")")
    code.append("\t}")
    
    code.append("}")
    
    return "\n".join(code)

def to_ruby(curl_dict):
    """将curl命令转换为Ruby代码"""
    if "error" in curl_dict:
        return f"# Error: {curl_dict['error']}"
    
    code = [
        "require 'net/http'",
        "require 'uri'",
        "require 'json'",
        "require 'openssl'"
    ]
    
    # 如果有表单数据，需要引入额外的库
    if curl_dict["form_data"] is not None:
        code.append("require 'mime/types'")
    
    code.append("")
    code.append("# 解析URL")
    code.append(f"uri = URI.parse('{curl_dict['url']}')")
    
    # 创建HTTP对象
    code.append("")
    code.append("# 创建HTTP对象")
    code.append("http = Net::HTTP.new(uri.host, uri.port)")
    
    # 设置HTTPS
    code.append("")
    code.append("# 设置HTTPS")
    code.append("if uri.scheme == 'https'")
    code.append("  http.use_ssl = true")
    
    # 设置SSL验证
    if not curl_dict["verify_ssl"]:
        code.append("  # 禁用SSL验证")
        code.append("  http.verify_mode = OpenSSL::SSL::VERIFY_NONE")
    else:
        code.append("  http.verify_mode = OpenSSL::SSL::VERIFY_PEER")
    
    code.append("end")
    
    # 设置超时
    if curl_dict["timeout"] is not None:
        code.append("")
        code.append("# 设置超时")
        code.append(f"http.open_timeout = {curl_dict['timeout']}")
        code.append(f"http.read_timeout = {curl_dict['timeout']}")
    
    # 创建请求
    code.append("")
    code.append("# 创建请求")
    
    # 根据请求方法创建不同的请求对象
    if curl_dict["method"] == "GET":
        code.append("request = Net::HTTP::Get.new(uri.request_uri)")
    elif curl_dict["method"] == "POST":
        code.append("request = Net::HTTP::Post.new(uri.request_uri)")
    elif curl_dict["method"] == "PUT":
        code.append("request = Net::HTTP::Put.new(uri.request_uri)")
    elif curl_dict["method"] == "DELETE":
        code.append("request = Net::HTTP::Delete.new(uri.request_uri)")
    elif curl_dict["method"] == "PATCH":
        code.append("request = Net::HTTP::Patch.new(uri.request_uri)")
    elif curl_dict["method"] == "HEAD":
        code.append("request = Net::HTTP::Head.new(uri.request_uri)")
    elif curl_dict["method"] == "OPTIONS":
        code.append("request = Net::HTTP::Options.new(uri.request_uri)")
    else:
        code.append(f"request = Net::HTTP.const_get('{curl_dict['method'].capitalize}').new(uri.request_uri)")
    
    # 设置headers
    if curl_dict["headers"]:
        code.append("")
        code.append("# 设置请求头")
        for key, value in curl_dict["headers"].items():
            code.append(f"request['{key}'] = '{value}'")
    
    # 设置cookies
    if "cookies" in curl_dict and curl_dict["cookies"]:
        code.append("")
        code.append("# 设置Cookies")
        cookie_parts = []
        for key, value in curl_dict["cookies"].items():
            cookie_parts.append(f"{key}={value}")
        code.append(f"request['Cookie'] = '{'; '.join(cookie_parts)}'")
    
    # 设置basic auth
    if curl_dict["auth"] is not None and curl_dict["auth"]["type"] == "basic" and "username" in curl_dict["auth"]:
        code.append("")
        code.append("# 设置Basic认证")
        code.append(f"request.basic_auth('{curl_dict['auth']['username']}', '{curl_dict['auth']['password']}')")
    
    # 设置请求体
    if curl_dict["data"] is not None:
        code.append("")
        code.append("# 设置请求体")
        if isinstance(curl_dict["data"], dict):
            if curl_dict["headers"].get("Content-Type", "").lower() == "application/json":
                # 构建JSON
                code.append("request.body = {")
                for key, value in curl_dict["data"].items():
                    if isinstance(value, str):
                        code.append(f"  '{key}' => '{value}',")
                    else:
                        code.append(f"  '{key}' => {value},")
                code.append("}.to_json")
            else:
                # 构建表单数据
                form_parts = []
                for key, value in curl_dict["data"].items():
                    form_parts.append(f"{key}={value}")
                code.append(f"request.body = '{form_parts}'")
        else:
            # 字符串形式的data
            code.append(f"request.body = '{curl_dict['data']}'")
    
    # 设置表单数据
    elif curl_dict["form_data"] is not None:
        code.append("")
        code.append("# 设置multipart表单数据")
        code.append("boundary = '----RubyFormBoundary' + SecureRandom.hex(16)")
        code.append("request['Content-Type'] = 'multipart/form-data; boundary=' + boundary")
        code.append("body = []")
        
        for key, value in curl_dict["form_data"].items():
            if value["type"] == "file":
                file_name = value["path"].split("/")[-1]
                code.append(f"# 添加文件 {key}")
                code.append(f"file_path = '{value['path']}'")
                code.append("file_content = File.read(file_path)")
                code.append("mime_type = MIME::Types.type_for(file_path).first.to_s")
                code.append("body << \"--#{boundary}\\r\\n\"")
                code.append(f"body << \"Content-Disposition: form-data; name=\\\"{key}\\\"; filename=\\\"{file_name}\\\"\\r\\n\"")
                code.append("body << \"Content-Type: #{mime_type}\\r\\n\\r\\n\"")
                code.append("body << file_content")
                code.append("body << \"\\r\\n\"")
            else:
                code.append(f"# 添加表单字段 {key}")
                code.append("body << \"--#{boundary}\\r\\n\"")
                code.append(f"body << \"Content-Disposition: form-data; name=\\\"{key}\\\"\\r\\n\\r\\n\"")
                code.append(f"body << \"{value['value']}\\r\\n\"")
        
        code.append("body << \"--#{boundary}--\\r\\n\"")
        code.append("request.body = body.join")
    
    # 发送请求
    code.append("")
    code.append("# 发送请求")
    code.append("begin")
    code.append("  response = http.request(request)")
    code.append("  ")
    code.append("  # 获取响应状态码")
    code.append("  puts \"Status: #{response.code} #{response.message}\"")
    code.append("  ")
    code.append("  # 获取响应头")
    code.append("  puts \"Headers:\"")
    code.append("  response.each_header do |key, value|")
    code.append("    puts \"#{key}: #{value}\"")
    code.append("  end")
    code.append("  ")
    code.append("  # 获取响应内容")
    code.append("  puts \"Response Body:\"")
    code.append("  puts response.body")
    code.append("  ")
    code.append("  # 尝试解析JSON")
    code.append("  begin")
    code.append("    json = JSON.parse(response.body)")
    code.append("    puts \"JSON Response:\"")
    code.append("    puts JSON.pretty_generate(json)")
    code.append("  rescue JSON::ParserError")
    code.append("    puts \"Response is not valid JSON\"")
    code.append("  end")
    code.append("rescue => e")
    code.append("  puts \"Error: #{e.message}\"")
    code.append("end")
    
    return "\n".join(code)
