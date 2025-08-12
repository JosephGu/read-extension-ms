import os
from pdf_directory_extractor import find_pdf_and_extract_toc

# 测试函数
if __name__ == '__main__':
    # 测试1：使用已知存在的书籍
    print("测试1：使用已知存在的书籍")
    result = find_pdf_and_extract_toc('raz', 'w', 'To Drill or Not to Drill')
    print(f"结果: {result}")
    print()

    # 测试2：使用不存在的书籍
    print("测试2：使用不存在的书籍")
    result = find_pdf_and_extract_toc('raz', 'w', '不存在的书籍')
    print(f"结果: {result}")
    print()

    # 测试3：测试不同级别的书籍
    print("测试3：测试不同级别的书籍")
    result = find_pdf_and_extract_toc('raz', 'v', 'Another Book')
    print(f"结果: {result}")