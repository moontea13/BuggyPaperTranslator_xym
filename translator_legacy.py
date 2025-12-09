import os
import time
import requests
import pandas as pd
from openai import OpenAI
import tqdm

# 从environment中读取HF_TOKEN
HF_TOKEN = os.getenv("HF_TOKEN", "") 
# api_key = os.environ.get("HF_TOKEN")
# print(f"API Key exists: {bool(api_key)}")
# print(f"Key length: {len(api_key) if api_key else 0}")

# 选用了最新的 OpenAI 兼容接口
client = OpenAI(
    api_key=HF_TOKEN,
    base_url="https://router.huggingface.co/v1",
)


def translate_text(text):  # 用来调用API翻译传入的文本
    # 更改了模型
    model_name = "openai/gpt-oss-120b:fastest"

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                # 简单更改了prompt
                {"role": "system", 
                 "content": "你是一个专业翻译助手，请将用户提供的一批英文论文的标题或摘要翻译成中文，每次输出为一段无格式、无换行的文字。保持原意不变，语言自然流畅，术语准确。"},
                {"role": "user", 
                 "content": f"请翻译以下文本：\n{text}"}
            ],
            temperature=0.2,
            max_tokens=len(text) * 2,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        return None


def main():
    # 读取数据
    # df = pd.read_csv("papers.csv")
    df = pd.read_csv("iccv2025.csv")

    if not os.path.exists("result.csv"):
        with open("result.csv", "w", encoding="utf-8") as f:
            f.write("title,authors,abstract,date,paper_url,score,title_cn,abstract_cn\n") 

    # 遍历每一行，翻译摘要
    for index, row in tqdm.tqdm(df.iterrows(), total=len(df), desc="翻译进度"):
        abstract = row['abstract']
        title = row['title']
        print(f"Translating paper {row['title']}...")

        try:
            title_cn = translate_text(title)
            abstract_cn = translate_text(abstract)
        except Exception as e:
            print(f"翻译失败: {e}")
            continue  # 跳过这一条，继续下一个

        # 将结果写入新文件
        with open("result.csv", "a", encoding="utf-8") as f: # 改为用a模式写入
            f.write(f"{title},{row['authors']},{abstract},{row['date']},{row['paper_url']},{row['score']},{title_cn},{abstract_cn}\n")
        time.sleep(2)  # 避免请求过于频繁 更改了时间长度


if __name__ == "__main__":
    main()
