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
        code.append(f"\t\tTimeout: {int(curl_dict['timeout'])} * time.Second,")
    
    # 设置重定向策略
    if not curl_dict["allow_redirects"]:
        code.append("\t\tCheckRedirect: func(req *http.Request, via []*http.Request) error {")
        code.append("\t\t\treturn http.ErrUseLastResponse")
        code.append("\t\t},")
    
    code.append("\t}")
    
    # 处理请求体
    if curl_dict["data"] is not None:
        code.append("\n\t// 准备请求体")
        if isinstance(curl_dict["data"], dict):
            if curl_dict["headers"].get("Content-Type", "").lower() == "application/json":
                code.append("\tdata := map[string]interface{}{")
                for key, value in curl_dict["data"].items():
                    if isinstance(value, str):
                        code.append(f"\t\t\"{key}\": \"{value}\",")
                    else:
                        code.append(f"\t\t\"{key}\": {value},")
                code.append("\t}")
                code.append("\tpayloadBytes, err := json.Marshal(data)")
                code.append("\tif err != nil {")
                code.append("\t\tpanic(err)")
                code.append("\t}")
                code.append("\tpayload := bytes.NewReader(payloadBytes)")
            else:
                code.append("\tform := url.Values{}")
                for key, value in curl_dict["data"].items():
                    code.append(f"\tform.Add(\"{key}\", \"{value}\")")
                code.append("\tpayload := strings.NewReader(form.Encode())")
        else:
            # 字符串形式的data
            code.append(f"\tpayload := strings.NewReader(`{curl_dict['data']}`)")
    elif curl_dict["form_data"] is not None:
        code.append("\n\t// 准备multipart表单")
        code.append("\tvar b bytes.Buffer")
        code.append("\tw := multipart.NewWriter(&b)")
        
        for key, value in curl_dict["form_data"].items():
            if value["type"] == "file":
                code.append(f"\n\t// 添加文件 {key}")
                code.append(f"\tfile, err := os.Open(\"{value['path']}\")")
                code.append("\tif err != nil {")
                code.append("\t\tpanic(err)")
                code.append("\t}")
                code.append("\tdefer file.Close()")
                code.append(f"\tfw, err := w.CreateFormFile(\"{key}\", filepath.Base(\"{value['path']}\"))")
                code.append("\tif err != nil {")
                code.append("\t\tpanic(err)")
                code.append("\t}")
                code.append("\t_, err = io.Copy(fw, file)")
                code.append("\tif err != nil {")
                code.append("\t\tpanic(err)")
                code.append("\t}")
            else:
                code.append(f"\n\t// 添加表单字段 {key}")
                code.append(f"\tfw, err := w.CreateFormField(\"{key}\")")
                code.append("\tif err != nil {")
                code.append("\t\tpanic(err)")
                code.append("\t}")
                code.append(f"\t_, err = fw.Write([]byte(\"{value['value']}\"))")
                code.append("\tif err != nil {")
                code.append("\t\tpanic(err)")
                code.append("\t}")
        
        code.append("\n\t// 关闭multipart writer")
        code.append("\terr := w.Close()")
        code.append("\tif err != nil {")
        code.append("\t\tpanic(err)")
        code.append("\t}")
        code.append("\tpayload := &b")
    else:
        code.append("\n\t// 无请求体")
        code.append("\tvar payload io.Reader = nil")
    
    # 创建请求
    code.append(f"\n\t// 创建请求")
    code.append(f"\treq, err := http.NewRequest(\"{curl_dict['method']}\", \"{curl_dict['url']}\", payload)")
    code.append("\tif err != nil {")
    code.append("\t\tpanic(err)")
    code.append("\t}")
    
    # 设置headers
    if curl_dict["headers"]:
        code.append("\n\t// 设置请求头")
        for key, value in curl_dict["headers"].items():
            code.append(f"\treq.Header.Add(\"{key}\", \"{value}\")")
    
    # 如果是form_data，设置Content-Type
    if curl_dict["form_data"] is not None:
        code.append("\n\t// 设置Content-Type为multipart/form-data")
        code.append("\treq.Header.Set(\"Content-Type\", w.FormDataContentType())")
    
    # 设置basic auth
    if curl_dict["auth"] is not None and curl_dict["auth"]["type"] == "basic" and "username" in curl_dict["auth"]:
        code.append("\n\t// 设置Basic认证")
        code.append(f"\treq.SetBasicAuth(\"{curl_dict['auth']['username']}\", \"{curl_dict['auth']['password']}\")")
    
    # 设置cookies
    if "cookies" in curl_dict and curl_dict["cookies"]:
        code.append("\n\t// 设置Cookies")
        for key, value in curl_dict["cookies"].items():
            code.append(f"\treq.AddCookie(&http.Cookie{{Name: \"{key}\", Value: \"{value}\"}})")
    
    # 发送请求
    code.append("\n\t// 发送请求")
    code.append("\tres, err := client.Do(req)")
    code.append("\tif err != nil {")
    code.append("\t\tpanic(err)")
    code.append("\t}")
    code.append("\tdefer res.Body.Close()")
    
    # 读取响应
    code.append("\n\t// 读取响应")
    code.append("\tbody, err := ioutil.ReadAll(res.Body)")
    code.append("\tif err != nil {")
    code.append("\t\tpanic(err)")
    code.append("\t}")
    
    # 输出响应
    code.append("\n\t// 输出响应")
    code.append("\tfmt.Println(\"Status:\", res.Status)")
    code.append("\tfmt.Println(\"Response Headers:\", res.Header)")
    code.append("\tfmt.Println(\"Response Body:\", string(body))")
    
    code.append("}")
    
    return "\n".join(code)

