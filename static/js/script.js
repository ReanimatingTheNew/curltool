document.addEventListener('DOMContentLoaded', function() {
    // 获取DOM元素 - Curl to JSON/Code
    const curlInput = document.getElementById('curlInput');
    const jsonOutput = document.getElementById('jsonOutput');
    const convertBtn = document.getElementById('convertBtn');
    const clearBtn = document.getElementById('clearBtn');
    const copyBtn = document.getElementById('copyBtn');
    const formatBtn = document.getElementById('formatBtn');
    const outputFormat = document.getElementById('outputFormat');
    const outputTitle = document.getElementById('outputTitle');
    
    // 获取DOM元素 - Code to Curl
    const codeInput = document.getElementById('codeInput');
    const curlOutput = document.getElementById('curlOutput');
    const convertCodeBtn = document.getElementById('convertCodeBtn');
    const clearCodeBtn = document.getElementById('clearCodeBtn');
    const copyCurlBtn = document.getElementById('copyCurlBtn');
    const codeLanguage = document.getElementById('codeLanguage');
    
    // 获取转换类型按钮
    const curlToJsonBtn = document.getElementById('curlToJsonBtn');
    const codeToCurlBtn = document.getElementById('codeToCurlBtn');
    const curlToJsonBox = document.getElementById('curl-to-json');
    const codeToCurlBox = document.getElementById('code-to-curl');
    
    // 获取示例下拉菜单
    const curlExamples = document.getElementById('curlExamples');
    const codeExamples = document.getElementById('codeExamples');
    
    // 获取所有选项卡按钮和内容
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');
    
    // 检查highlight.js是否加载
    if (typeof hljs !== 'undefined') {
        // 初始化代码高亮
        hljs.highlightAll();
    } else {
        console.error('highlight.js 未加载，等待加载完成...');
        // 尝试在稍后再初始化
        setTimeout(function() {
            if (typeof hljs !== 'undefined') {
                hljs.highlightAll();
            } else {
                console.error('highlight.js 仍然未加载，请检查脚本引用');
            }
        }, 1000);
    }
    
    // 输出格式选择变更事件
    outputFormat.addEventListener('change', function() {
        const format = outputFormat.value;
        // 更新输出标题
        if (format === 'json') {
            outputTitle.textContent = 'JSON Result';
            jsonOutput.className = 'json';
        } else {
            outputTitle.textContent = `${format.charAt(0).toUpperCase() + format.slice(1)} Code`;
            jsonOutput.className = format;
        }
        
        // 如果已经有转换结果，重新转换
        if (jsonOutput.textContent && jsonOutput.textContent !== '// 转换结果将显示在这里' && curlInput.value.trim()) {
            convertBtn.click();
        }
        
        // 安全地使用highlight.js
        if (typeof hljs !== 'undefined') {
            try {
                hljs.highlightElement(jsonOutput);
            } catch (e) {
                console.error('代码高亮失败:', e);
            }
        }
    });
    
    // Curl 转换按钮点击事件
    convertBtn.addEventListener('click', function() {
        const curlCommand = curlInput.value.trim();
        console.log('用户输入的curl命令:', curlCommand);
        
        if (!curlCommand) {
            showNotification('请输入curl命令', 'error');
            return;
        }
        
        const format = outputFormat.value;
        
        // 准备发送的数据
        const requestData = {
            curl: curlCommand
        };
        console.log('准备发送的数据:', requestData);
        
        // 根据选择的输出格式决定发送请求的API端点
        let apiUrl = '/api/convert';
        if (format !== 'json') {
            apiUrl = '/api/curl-to-code';
            requestData.language = format;
        }
        
        // 发送请求到后端API
        console.log(`发送请求到: ${apiUrl}`);
        fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        })
        .then(response => {
            console.log('收到响应状态:', response.status);
            if (!response.ok) {
                throw new Error('网络请求失败，状态码: ' + response.status);
            }
            return response.json();
        })
        .then(data => {
            console.log('收到响应数据类型:', typeof data);
            
            // 根据输出格式处理响应数据
            if (format === 'json') {
                // 格式化JSON并显示
                const formattedJson = JSON.stringify(data, null, 4);
                jsonOutput.textContent = formattedJson;
                jsonOutput.className = 'json';
            } else {
                // 显示代码
                if (data.code) {
                    jsonOutput.textContent = data.code;
                    jsonOutput.className = format;
                } else if (data.error) {
                    jsonOutput.textContent = `// Error: ${data.error}`;
                    showNotification('转换失败: ' + data.error, 'error');
                    return;
                } else {
                    jsonOutput.textContent = '// 无法解析响应数据';
                    showNotification('转换失败: 无法解析响应数据', 'error');
                    return;
                }
            }
            
            // 安全地使用highlight.js
            if (typeof hljs !== 'undefined') {
                try {
                    hljs.highlightElement(jsonOutput);
                } catch (e) {
                    console.error('代码高亮失败:', e);
                }
            }
            
            showNotification('转换成功', 'success');
        })
        .catch(error => {
            console.error('请求出错:', error);
            showNotification('转换失败: ' + error.message, 'error');
        });
    });
    
    // Code to Curl 转换按钮点击事件
    convertCodeBtn.addEventListener('click', function() {
        const code = codeInput.value.trim();
        const language = codeLanguage.value;
        console.log(`用户输入的${language}代码:`, code);
        
        if (!code) {
            showNotification('请输入代码', 'error');
            return;
        }
        
        // 准备发送的数据
        const requestData = {
            code: code,
            language: language
        };
        console.log('准备发送的数据:', requestData);
        
        // 发送请求到后端API
        console.log('发送请求到: /api/reverse');
        fetch('/api/reverse', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        })
        .then(response => {
            console.log('收到响应状态:', response.status);
            if (!response.ok) {
                throw new Error('网络请求失败，状态码: ' + response.status);
            }
            return response.json();
        })
        .then(data => {
            console.log('收到响应数据:', data);
            
            if (!data.success) {
                showNotification('转换失败: ' + data.message, 'error');
                return;
            }
            
            // 显示curl命令
            curlOutput.textContent = data.command;
            
            // 安全地使用highlight.js
            if (typeof hljs !== 'undefined') {
                try {
                    hljs.highlightElement(curlOutput);
                } catch (e) {
                    console.error('代码高亮失败:', e);
                }
            }
            
            showNotification('转换成功', 'success');
        })
        .catch(error => {
            console.error('请求出错:', error);
            showNotification('转换失败: ' + error.message, 'error');
        });
    });
    
    // Curl to JSON 清除按钮点击事件
    clearBtn.addEventListener('click', function() {
        curlInput.value = '';
        jsonOutput.textContent = '// 转换结果将显示在这里';
        
        // 安全地使用highlight.js
        if (typeof hljs !== 'undefined') {
            try {
                hljs.highlightElement(jsonOutput);
            } catch (e) {
                console.error('代码高亮失败:', e);
            }
        }
    });
    
    // Code to Curl 清除按钮点击事件
    clearCodeBtn.addEventListener('click', function() {
        codeInput.value = '';
        curlOutput.textContent = '// Curl命令将显示在这里';
        
        // 安全地使用highlight.js
        if (typeof hljs !== 'undefined') {
            try {
                hljs.highlightElement(curlOutput);
            } catch (e) {
                console.error('代码高亮失败:', e);
            }
        }
    });
    
    // Curl to JSON 复制按钮点击事件
    copyBtn.addEventListener('click', function() {
        const text = jsonOutput.textContent;
        
        if (text && text !== '// 转换结果将显示在这里') {
            navigator.clipboard.writeText(text)
                .then(() => {
                    showNotification('已复制到剪贴板', 'success');
                })
                .catch(err => {
                    console.error('复制失败:', err);
                    showNotification('复制失败', 'error');
                });
        } else {
            showNotification('没有内容可复制', 'error');
        }
    });
    
    // Code to Curl 复制按钮点击事件
    copyCurlBtn.addEventListener('click', function() {
        const text = curlOutput.textContent;
        
        if (text && text !== '// Curl命令将显示在这里') {
            navigator.clipboard.writeText(text)
                .then(() => {
                    showNotification('已复制到剪贴板', 'success');
                })
                .catch(err => {
                    console.error('复制失败:', err);
                    showNotification('复制失败', 'error');
                });
        } else {
            showNotification('没有内容可复制', 'error');
        }
    });
    
    
    // 格式化按钮点击事件
    formatBtn.addEventListener('click', function() {
        const text = jsonOutput.textContent;
        
        if (text && text !== '// 转换结果将显示在这里') {
            try {
                const json = JSON.parse(text);
                const formattedJson = JSON.stringify(json, null, 4);
                jsonOutput.textContent = formattedJson;
                
                // 安全地使用highlight.js
                if (typeof hljs !== 'undefined') {
                    try {
                        hljs.highlightElement(jsonOutput);
                    } catch (e) {
                        console.error('代码高亮失败:', e);
                    }
                }
                
                showNotification('格式化成功', 'success');
            } catch (error) {
                console.error('格式化失败:', error);
                showNotification('无效的JSON格式', 'error');
            }
        } else {
            showNotification('没有内容可格式化', 'error');
        }
    });
    
    // 转换类型切换功能
    curlToJsonBtn.addEventListener('click', function() {
        curlToJsonBtn.classList.add('active');
        codeToCurlBtn.classList.remove('active');
        curlToJsonBox.classList.add('active');
        codeToCurlBox.classList.remove('active');
    });
    
    codeToCurlBtn.addEventListener('click', function() {
        codeToCurlBtn.classList.add('active');
        curlToJsonBtn.classList.remove('active');
        codeToCurlBox.classList.add('active');
        curlToJsonBox.classList.remove('active');
    });
    
    // 选项卡切换功能
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // 获取当前选项卡组
            const tabGroup = this.closest('.tab-buttons').nextElementSibling;
            const tabPanes = tabGroup.querySelectorAll('.tab-pane');
            const tabBtns = this.closest('.tab-buttons').querySelectorAll('.tab-btn');
            
            // 移除所有活动状态
            tabBtns.forEach(b => b.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('active'));
            
            // 添加当前活动状态
            this.classList.add('active');
            const tabId = this.getAttribute('data-tab');
            tabGroup.querySelector('#' + tabId).classList.add('active');
        });
    });
    
    // 预设curl示例功能
    curlExamples.addEventListener('change', function() {
        if (this.value) {
            curlInput.value = this.value;
        }
    });
    
    // 预设代码示例功能
    const codeExamplesMap = {
        'python-get': `import requests

response = requests.get('https://api.example.com/users')
print(response.json())`,
        
        'python-post': `import requests

url = 'https://api.example.com/users'
headers = {'Content-Type': 'application/json'}
data = {'name': 'John', 'email': 'john@example.com'}

response = requests.post(url, headers=headers, json=data)
print(response.json())`,
        
        'javascript-fetch': `fetch('https://api.example.com/users', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        name: 'John',
        email: 'john@example.com'
    })
})
.then(response => response.json())
.then(data => console.log(data))`,
        
        'javascript-axios': `axios.post('https://api.example.com/users', {
    name: 'John',
    email: 'john@example.com'
}, {
    headers: {
        'Content-Type': 'application/json'
    }
})
.then(response => console.log(response.data))`,
        
        'php-curl': `<?php
$ch = curl_init();

curl_setopt($ch, CURLOPT_URL, 'https://api.example.com/users');
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode(array(
    'name' => 'John',
    'email' => 'john@example.com'
)));

$response = curl_exec($ch);
curl_close($ch);

echo $response;
?>`
    };
    
    codeExamples.addEventListener('change', function() {
        if (this.value && codeExamplesMap[this.value]) {
            codeInput.value = codeExamplesMap[this.value];
            
            // 自动选择对应的语言
            if (this.value.startsWith('python')) {
                codeLanguage.value = 'python';
            } else if (this.value.startsWith('javascript')) {
                codeLanguage.value = 'javascript';
            } else if (this.value.startsWith('php')) {
                codeLanguage.value = 'php';
            }
        }
    });
    
    // 显示通知函数
    function showNotification(message, type) {
        // 移除现有通知
        const existingNotification = document.querySelector('.notification');
        if (existingNotification) {
            existingNotification.remove();
        }
        
        // 创建新通知
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        document.body.appendChild(notification);
        
        // 显示通知
        setTimeout(() => {
            notification.classList.add('show');
        }, 10);
        
        // 自动隐藏通知
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }
});
