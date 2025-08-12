import os

# 测试单个PDF文件的属性
pdf_path = r'G:\workspace\books\w\Vikings.pdf'

print(f"测试文件: {pdf_path}")
print(f"文件是否存在: {os.path.exists(pdf_path)}")
print(f"是否为文件: {os.path.isfile(pdf_path)}")
print(f"是否为目录: {os.path.isdir(pdf_path)}")
print(f"是否为PDF文件: {pdf_path.lower().endswith('.pdf')}")

# 尝试读取文件内容（仅读取前100个字节）
if os.path.isfile(pdf_path):
    try:
        with open(pdf_path, 'rb') as f:
            content = f.read(100)
            print(f"成功读取文件前100个字节: {content[:20]}...")
    except Exception as e:
        print(f"读取文件失败: {e}")