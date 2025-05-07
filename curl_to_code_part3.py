"""
curl命令转换为Java和C#代码的模块
"""

def to_java(curl_dict):
    """将curl命令转换为Java代码"""
    if "error" in curl_dict:
        return f"// Error: {curl_dict['error']}"
    
    code = [
        "import java.io.*;",
        "import java.net.HttpURLConnection;",
        "import java.net.URL;",
        "import java.nio.charset.StandardCharsets;",
        "import java.util.HashMap;",
        "import java.util.Map;",
        "import java.util.Scanner;",
        "import javax.net.ssl.HttpsURLConnection;",
        "import javax.net.ssl.SSLContext;",
        "import javax.net.ssl.TrustManager;",
        "import javax.net.ssl.X509TrustManager;",
        "import java.security.cert.X509Certificate;",
        "",
        "public class CurlRequest {",
        "    public static void main(String[] args) {",
        "        try {"
    ]
    
    # 禁用SSL验证（如果需要）
    if not curl_dict["verify_ssl"]:
        code.append("            // 禁用SSL验证")
        code.append("            TrustManager[] trustAllCerts = new TrustManager[] {")
        code.append("                new X509TrustManager() {")
        code.append("                    public X509Certificate[] getAcceptedIssuers() { return null; }")
        code.append("                    public void checkClientTrusted(X509Certificate[] certs, String authType) { }")
        code.append("                    public void checkServerTrusted(X509Certificate[] certs, String authType) { }")
        code.append("                }")
        code.append("            };")
        code.append("            SSLContext sc = SSLContext.getInstance(\"SSL\");")
        code.append("            sc.init(null, trustAllCerts, new java.security.SecureRandom());")
        code.append("            HttpsURLConnection.setDefaultSSLSocketFactory(sc.getSocketFactory());")
        code.append("            HttpsURLConnection.setDefaultHostnameVerifier((hostname, session) -> true);")
    
    # 创建URL连接
    code.append(f"            // 创建URL连接")
    code.append(f"            URL url = new URL(\"{curl_dict['url']}\");")
    code.append(f"            HttpURLConnection connection = (HttpURLConnection) url.openConnection();")
    
    # 设置请求方法
    code.append(f"            // 设置请求方法")
    code.append(f"            connection.setRequestMethod(\"{curl_dict['method']}\");")
    
    # 设置超时
    if curl_dict["timeout"] is not None:
        timeout_ms = int(curl_dict["timeout"] * 1000)
        code.append(f"            // 设置超时")
        code.append(f"            connection.setConnectTimeout({timeout_ms});")
        code.append(f"            connection.setReadTimeout({timeout_ms});")
    
    # 设置是否自动重定向
    if not curl_dict["allow_redirects"]:
        code.append(f"            // 禁用自动重定向")
        code.append(f"            connection.setInstanceFollowRedirects(false);")
    
    # 设置headers
    if curl_dict["headers"]:
        code.append(f"            // 设置请求头")
        for key, value in curl_dict["headers"].items():
            code.append(f"            connection.setRequestProperty(\"{key}\", \"{value}\");")
    
    # 设置cookies
    if "cookies" in curl_dict and curl_dict["cookies"]:
        code.append(f"            // 设置Cookies")
        cookie_parts = []
        for key, value in curl_dict["cookies"].items():
            cookie_parts.append(f"{key}={value}")
        code.append(f"            connection.setRequestProperty(\"Cookie\", \"{'; '.join(cookie_parts)}\");")
    
    # 设置basic auth
    if curl_dict["auth"] is not None and curl_dict["auth"]["type"] == "basic" and "username" in curl_dict["auth"]:
        code.append(f"            // 设置Basic认证")
        code.append(f"            String auth = \"{curl_dict['auth']['username']}:{curl_dict['auth']['password']}\";")
        code.append(f"            String encodedAuth = java.util.Base64.getEncoder().encodeToString(auth.getBytes(StandardCharsets.UTF_8));")
        code.append(f"            connection.setRequestProperty(\"Authorization\", \"Basic \" + encodedAuth);")
    
    # 设置请求体
    if curl_dict["data"] is not None or curl_dict["form_data"] is not None:
        code.append(f"            // 设置输出")
        code.append(f"            connection.setDoOutput(true);")
        
        if curl_dict["data"] is not None:
            code.append(f"            // 设置请求体")
            if isinstance(curl_dict["data"], dict):
                if curl_dict["headers"].get("Content-Type", "").lower() == "application/json":
                    # 构建JSON
                    json_str = "{"
                    for i, (key, value) in enumerate(curl_dict["data"].items()):
                        if isinstance(value, str):
                            json_str += f"\\\"{key}\\\": \\\"{value}\\\""
                        else:
                            json_str += f"\\\"{key}\\\": {value}"
                        if i < len(curl_dict["data"]) - 1:
                            json_str += ", "
                    json_str += "}"
                    code.append(f"            String jsonInputString = \"{json_str}\";")
                    code.append("            try (OutputStream os = connection.getOutputStream()) {")
                    code.append("                byte[] input = jsonInputString.getBytes(StandardCharsets.UTF_8);")
                    code.append("                os.write(input, 0, input.length);")
                    code.append("            }")
                else:
                    # 构建表单数据
                    form_parts = []
                    for key, value in curl_dict["data"].items():
                        form_parts.append(f"{key}={value}")
                    form_data = "&".join(form_parts)
                    code.append(f"            String formData = \"{form_data}\";")
                    code.append("            try (OutputStream os = connection.getOutputStream()) {")
                    code.append(f"                byte[] input = formData.getBytes(StandardCharsets.UTF_8);")
                    code.append("                os.write(input, 0, input.length);")
                    code.append("            }")
            else:
                # 字符串形式的data
                code.append(f"            String data = \"{curl_dict['data']}\";")
                code.append("            try (OutputStream os = connection.getOutputStream()) {")
                code.append("                byte[] input = data.getBytes(StandardCharsets.UTF_8);")
                code.append("                os.write(input, 0, input.length);")
                code.append("            }")
        elif curl_dict["form_data"] is not None:
            code.append(f"            // 设置multipart表单数据")
            code.append(f"            String boundary = \"----WebKitFormBoundary7MA4YWxkTrZu0gW\";")
            code.append(f"            connection.setRequestProperty(\"Content-Type\", \"multipart/form-data; boundary=\" + boundary);")
            code.append("            try (OutputStream os = connection.getOutputStream()) {")
            code.append("                PrintWriter writer = new PrintWriter(new OutputStreamWriter(os, StandardCharsets.UTF_8), true);")
            
            for key, value in curl_dict["form_data"].items():
                code.append(f"                // 添加表单项 {key}")
                code.append("                writer.append(\"--\" + boundary).append(\"\\r\\n\");")
                
                if value["type"] == "file":
                    file_name = value["path"].split("/")[-1]
                    code.append(f"                writer.append(\"Content-Disposition: form-data; name=\\\"{key}\\\"; filename=\\\"{file_name}\\\"\").append(\"\\r\\n\");")
                    code.append(f"                writer.append(\"Content-Type: application/octet-stream\").append(\"\\r\\n\");")
                    code.append(f"                writer.append(\"\\r\\n\");")
                    code.append(f"                writer.flush();")
                    code.append(f"                // 注意：在实际应用中，您需要读取文件内容并写入")
                    code.append(f"                // 这里仅作为示例")
                    code.append(f"                try (FileInputStream fis = new FileInputStream(\"{value['path']}\")) {")
                    code.append(f"                    byte[] buffer = new byte[1024];")
                    code.append(f"                    int length;")
                    code.append(f"                    while ((length = fis.read(buffer)) > 0) {")
                    code.append(f"                        os.write(buffer, 0, length);")
                    code.append(f"                    }")
                    code.append(f"                    os.flush();")
                    code.append(f"                }")
                    code.append(f"                writer.append(\"\\r\\n\");")
                else:
                    code.append(f"                writer.append(\"Content-Disposition: form-data; name=\\\"{key}\\\"\").append(\"\\r\\n\");")
                    code.append(f"                writer.append(\"\\r\\n\");")
                    code.append(f"                writer.append(\"{value['value']}\").append(\"\\r\\n\");")
            
            code.append(f"                writer.append(\"--\" + boundary + \"--\").append(\"\\r\\n\");")
            code.append(f"                writer.flush();")
            code.append(f"            }")
    
    # 获取响应
    code.append(f"            // 获取响应")
    code.append(f"            int responseCode = connection.getResponseCode();")
    code.append(f"            System.out.println(\"Response Code: \" + responseCode);")
    code.append(f"            ")
    code.append(f"            // 获取响应头")
    code.append(f"            Map<String, String> responseHeaders = new HashMap<>();")
    code.append(f"            for (int i = 0; ; i++) {")
    code.append(f"                String headerName = connection.getHeaderFieldKey(i);")
    code.append(f"                String headerValue = connection.getHeaderField(i);")
    code.append(f"                if (headerName == null && headerValue == null) {")
    code.append(f"                    break;")
    code.append(f"                }")
    code.append(f"                if (headerName != null) {")
    code.append(f"                    responseHeaders.put(headerName, headerValue);")
    code.append(f"                }")
    code.append(f"            }")
    code.append(f"            System.out.println(\"Response Headers: \" + responseHeaders);")
    code.append(f"            ")
    code.append(f"            // 读取响应内容")
    code.append(f"            StringBuilder response = new StringBuilder();")
    code.append(f"            try (Scanner scanner = new Scanner(")
    code.append(f"                    responseCode >= 400 ? connection.getErrorStream() : connection.getInputStream())) {")
    code.append(f"                while (scanner.hasNextLine()) {")
    code.append(f"                    response.append(scanner.nextLine());")
    code.append(f"                }")
    code.append(f"            }")
    code.append(f"            System.out.println(\"Response Body: \" + response.toString());")
    
    # 关闭连接
    code.append(f"            // 关闭连接")
    code.append(f"            connection.disconnect();")
    
    # 异常处理
    code.append(f"        }} catch (Exception e) {{")
    code.append(f"            e.printStackTrace();")
    code.append(f"        }}")
    code.append(f"    }}")
    code.append(f"}}")
    
    return "\n".join(code)

