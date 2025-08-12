import os
import PyPDF2
import re
import logging

# 配置日志 (仅记录警告和错误)
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def find_pdf_and_extract_toc(series, level, name):
    """
    通过series、level和name查找对应的PDF文件，并提取目录

    参数:
        series: 书籍系列
        level: 书籍级别
        name: 书籍名称

    返回:
        dict: 包含状态、消息和目录数组的字典
    """
    # 构建书籍路径
    # 根据之前main.py中的逻辑，书籍存储在'G:\workspace\books'目录下
    books_dir = r'G:\workspace\books'
    
    # 尝试多种可能的路径格式
    possible_paths = [
        os.path.join(books_dir, level, f'{name}.pdf'),
        os.path.join(books_dir, series, level, f'{name}.pdf'),
        os.path.join(books_dir, series, f'{name}.pdf'),
        os.path.join(books_dir, f'{name}.pdf')
    ]
    
    pdf_path = None
    for path in possible_paths:
        if os.path.exists(path):
            pdf_path = path
            break
    
    if not pdf_path:
        return {
            "success": False,
            "message": f"未找到PDF文件: {name}.pdf",
            "error_code": "FILE_NOT_FOUND"
        }

    # 检查是否为PDF文件
    if not pdf_path.lower().endswith('.pdf'):
        return {
            "success": False,
            "message": f"找到的文件不是PDF文件: {pdf_path}",
            "error_code": "NOT_A_PDF"
        }

    # 仅在调试模式下记录找到的PDF路径
    # logger.info(f"找到PDF文件: {pdf_path}")

    try:
        # 打开PDF文件
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)

            # 检查PDF页数
            num_pages = len(reader.pages)
            if num_pages < 2:
                return {
                    "success": False,
                    "message": f"PDF文件页数不足2页，无法提取目录",
                    "error_code": "INSUFFICIENT_PAGES"
                }

            # 尝试从第2-5页提取目录（通常目录在这些页面）
            toc = []
            max_pages_to_check = min(5, num_pages)
            
            # 目录识别模式
            toc_patterns = [
                r'^\d+\.\s+',  # 1. 标题
                r'^Chapter \d+',  # Chapter 1
                r'^\d+\s+',  # 1 标题
                r'^[IVXLCDM]+\.\s+',  # I. 标题 (罗马数字)
                r'^[a-zA-Z]\.\s+',  # a. 标题
                r'^\d+\.\d+\s+',  # 1.1 标题
            ]
            
            # 尝试从元数据获取目录
            if hasattr(reader, 'outline') and reader.outline:
                # 仅在调试模式下记录元数据目录提取信息
                # logger.info(f"从元数据中提取目录，找到 {len(reader.outline)} 个条目")
                for item in reader.outline:
                    if isinstance(item, dict) and 'title' in item:
                        toc.append(item['title'])
                    elif isinstance(item, tuple) and len(item) > 0 and isinstance(item[0], str):
                        toc.append(item[0])
            
            # 如果元数据中没有目录，尝试从页面提取
            if not toc:
                # 仅在调试模式下记录页面提取信息
                # logger.info(f"从页面中提取目录，检查第2-{max_pages_to_check}页")
                for page_num in range(1, max_pages_to_check):  # 索引从1开始（第2页）到max_pages_to_check-1
                    page = reader.pages[page_num]
                    page_text = page.extract_text()
                    
                    # 清洗文本
                    page_text = re.sub(r'\n+', '\n', page_text).strip()
                    
                    # 检查是否可能包含目录
                    if any(re.search(pattern, page_text, re.MULTILINE) for pattern in toc_patterns):
                        lines = page_text.split('\n')
                        for line in lines:
                            line = line.strip()
                            # 跳过空行和页码
                            if not line or line.isdigit() or len(line) > 100:  # 过长的行可能不是目录
                                continue
                             
                            # 检查是否匹配任何目录模式
                            if any(re.match(pattern, line) for pattern in toc_patterns):
                                toc.append(line)
                        
                        # 如果找到了目录条目，就不再检查后续页面
                        if toc:
                            # 仅在调试模式下记录找到的目录条目数
                            # logger.info(f"在第{page_num+1}页找到 {len(toc)} 个目录条目")
                            break
            
            # 去重并保持顺序
            toc = list(dict.fromkeys(toc))

            # 检查是否提取到目录
            if not toc:
                # 检查是否所有页面文本都为空
                all_pages_empty = True
                for page_num in range(min(5, len(reader.pages))):
                    page = reader.pages[page_num]
                    page_text = page.extract_text()
                    if page_text and page_text.strip():
                        all_pages_empty = False
                        break
                
                if all_pages_empty:
                    return {
                        "success": False,
                        "message": f"无法提取{name}.pdf的目录: PDF文件可能是扫描版或格式特殊，无法提取文本",
                        "error_code": "PDF_NO_TEXT",
                        "toc": []
                    }
                else:
                    return {
                        "success": True,
                        "message": f"成功提取{name}.pdf的目录，但未找到匹配的目录条目",
                        "toc": []
                    }
            
            return {
                "success": True,
                "message": f"成功提取{name}.pdf的目录",
                "toc": toc
            }

    except PyPDF2.errors.PdfReadError as e:
        logger.error(f"读取PDF文件时出错: {str(e)}")
        return {
            "success": False,
            "message": f"读取PDF文件时出错: {str(e)}",
            "error_code": "PDF_READ_ERROR"
        }
    except Exception as e:
        logger.error(f"处理PDF文件时出错: {str(e)}")
        return {
            "success": False,
            "message": f"处理PDF文件时出错: {str(e)}",
            "error_code": "PDF_PROCESSING_ERROR"
        }


# 测试代码
if __name__ == '__main__':
    # 示例调用
    result = find_pdf_and_extract_toc('raz', 'w', 'To Drill or Not to Drill')
    print(result)