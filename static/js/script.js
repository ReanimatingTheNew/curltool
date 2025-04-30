document.addEventListener('DOMContentLoaded', function() {
    // 获取DOM元素
    const curlInput = document.getElementById('curlInput');
    const jsonOutput = document.getElementById('jsonOutput');
    const convertBtn = document.getElementById('convertBtn');
    const clearBtn = document.getElementById('clearBtn');
    const copyBtn = document.getElementById('copyBtn');
    const formatBtn = document.getElementById('formatBtn');
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
    
    // 转换按钮点击事件
    convertBtn.addEventListener('click', function() {
        const curlCommand = curlInput.value.trim();
        console.log('用户输入的curl命令:', curlCommand);
        
        if (!curlCommand) {
            showNotification('请输入curl命令', 'error');
            return;
        }
        
        // 准备发送的数据
        const requestData = {
            curl: curlCommand
        };
        console.log('准备发送的数据:', requestData);
        
        // 发送请求到后端API
        console.log('发送请求到: /api/convert');
        fetch('/api/convert', {
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
            // 格式化JSON并显示
            const formattedJson = JSON.stringify(data, null, 4);
            jsonOutput.textContent = formattedJson;
            
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
    
    // 清除按钮点击事件
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
    
    // 复制按钮点击事件
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
    
    // 选项卡切换功能
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // 移除所有活动状态
            tabBtns.forEach(b => b.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('active'));
            
            // 添加当前活动状态
            this.classList.add('active');
            const tabId = this.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
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
