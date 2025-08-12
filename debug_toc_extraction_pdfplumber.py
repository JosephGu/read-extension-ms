import os
import re
import logging
import pdfplumber

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def debug_pdf_toc_extraction(series, level, name):
    """
    使用pdfplumber调试PDF目录提取逻辑
    """
    # 构建书籍路径
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
        logger.error(f"未找到PDF文件: {name}.pdf")
        return
    
    logger.info(f"找到PDF文件: {pdf_path}")
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # 打印PDF信息
            logger.info(f"PDF页数: {len(pdf.pages)}")
            
            # 尝试从页面提取目录
            max_pages_to_check = min(5, len(pdf.pages))
            logger.info(f"尝试从第2-{max_pages_to_check}页提取目录")
            
            # 目录识别模式
            toc_patterns = [
                r'^\d+\.\s+',  # 1. 标题
                r'^Chapter \d+',  # Chapter 1
                r'^\d+\s+',  # 1 标题
                r'^[IVXLCDM]+\.\s+',  # I. 标题 (罗马数字)
                r'^[a-zA-Z]\.\s+',  # a. 标题
                r'^\d+\.\d+\s+',  # 1.1 标题
                r'^Section \d+',  # Section 1
                r'^[A-Z]\.\s+',  # A. 标题
            ]
            
            for page_num in range(1, max_pages_to_check):  # 索引从1开始（第2页）
                page = pdf.pages[page_num]
                page_text = page.extract_text()
                
                logger.info(f"\n===== 第{page_num+1}页内容 =====")
                # 打印页面文本长度
                logger.info(f"页面文本长度: {len(page_text) if page_text else 0} 字符")
                
                # 打印页面文本内容（限制长度）
                if page_text:
                    if len(page_text) > 500:
                        logger.info(f"页面文本前500个字符: {page_text[:500]}")
                    else:
                        logger.info(f"页面文本: {page_text}")
                else:
                    logger.info("页面文本为空")
                
                # 检查每个模式
                if page_text:
                    for pattern in toc_patterns:
                        pattern_matches = re.findall(pattern, page_text, re.MULTILINE)
                        if pattern_matches:
                            logger.info(f"模式 '{pattern}' 匹配到 {len(pattern_matches)} 个结果")
                            logger.info(f"匹配结果: {pattern_matches}")
                
                logger.info(f"在第{page_num+1}页找到可能的目录条目:")
                # 提取匹配的行
                toc_candidates = []
                if page_text:
                    lines = page_text.split('\n')
                    for line in lines:
                        line = line.strip()
                        if any(re.match(pattern, line) for pattern in toc_patterns):
                            toc_candidates.append(line)
                logger.info(f"候选目录条目: {toc_candidates}")
                
    except Exception as e:
        logger.error(f"处理PDF文件时出错: {str(e)}")

if __name__ == '__main__':
    # 测试特定书籍
    debug_pdf_toc_extraction('raz', 'w', 'To Drill or Not to Drill')