def to_csharp(curl_dict):
    """将curl命令转换为C#代码"""
    if "error" in curl_dict:
        return f"// Error: {curl_dict['error']}"
    
    code = [
        "using System;",
        "using System.Collections.Generic;",
        "using System.IO;",
        "using System.Net;",
        "using System.Net.Http;",
        "using System.Net.Http.Headers;",
        "using System.Text;",
        "using System.Threading.Tasks;",
        "using Newtonsoft.Json;",
        "",
        "class Program",
        "{",
        "    static async Task Main(string[] args)",
        "    {"
    ]
    
    # 创建HttpClientHandler
    code.append("        // 创建HttpClientHandler")
    code.append("        var handler = new HttpClientHandler();")
    
    # 设置是否自动重定向
    if not curl_dict["allow_redirects"]:
        code.append("        // 禁用自动重定向")
        code.append("        handler.AllowAutoRedirect = false;")
    
    # 设置是否验证SSL
    if not curl_dict["verify_ssl"]:
        code.append("        // 禁用SSL验证")
        code.append("        handler.ServerCertificateCustomValidationCallback = (message, cert, chain, errors) => true;")
    
    # 设置cookies
    if "cookies" in curl_dict and curl_dict["cookies"]:
        code.append("        // 设置Cookies")
        code.append("        handler.CookieContainer = new CookieContainer();")
        for key, value in curl_dict["cookies"].items():
            code.append(f"        handler.CookieContainer.Add(new Uri(\"{curl_dict['url']}\"), new Cookie(\"{key}\", \"{value}\"));")
    
    # 创建HttpClient
    code.append("        // 创建HttpClient")
    code.append("        using (var client = new HttpClient(handler))")
    code.append("        {")
    
    # 设置超时
    if curl_dict["timeout"] is not None:
        timeout_ms = int(curl_dict["timeout"] * 1000)
        code.append(f"            // 设置超时")
        code.append(f"            client.Timeout = TimeSpan.FromMilliseconds({timeout_ms});")
    
    # 设置headers
    if curl_dict["headers"]:
        code.append("            // 设置请求头")
        for key, value in curl_dict["headers"].items():
            # 跳过Content-Type，因为它会在后面设置
            if key.lower() != "content-type":
                code.append(f"            client.DefaultRequestHeaders.Add(\"{key}\", \"{value}\");")
    
    # 设置basic auth
    if curl_dict["auth"] is not None and curl_dict["auth"]["type"] == "basic" and "username" in curl_dict["auth"]:
        code.append("            // 设置Basic认证")
        code.append(f"            var authToken = Encoding.ASCII.GetBytes(\"{curl_dict['auth']['username']}:{curl_dict['auth']['password']}\");")
        code.append(f"            client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue(\"Basic\", Convert.ToBase64String(authToken));")
    
    # 创建请求消息
    code.append("            // 创建请求消息")
    code.append(f"            var request = new HttpRequestMessage(new HttpMethod(\"{curl_dict['method']}\"), \"{curl_dict['url']}\");")
    
    # 设置请求体
    if curl_dict["data"] is not None:
        code.append("            // 设置请求体")
        if isinstance(curl_dict["data"], dict):
            if curl_dict["headers"].get("Content-Type", "").lower() == "application/json":
                # 构建JSON
                code.append("            var jsonData = new Dictionary<string, object>()")
                code.append("            {")
                for key, value in curl_dict["data"].items():
                    if isinstance(value, str):
                        code.append(f"                {{ \"{key}\", \"{value}\" }},")
                    else:
                        code.append(f"                {{ \"{key}\", {value} }},")
                code.append("            };")
                code.append("            var jsonContent = JsonConvert.SerializeObject(jsonData);")
                code.append("            var content = new StringContent(jsonContent, Encoding.UTF8, \"application/json\");")
                code.append("            request.Content = content;")
            else:
                # 构建表单数据
                code.append("            var formData = new Dictionary<string, string>()")
                code.append("            {")
                for key, value in curl_dict["data"].items():
                    code.append(f"                {{ \"{key}\", \"{value}\" }},")
                code.append("            };")
                code.append("            var content = new FormUrlEncodedContent(formData);")
                code.append("            request.Content = content;")
        else:
            # 字符串形式的data
            content_type = curl_dict["headers"].get("Content-Type", "text/plain")
            code.append(f"            var content = new StringContent(\"{curl_dict['data']}\", Encoding.UTF8, \"{content_type}\");")
            code.append("            request.Content = content;")
    
    # 设置表单数据
    elif curl_dict["form_data"] is not None:
        code.append("            // 设置multipart表单数据")
        code.append("            var multipartContent = new MultipartFormDataContent();")
        
        for key, value in curl_dict["form_data"].items():
            if value["type"] == "file":
                file_name = value["path"].split("/")[-1]
                code.append(f"            // 添加文件 {key}")
                code.append(f"            var fileContent = new ByteArrayContent(File.ReadAllBytes(\"{value['path']}\"));")
                code.append(f"            fileContent.Headers.ContentType = MediaTypeHeaderValue.Parse(\"application/octet-stream\");")
                code.append(f"            multipartContent.Add(fileContent, \"{key}\", \"{file_name}\");")
            else:
                code.append(f"            // 添加表单字段 {key}")
                code.append(f"            var stringContent = new StringContent(\"{value['value']}\");")
                code.append(f"            multipartContent.Add(stringContent, \"{key}\");")
        
        code.append("            request.Content = multipartContent;")
    
    # 发送请求
    code.append("            // 发送请求")
    code.append("            try")
    code.append("            {")
    code.append("                var response = await client.SendAsync(request);")
    code.append("                ")
    code.append("                // 获取响应状态码")
    code.append("                Console.WriteLine($\"Status Code: {(int)response.StatusCode} {response.StatusCode}\");")
    code.append("                ")
    code.append("                // 获取响应头")
    code.append("                Console.WriteLine(\"Response Headers:\");")
    code.append("                foreach (var header in response.Headers)")
    code.append("                {")
    code.append("                    Console.WriteLine($\"{header.Key}: {string.Join(\", \", header.Value)}\");")
    code.append("                }")
    code.append("                ")
    code.append("                // 获取响应内容")
    code.append("                var responseContent = await response.Content.ReadAsStringAsync();")
    code.append("                Console.WriteLine(\"Response Body:\");")
    code.append("                Console.WriteLine(responseContent);")
    code.append("                ")
    code.append("                // 尝试解析JSON")
    code.append("                try")
    code.append("                {")
    code.append("                    var jsonObj = JsonConvert.DeserializeObject(responseContent);")
    code.append("                    Console.WriteLine(\"JSON Response:\");")
    code.append("                    Console.WriteLine(JsonConvert.SerializeObject(jsonObj, Formatting.Indented));")
    code.append("                }")
    code.append("                catch (JsonException)")
    code.append("                {")
    code.append("                    Console.WriteLine(\"Response is not valid JSON\");")
    code.append("                }")
    code.append("            }")
    code.append("            catch (Exception ex)")
    code.append("            {")
    code.append("                Console.WriteLine($\"Error: {ex.Message}\");")
    code.append("            }")
    code.append("        }")
    code.append("    }")
    code.append("}")
    
    return "\n".join(code)
