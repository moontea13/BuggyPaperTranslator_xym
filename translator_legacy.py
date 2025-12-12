import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv
import openai
from openai import OpenAI
import tqdm
import csv
import tenacity
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import json

# 从environment中读取HF_TOKEN
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN", "") 

# 选用了 OpenAI 兼容接口
client = OpenAI(
    api_key=HF_TOKEN,
    base_url="https://router.huggingface.co/v1",
)

# 加入tenacity重试机制
@retry(
    stop=stop_after_attempt(5),  
    wait=wait_exponential(multiplier=1, min=4, max=60), 
    retry=retry_if_exception_type((openai.RateLimitError,openai.APITimeoutError,openai.APIConnectionError)),
    reraise=True
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
            max_tokens=len(text) * 3,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        raise


def main():
    # 读取数据
    df = pd.read_csv("iccv2025.csv")
     # 检查点
    checkpoint = 'checkpoint.json'
    processed = json.load(open(checkpoint))['processed'] if os.path.exists(checkpoint) else []

    if not os.path.exists("result.csv"):
        with open("result.csv", "w", encoding="utf-8") as f:
            f.write("title,authors,abstract,date,paper_url,score,title_cn,abstract_cn\n") 

    # 遍历每一行，翻译摘要
    for index, row in tqdm.tqdm(df.iterrows(), total=len(df), desc="翻译进度"):
        if index in processed:
            continue

        try:
            abstract = row['abstract']
            title = row['title']
            print(f"Translating paper {row['title']}...")

            title_cn = translate_text(title)
            abstract_cn = translate_text(abstract)

            with open("result.csv", "a", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow([title,row['authors'],abstract,row['date'],row['paper_url'],row['score'],title_cn,abstract_cn])
            
            processed.append(index)
            json.dump({'processed': processed}, open('checkpoint.json', 'w', encoding='utf-8'))
        except Exception as e:
            print(f"翻译失败: {e}")

        time.sleep(5)  # 更改了时间长度


if __name__ == "__main__":
    main()
