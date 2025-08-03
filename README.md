# FastAPI 图书API服务

这是一个简单的FastAPI应用，提供图书信息的API接口。

## 功能
- `/getBooks` 端点返回图书列表

## 安装依赖

1. 确保已安装Python 3.7+。
2. 安装所需依赖：
   ```bash
   pip install fastapi uvicorn
   ```

## 运行服务

### 方法1：使用启动脚本
1. 双击运行 `start_server.bat` 文件
2. 服务器将启动在 http://0.0.0.0:8080

### 方法2：手动运行
在命令行中执行：
```bash
uvicorn main:app --host 0.0.0.0 --port 8080
```

## 访问API
服务启动后，可以通过以下URL访问API：
- 图书列表: http://localhost:8080/getBooks