def to_ruby(curl_dict):
    """将curl命令转换为Ruby代码"""
    if "error" in curl_dict:
        return f"# Error: {curl_dict['error']}"
    
    code = ["require 'net/http'", "require 'uri'", "require 'json'"]
    
    # 如果有文件上传，添加multipart库
    if curl_dict["form_data"] is not None:
        code.append("require 'net/http/post/multipart'")
    
    # 解析URL
    code.append(f"\n# 解析URL")
    code.append(f"uri = URI.parse('{curl_dict['url']}')")
    
    # 创建HTTP对象
    code.append("\n# 创建HTTP对象")
    code.append("http = Net::HTTP.new(uri.host, uri.port)")
    
    # 设置HTTPS
    if curl_dict["url"].startswith("https"):
        code.append("http.use_ssl = true")
        if not curl_dict["verify_ssl"]:
            code.append("http.verify_mode = OpenSSL::SSL::VERIFY_NONE")
    
    # 设置超时
    if curl_dict["timeout"] is not None:
        code.append(f"http.open_timeout = {curl_dict['timeout']}")
        code.append(f"http.read_timeout = {curl_dict['timeout']}")
    
    # 创建请求
    method = curl_dict["method"].capitalize()
    if method == "Get":
        req_class = "Net::HTTP::Get"
    elif method == "Post":
        req_class = "Net::HTTP::Post"
    elif method == "Put":
        req_class = "Net::HTTP::Put"
    elif method == "Delete":
        req_class = "Net::HTTP::Delete"
    elif method == "Patch":
        req_class = "Net::HTTP::Patch"
    elif method == "Head":
        req_class = "Net::HTTP::Head"
    elif method == "Options":
        req_class = "Net::HTTP::Options"
    else:
        req_class = f"Net::HTTP::{method}"
    
    # 处理表单数据
    if curl_dict["form_data"] is not None:
        code.append("\n# 创建multipart表单请求")
        code.append(f"request = {req_class}.new(uri)")
        
        # 添加表单数据
        code.append("\n# 添加表单数据")
        for key, value in curl_dict["form_data"].items():
            if value["type"] == "file":
                code.append(f"file_path = '{value['path']}'")
                code.append(f"file_name = File.basename(file_path)")
                code.append(f"file_data = File.open(file_path)")
                code.append(f"request.body = {")
                code.append(f"  '{key}' => UploadIO.new(file_data, 'application/octet-stream', file_name)")
                code.append("}")
            else:
                code.append(f"request.set_form_data('{key}' => '{value['value']}')")
    else:
        code.append("\n# 创建请求")
        code.append(f"request = {req_class}.new(uri)")
        
        # 处理请求体
        if curl_dict["data"] is not None:
            code.append("\n# 设置请求体")
            if isinstance(curl_dict["data"], dict):
                if curl_dict["headers"].get("Content-Type", "").lower() == "application/json":
                    code.append(f"request.body = {curl_dict['data']}.to_json")
                else:
                    # 使用URI.encode_www_form
                    form_data = []
                    for key, value in curl_dict["data"].items():
                        form_data.append(f"'{key}' => '{value}'")
                    code.append(f"request.body = URI.encode_www_form({{{', '.join(form_data)}}})")
            else:
                # 字符串形式的data
                code.append(f"request.body = '{curl_dict['data']}'")
    
    # 设置headers
    if curl_dict["headers"]:
        code.append("\n# 设置请求头")
        for key, value in curl_dict["headers"].items():
            code.append(f"request['{key}'] = '{value}'")
    
    # 设置basic auth
    if curl_dict["auth"] is not None and curl_dict["auth"]["type"] == "basic" and "username" in curl_dict["auth"]:
        code.append("\n# 设置Basic认证")
        code.append(f"request.basic_auth '{curl_dict['auth']['username']}', '{curl_dict['auth']['password']}'")
    
    # 设置cookies
    if "cookies" in curl_dict and curl_dict["cookies"]:
        code.append("\n# 设置Cookies")
        cookie_parts = []
        for key, value in curl_dict["cookies"].items():
            cookie_parts.append(f"{key}={value}")
        code.append(f"request['Cookie'] = '{'; '.join(cookie_parts)}'")
    
    # 发送请求
    code.append("\n# 发送请求")
    code.append("response = http.request(request)")
    
    # 输出响应
    code.append("\n# 输出响应")
    code.append("puts \"Status: #{response.code}\"")
    code.append("puts \"Headers: #{response.to_hash.inspect}\"")
    code.append("puts \"Body: #{response.body}\"")
    
    # 尝试解析JSON
    code.append("\n# 尝试解析JSON")
    code.append("begin")
    code.append("  json_response = JSON.parse(response.body)")
    code.append("  puts \"JSON: #{json_response}\"")
    code.append("rescue JSON::ParserError")
    code.append("  puts \"Response is not valid JSON\"")
    code.append("end")
    
    return "\n".join(code)
