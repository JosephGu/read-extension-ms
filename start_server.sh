#!/bin/bash

# 启动 Uvicorn 服务器
uvicorn main:app --host 0.0.0.0 --port 8080

# 可选：如果需要在服务器停止后保持终端窗口打开，可以取消下面一行的注释
# read -p "按 Enter 键继续..."