# Curl 转 JSON 工具

这是一个简单高效的工具，可以将 curl 命令转换为 JSON 格式，便于分析和处理。该工具提供了友好的 Web 界面和 API 接口，方便集成到其他系统中。

## 功能特点

- 将 curl 命令解析为结构化的 JSON 格式
- 支持多种 curl 参数，如请求方法、头信息、数据等
- 提供 Web 界面，方便直接使用
- 提供 API 接口，便于集成到其他系统
- 美观的界面设计和用户友好的交互体验

## 安装与运行

### 前提条件

- Python 3.7+
- pip（Python 包管理器）

### 安装步骤

1. 克隆或下载本项目到本地
2. 进入项目目录
3. 安装依赖包

```bash
pip install -r requirements.txt
```

### 运行应用

```bash
python app.py
```

应用将在 http://localhost:5000 上运行。

## API 使用说明

### 接口地址

```
POST /api/convert
```

### 请求格式

```json
{
    "curl": "your curl command here"
}
```

### 响应格式

```json
{
    "method": "POST",
    "url": "https://api.example.com",
    "headers": {
        "Content-Type": "application/json"
    },
    "data": {
        "key": "value"
    }
}
```

## 示例

### 示例 curl 命令

```
curl -X POST https://api.example.com -H "Content-Type: application/json" -d '{"key":"value"}'
```

### 转换结果

```json
{
    "method": "POST",
    "url": "https://api.example.com",
    "headers": {
        "Content-Type": "application/json"
    },
    "data": {
        "key": "value"
    }
}
```

## 部署

该应用可以部署到任何支持 Python 的服务器上，如 Heroku、AWS、阿里云等。

### 使用 Gunicorn 部署

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 许可证

MIT

## 联系方式

如有任何问题或建议，请提交 issue 或联系开发者。
