document.addEventListener('DOMContentLoaded', function() {
    // Page navigation switching - only for links with data-tab attribute
    const tabNavLinks = document.querySelectorAll('.main-nav a[data-tab]');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabNavLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // 移除所有活动状态
            tabNavLinks.forEach(l => l.classList.remove('active'));
            tabContents.forEach(tab => tab.classList.remove('active'));
            
            // 添加当前活动状态
            this.classList.add('active');
            
            // Show corresponding content area
            const tabId = this.getAttribute('data-tab');
            const tabElement = document.getElementById(tabId);
            if (tabElement) {
                tabElement.classList.add('active');
            }
        });
    });
    
    // Highlight current navigation item
    const currentPath = window.location.pathname;
    document.querySelectorAll('.main-nav a').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
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
    
    // 复制输入区域按钮
    const copyInputBtn = document.getElementById('copyInputBtn');
    if (copyInputBtn) {
        copyInputBtn.addEventListener('click', function() {
            const textToCopy = curlInput.value;
            navigator.clipboard.writeText(textToCopy)
                .then(() => {
                    // 显示复制成功提示
                    const originalText = this.textContent;
                    this.textContent = 'Copied!';
                    setTimeout(() => {
                        this.textContent = originalText;
                    }, 2000);
                })
                .catch(err => {
                    console.error('Copy failed:', err);
                });
        });
    }
    
    // 清除按钮
    clearBtn.addEventListener('click', function() {
        curlInput.value = '';
        jsonOutput.textContent = '// Conversion result will be displayed here';
        jsonOutput.className = 'json';
    });
    
    // 复制按钮
    copyBtn.addEventListener('click', function() {
        const textToCopy = jsonOutput.textContent;
        navigator.clipboard.writeText(textToCopy)
            .then(() => {
                // 显示复制成功提示
                const originalText = this.textContent;
                this.textContent = 'Copied!';
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
            }
        } catch (error) {
            console.error('Format failed:', error);
        }
    });
    
    // 转换按钮
    convertBtn.addEventListener('click', function() {
        const curlCommand = curlInput.value.trim();
        console.log('User input curl command:', curlCommand);
        
        if (!curlCommand) {
            showNotification('Please enter a curl command', 'error');
            return;
        }
        
        // 显示加载状态
        convertBtn.disabled = true;
        convertBtn.textContent = 'Converting...';
        
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
                outputTitle.textContent = 'JSON Result';
            } else {
                // Display the language
                outputTitle.textContent = `${format.toUpperCase()}`;
                if (data.code) {
                    jsonOutput.textContent = data.code;
                    jsonOutput.className = format;
                } else if (data.error) {
                    jsonOutput.textContent = `// Error: ${data.error}`;
                    showNotification('Conversion failed: ' + data.error, 'error');
                    convertBtn.disabled = false;
                    convertBtn.textContent = 'Convert';
                    return;
                } else {
                    jsonOutput.textContent = '// Unable to parse response data';
                    showNotification('Conversion failed: Unable to parse response data', 'error');
                    convertBtn.disabled = false;
                    convertBtn.textContent = 'Convert';
                    return;
                }
            }
            
            showNotification('Conversion successful', 'success');
            
            // 恢复按钮状态
            convertBtn.disabled = false;
            convertBtn.textContent = 'Convert';
        })
        .catch(error => {
            console.error('Request error:', error);
            showNotification('Conversion failed: ' + error.message, 'error');
            jsonOutput.textContent = 'Conversion failed. Please check if your curl command is correct.';
            
            // 恢复按钮状态
            convertBtn.disabled = false;
            convertBtn.textContent = 'Convert';
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
        curlOutput.textContent = '// Curl command will be displayed here';
    });
    
    // 复制Curl按钮
    copyCurlBtn.addEventListener('click', function() {
        const textToCopy = curlOutput.textContent;
        navigator.clipboard.writeText(textToCopy)
            .then(() => {
                // 显示复制成功提示
                const originalText = this.textContent;
                this.textContent = 'Copied!';
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
        console.log(`User input ${language} code:`, code);
        
        if (!code) {
            showNotification('Please enter code', 'error');
            return;
        }
        
        // 显示加载状态
        convertCodeBtn.disabled = true;
        convertCodeBtn.textContent = 'Converting...';
        
        // 准备发送的数据
        const requestData = {
            code: code,
            language: language
        };
        console.log('准备发送的数据:', requestData);
        
        // 发送请求到后端API
        console.log('Sending request to: /api/reverse');
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
                showNotification('Conversion failed: ' + (data.message || 'Unknown error'), 'error');
                curlOutput.textContent = 'Conversion failed. Please check if your code is correct.';
                convertCodeBtn.disabled = false;
                convertCodeBtn.textContent = 'Convert';
                return;
            }
            
            // 显示curl命令
            curlOutput.textContent = data.command;
            curlOutput.className = 'bash';
            
            showNotification('Conversion successful', 'success');
            
            // 恢复按钮状态
            convertCodeBtn.disabled = false;
            convertCodeBtn.textContent = 'Convert';
        })
        .catch(error => {
            console.error('请求出错:', error);
            showNotification('Conversion failed: ' + error.message, 'error');
            curlOutput.textContent = 'Conversion failed. Please check if your code is correct.';
            
            // 恢复按钮状态
            convertCodeBtn.disabled = false;
            convertCodeBtn.textContent = 'Convert';
        });
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
