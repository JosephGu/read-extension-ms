import os
from fastapi import FastAPI, status
from openai import OpenAI

app = FastAPI()


@app.get("/getBooks", status_code=status.HTTP_200_OK)
def root():
    return {
        "message": [
            {
                "series": "Harry Potter",
                "level": "1",
                "name": "Harry Potter and the Philosopher's Stone",
            },
            {
                "series": "Harry Potter",
                "level": "2",
                "name": "Harry Potter and the Chamber of Secrets",
            },
            {
                "series": "Harry Potter",
                "level": "3",
                "name": "Harry Potter and the Prisoner of Azkaban",
            },
            {
                "series": "The Lord of the Rings",
                "level": "1",
                "name": "The Fellowship of the Ring",
            },
            {"series": "The Lord of the Rings", "level": "2", "name": "The Two Towers"},
            {
                "series": "The Lord of the Rings",
                "level": "3",
                "name": "The Return of the King",
            },
            {"series": "Hello World", "level": "3", "name": "RAZ"},
        ]
    }


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
