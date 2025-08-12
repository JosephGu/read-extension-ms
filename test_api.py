import requests
import time

# 测试getBookToc接口
if __name__ == '__main__':
    url = 'http://127.0.0.1:8000/getBookToc'
    params = {
        'series': 'raz',
        'level': 'w',
        'name': 'To Drill or Not to Drill'
    }

    # 简化打印输出
    print(f"测试getBookToc接口: {url}?series={params['series']}&level={params['level']}&name={params['name']}")

    try:
        # 尝试连接多次，确保服务器已经启动
        max_retries = 3
        retries = 0
        while retries < max_retries:
            try:
                response = requests.get(url, params=params, timeout=5)
                print(f"响应状态码: {response.status_code}")
                print(f"响应内容: {response.text[:200]}...")  # 只打印部分响应内容
                break
            except requests.exceptions.ConnectionError as e:
                retries += 1
                if retries < max_retries:
                    time.sleep(2)
                else:
                    print("连接失败: 达到最大重试次数")
        else:
            print("请求失败")
    except Exception as e:
        print(f"请求出错: {str(e)}")