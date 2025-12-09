import os
import time
import requests
import pandas as pd
from openai import OpenAI
import tqdm

# 从environment中读取HF_TOKEN
HF_TOKEN = os.getenv("HF_TOKEN", "") 

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
                 "content": "你是一个专业翻译助手，请将用户提供的一批英文论文的标题和摘要翻译成中文。保持原意不变，语言自然流畅，术语准确。"},
                {"role": "user", 
                 "content": f"请翻译以下文本：\n{text}"}
            ],
            temperature=0.2,
            max_tokens=len(text) * 3,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        return None


def main():
    # 读取数据
    df = pd.read_csv("papers.csv")

    # 遍历每一行，翻译摘要
    for index, row in df.iterrows():
        abstract = row['abstract']
        print(f"Translating paper {row['id']}...")

        cn_abstract = translate_text(abstract)

        # 将结果写入新文件
        with open("result.csv", "a", encoding="utf-8") as f: # 改为用a模式写入
            f.write(f"{row['id']},{cn_abstract}\n")
        time.sleep(2)  # 避免请求过于频繁 更改了时间长度


if __name__ == "__main__":
    main()
