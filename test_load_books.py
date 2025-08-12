import os
import sys

sys.path.append('g:\workspace\read-extension-ms')

# 导入main.py中的相关变量和函数
from main import load_books_data, books_dir, books_data

# 打印当前配置
print(f"测试书籍加载功能")
print(f"书籍目录: {books_dir}")

# 调用加载函数
load_books_data()

# 打印结果
print(f"测试完成，共加载 {len(books_data)} 本书籍")
print(f"加载的数据样例: {books_data[:5] if len(books_data) >=5 else books_data}")