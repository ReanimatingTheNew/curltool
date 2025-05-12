document.addEventListener('DOMContentLoaded', function() {
    // 页面导航切换
    const navLinks = document.querySelectorAll('.main-nav a');
    const tabContents = document.querySelectorAll('.tab-content');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // 移除所有活动状态
            navLinks.forEach(l => l.classList.remove('active'));
            tabContents.forEach(tab => tab.classList.remove('active'));
            
            // 添加当前活动状态
            this.classList.add('active');
            
            // 显示对应的内容区域
            const tabId = this.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });
    
    // 转换器面板切换
    const tabButtons = document.querySelectorAll('.tab-btn');
    const converterPanels = document.querySelectorAll('.converter-panel');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            // 移除所有活动状态
            tabButtons.forEach(btn => btn.classList.remove('active'));
            converterPanels.forEach(panel => panel.classList.remove('active'));
            
            // 添加当前活动状态
            this.classList.add('active');
            
            // 显示对应的转换器面板
            const panelId = this.getAttribute('data-converter');
            document.getElementById(panelId).classList.add('active');
        });
    });
    
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
    
    // Curl转换功能
    const curlInput = document.getElementById('curlInput');
    const jsonOutput = document.getElementById('jsonOutput');
    const convertBtn = document.getElementById('convertBtn');
    const clearBtn = document.getElementById('clearBtn');
    const copyBtn = document.getElementById('copyBtn');
    const formatBtn = document.getElementById('formatBtn');
    const outputFormat = document.getElementById('outputFormat');
    const outputTitle = document.getElementById('outputTitle');
    const curlExamples = document.getElementById('curlExamples');
    
    // 设置示例
    curlExamples.addEventListener('change', function() {
        if (this.value) {
            // 直接设置值，不进行额外处理
            curlInput.value = this.value;
        }
        this.selectedIndex = 0; // 重置选择
    });
    
    // 清除按钮
    clearBtn.addEventListener('click', function() {
        curlInput.value = '';
        jsonOutput.textContent = '// 转换结果将显示在这里';
        jsonOutput.className = 'json';
        hljs.highlightElement(jsonOutput);
    });
    
    // 复制按钮
    copyBtn.addEventListener('click', function() {
        const textToCopy = jsonOutput.textContent;
        navigator.clipboard.writeText(textToCopy)
            .then(() => {
                // 显示复制成功提示
                const originalText = this.textContent;
                this.textContent = '已复制!';
                setTimeout(() => {
                    this.textContent = originalText;
                }, 2000);
            })
            .catch(err => {
                console.error('复制失败:', err);
            });
    });
    
    // 格式化按钮
    formatBtn.addEventListener('click', function() {
        try {
            // 尝试解析JSON并格式化
            if (jsonOutput.className.includes('json')) {
                const jsonObj = JSON.parse(jsonOutput.textContent);
                jsonOutput.textContent = JSON.stringify(jsonObj, null, 2);
                hljs.highlightElement(jsonOutput);
            }
        } catch (error) {
            console.error('格式化失败:', error);
        }
    });
    
    // 转换按钮
    convertBtn.addEventListener('click', function() {
        const curlCommand = curlInput.value.trim();
        console.log('用户输入的curl命令:', curlCommand);
        
        if (!curlCommand) {
            showNotification('请输入curl命令', 'error');
            return;
        }
        
        // 显示加载状态
        convertBtn.disabled = true;
        convertBtn.textContent = '转换中...';
        
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
                outputTitle.textContent = 'JSON结果';
            } else {
                // 显示代码
                outputTitle.textContent = `${format.toUpperCase()} 代码`;
                if (data.code) {
                    jsonOutput.textContent = data.code;
                    jsonOutput.className = format;
                } else if (data.error) {
                    jsonOutput.textContent = `// Error: ${data.error}`;
                    showNotification('转换失败: ' + data.error, 'error');
                    convertBtn.disabled = false;
                    convertBtn.textContent = '转换';
                    return;
                } else {
                    jsonOutput.textContent = '// 无法解析响应数据';
                    showNotification('转换失败: 无法解析响应数据', 'error');
                    convertBtn.disabled = false;
                    convertBtn.textContent = '转换';
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
            
            // 恢复按钮状态
            convertBtn.disabled = false;
            convertBtn.textContent = '转换';
        })
        .catch(error => {
            console.error('请求出错:', error);
            showNotification('转换失败: ' + error.message, 'error');
            jsonOutput.textContent = '转换失败，请检查您的curl命令是否正确。';
            
            // 恢复按钮状态
            convertBtn.disabled = false;
            convertBtn.textContent = '转换';
        });
    });
    
    // 代码转Curl功能
    const codeInput = document.getElementById('codeInput');
    const curlOutput = document.getElementById('curlOutput');
    const convertCodeBtn = document.getElementById('convertCodeBtn');
    const clearCodeBtn = document.getElementById('clearCodeBtn');
    const copyCurlBtn = document.getElementById('copyCurlBtn');
    const codeLanguage = document.getElementById('codeLanguage');
    const codeExamples = document.getElementById('codeExamples');
    
    // 代码示例
    const codeExamplesData = {
        'python-get': `import requests

response = requests.get('https://api.example.com/users')
print(response.json())`,
        'python-post': `import requests

headers = {
    'Content-Type': 'application/json',
}

data = {
    'name': 'John',
    'email': 'john@example.com'
}

response = requests.post('https://api.example.com/users', headers=headers, json=data)
print(response.json())`,
        'javascript-fetch': `fetch('https://api.example.com/users', {
  method: 'GET',
  headers: {
    'Accept': 'application/json'
  }
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));`,
        'javascript-axios': `axios.get('https://api.example.com/users')
  .then(response => {
    console.log(response.data);
  })
  .catch(error => {
    console.error('Error:', error);
  });`,
        'php-curl': `<?php
$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://api.example.com/users",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_HTTPHEADER => [
    "Accept: application/json"
  ],
]);

$response = curl_exec($curl);
$err = curl_error($curl);

curl_close($curl);

if ($err) {
  echo "cURL Error #:" . $err;
} else {
  echo $response;
}
?>`
    };
    
    // 设置代码示例
    codeExamples.addEventListener('change', function() {
        if (this.value && codeExamplesData[this.value]) {
            codeInput.value = codeExamplesData[this.value];
            
            // 自动选择对应的语言
            if (this.value.startsWith('python')) {
                codeLanguage.value = 'python';
            } else if (this.value.startsWith('javascript')) {
                codeLanguage.value = 'javascript';
            } else if (this.value.startsWith('php')) {
                codeLanguage.value = 'php';
            }
        }
        this.selectedIndex = 0; // 重置选择
    });
    
    // 清除代码按钮
    clearCodeBtn.addEventListener('click', function() {
        codeInput.value = '';
        curlOutput.textContent = '// Curl命令将显示在这里';
        hljs.highlightElement(curlOutput);
    });
    
    // 复制Curl按钮
    copyCurlBtn.addEventListener('click', function() {
        const textToCopy = curlOutput.textContent;
        navigator.clipboard.writeText(textToCopy)
            .then(() => {
                // 显示复制成功提示
                const originalText = this.textContent;
                this.textContent = '已复制!';
                setTimeout(() => {
                    this.textContent = originalText;
                }, 2000);
            })
            .catch(err => {
                console.error('复制失败:', err);
            });
    });
    
    // 代码转Curl按钮
    convertCodeBtn.addEventListener('click', function() {
        const code = codeInput.value.trim();
        const language = codeLanguage.value;
        console.log(`用户输入的${language}代码:`, code);
        
        if (!code) {
            showNotification('请输入代码', 'error');
            return;
        }
        
        // 显示加载状态
        convertCodeBtn.disabled = true;
        convertCodeBtn.textContent = '转换中...';
        
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
                showNotification('转换失败: ' + (data.message || '未知错误'), 'error');
                curlOutput.textContent = '转换失败，请检查您的代码是否正确。';
                convertCodeBtn.disabled = false;
                convertCodeBtn.textContent = '转换';
                return;
            }
            
            // 显示curl命令
            curlOutput.textContent = data.command;
            curlOutput.className = 'bash';
            
            // 安全地使用highlight.js
            if (typeof hljs !== 'undefined') {
                try {
                    hljs.highlightElement(curlOutput);
                } catch (e) {
                    console.error('代码高亮失败:', e);
                }
            }
            
            showNotification('转换成功', 'success');
            
            // 恢复按钮状态
            convertCodeBtn.disabled = false;
            convertCodeBtn.textContent = '转换';
        })
        .catch(error => {
            console.error('请求出错:', error);
            showNotification('转换失败: ' + error.message, 'error');
            curlOutput.textContent = '转换失败，请检查您的代码是否正确。';
            
            // 恢复按钮状态
            convertCodeBtn.disabled = false;
            convertCodeBtn.textContent = '转换';
        });
    });
    
    // 初始化代码高亮
    document.querySelectorAll('pre code').forEach(block => {
        hljs.highlightElement(block);
    });
    
    // 显示通知函数
    function showNotification(message, type) {
        // 创建通知元素
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        
        // 添加到页面
        document.body.appendChild(notification);
        
        // 显示动画
        setTimeout(() => {
            notification.classList.add('show');
        }, 10);
        
        // 自动消失
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
});
