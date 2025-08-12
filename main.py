import os
from fastapi import FastAPI, status
import logging
from openai import OpenAI
from pdf_directory_extractor import find_pdf_and_extract_toc

# 配置日志
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# 全局变量存储书籍数据
books_data = []

# 获取项目父目录
project_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(project_dir)
books_dir = os.path.join(parent_dir, 'books')

# 添加日志，显示当前设置的路径
print(f"Project directory: {project_dir}")
print(f"Parent directory: {parent_dir}")
print(f"Books directory: {books_dir}")

# 检查books目录是否存在
if not os.path.exists(books_dir):
    print(f"Warning: Books directory not found at {books_dir}")
    # 尝试创建books目录
    try:
        os.makedirs(books_dir)
        print(f"Created books directory at {books_dir}")
    except Exception as e:
        print(f"Error creating books directory: {e}")

# 加载书籍数据的函数
@app.on_event("startup")
def load_books_data():
    global books_data
    books_data = []

    print("开始加载书籍数据...")
    print(f"书籍目录路径: {books_dir}")

    # 检查 books 文件夹是否存在
    if not os.path.exists(books_dir):
        print(f"警告: 未找到书籍目录: {books_dir}")
        return
    else:
        print(f"找到书籍目录: {books_dir}")

    # 打印目录内容
    print(f"书籍目录内容: {os.listdir(books_dir)}")

    # 遍历第一层目录作为 series
    for series in os.listdir(books_dir):
        series_path = os.path.join(books_dir, series)
        print(f"检查: {series_path}")
        if not os.path.isdir(series_path):
            print(f"  跳过非目录: {series}")
            continue
        print(f"处理系列: {series}")

        # 打印系列目录内容
        print(f"  系列目录内容: {os.listdir(series_path)}")

        # 遍历series目录下的所有项目
        print(f"  系列目录内容: {os.listdir(series_path)}")
        for item in os.listdir(series_path):
            item_path = os.path.join(series_path, item)
            print(f"  检查: {item_path}")
            
            # 打印文件属性信息
            is_file = os.path.isfile(item_path)
            is_dir = os.path.isdir(item_path)
            is_pdf = item.lower().endswith('.pdf')
            print(f"  文件属性 - 是文件: {is_file}, 是目录: {is_dir}, 是PDF: {is_pdf}")
            
            # 如果是PDF文件，直接处理
            if is_file and is_pdf:
                print(f"  处理PDF书籍: {item}")
                # 移除文件扩展名作为书籍名称
                book_name = os.path.splitext(item)[0]
                
                # 解析series和level信息
                # 根据用户期望，设置series为"raz"，level为目录名
                current_series = "raz"
                current_level = series  # 使用目录名作为level
                
                print(f"  设置series: {current_series}, level: {current_level}")
                
                books_data.append({
                    "series": current_series,
                    "level": current_level,
                    "name": book_name
                })
            # 如果是目录，视为level目录
            elif is_dir:
                level = item
                level_path = item_path
                print(f"  处理级别: {level}")

                # 打印级别目录内容
                print(f"    级别目录内容: {os.listdir(level_path)}")

                # 遍历级别目录下的文件
                for name in os.listdir(level_path):
                    name_path = os.path.join(level_path, name)
                    print(f"    检查: {name_path}")
                    
                    # 打印文件属性信息
                    is_file_level = os.path.isfile(name_path)
                    is_dir_level = os.path.isdir(name_path)
                    is_pdf_level = name.lower().endswith('.pdf')
                    print(f"    文件属性 - 是文件: {is_file_level}, 是目录: {is_dir_level}, 是PDF: {is_pdf_level}")
                    
                    # 检查是否为PDF文件
                    if is_file_level and is_pdf_level:
                        print(f"    处理PDF书籍: {name}")
                        # 移除文件扩展名作为书籍名称
                        book_name = os.path.splitext(name)[0]
                        books_data.append({
                            "series": series,
                            "level": level,
                            "name": book_name
                        })
                    elif is_dir_level:
                        print(f"    处理目录书籍: {name}")
                        books_data.append({
                            "series": series,
                            "level": level,
                            "name": name
                        })
                    else:
                        print(f"      跳过非PDF文件: {name}")
                        continue
            else:
                print(f"  跳过非PDF文件和目录: {item}")
                continue

    print(f"书籍数据加载完成，共加载 {len(books_data)} 本书籍")
    print(f"加载的数据样例: {books_data[:2] if len(books_data) >= 2 else books_data}")




@app.get("/getBooks", status_code=status.HTTP_200_OK)
def get_books():
    return {
        "message": books_data
    }


@app.get("/getBookToc", status_code=status.HTTP_200_OK)
def get_book_toc(series: str, level: str, name: str):
    try:
        # 调用PDF目录提取函数
        result = find_pdf_and_extract_toc(series, level, name)
        if result["success"]:
            return {
                "success": True,
                "message": result["message"],
                "toc": result["toc"]
            }, status.HTTP_200_OK
        else:
            return {
                "success": False,
                "message": result["message"],
                "error_code": result["error_code"]
            }, status.HTTP_400_BAD_REQUEST
    except Exception as e:
        return {
            "success": False,
            "message": f"调用PDF目录提取功能时出错: {str(e)}",
            "error_code": "INTERNAL_ERROR"
        }, status.HTTP_500_INTERNAL_SERVER_ERROR


@app.get("/sendBook", status_code=status.HTTP_200_OK)
def send_book(series: str, level: str, name: str):
    try:
        # 获取API密钥
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            return {
                "success": False,
                "message": "API key not found",
                "error_code": "API_KEY_MISSING",
            }, status.HTTP_400_BAD_REQUEST

        # 创建OpenAI客户端
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

        # 调用API
        response = client.chat.completions.create(
            model="deepseek-chat",
            temperature=1,
            messages=[
                {
                    # todo add system role 
                    "role": "system",
                    "content": "你是一个专业的英语老师，你会根据用户提供的书名，生成3个子topic",
                },
                {

                    "role": "user",
                    "content": f"我是7岁男孩，每天会以昨晚看的书作为topic来和外教老师进行英语口语练习，帮我根据{series}系列{level}级别并且书名为{name}的书生成3个子topic，要求是英文的，并且包含book的名称以及章节名称，长度在不超过200个英文单词，你的口吻是家长给老师写的课前便签",
                }
            ],
            stream=False,
        )

        # 提取结果
        content = response.choices[0].message.content
        print(content)
        # 返回成功响应
        return {"success": True, "message": content}

    except Exception as e:
        # 捕获所有异常并返回错误响应
        return {
            "success": False,
            "message": str(e),
            "error_code": "SERVER_ERROR",
        }, status.HTTP_500_INTERNAL_SERVER_ERROR
