import os

# 模拟main.py中的变量和逻辑
books_dir = r'G:\workspace\books'
books_data = []

# 打印测试配置
print(f"测试完整书籍加载逻辑")
print(f"书籍目录: {books_dir}")
print(f"目录是否存在: {os.path.exists(books_dir)}")

# 模拟load_books_data函数
print("开始加载书籍数据...")

# 检查 books 文件夹是否存在
if not os.path.exists(books_dir):
    print(f"警告: 未找到书籍目录: {books_dir}")
else:
    print(f"找到书籍目录: {books_dir}")
    print(f"书籍目录内容: {os.listdir(books_dir)}")

    # 遍历第一层目录作为 series
    for series in os.listdir(books_dir):
        series_path = os.path.join(books_dir, series)
        print(f"检查系列: {series_path}")
        if not os.path.isdir(series_path):
            print(f"  跳过非目录系列: {series}")
            continue
        print(f"处理系列: {series}")
        print(f"  系列目录内容: {os.listdir(series_path)}")

        # 遍历第二层目录作为 level
        for level in os.listdir(series_path):
            level_path = os.path.join(series_path, level)
            print(f"  检查级别: {level_path}")
            if not os.path.isdir(level_path):
                print(f"    跳过非目录级别: {level}")
                continue
            print(f"  处理级别: {level}")
            print(f"    级别目录内容: {os.listdir(level_path)}")

            # 遍历文件作为书籍
            for name in os.listdir(level_path):
                name_path = os.path.join(level_path, name)
                print(f"    检查文件: {name_path}")
                
                # 打印文件属性信息
                is_file = os.path.isfile(name_path)
                is_dir = os.path.isdir(name_path)
                is_pdf = name.lower().endswith('.pdf')
                print(f"    文件属性 - 是文件: {is_file}, 是目录: {is_dir}, 是PDF: {is_pdf}")
                
                # 检查是否为PDF文件
                if is_file and is_pdf:
                    print(f"    处理PDF书籍: {name}")
                    # 移除文件扩展名作为书籍名称
                    book_name = os.path.splitext(name)[0]
                    books_data.append({
                        "series": series,
                        "level": level,
                        "name": book_name
                    })
                elif is_dir:
                    print(f"    处理目录书籍: {name}")
                    books_data.append({
                        "series": series,
                        "level": level,
                        "name": name
                    })
                else:
                    print(f"      跳过非PDF文件: {name}")

print(f"书籍数据加载完成，共加载 {len(books_data)} 本书籍")
print(f"加载的数据样例: {books_data[:5] if len(books_data) >=5 else books_data}")