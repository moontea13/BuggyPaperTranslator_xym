# 科研文献翻译工具 Project HF-Translator (Buggy Paper Translator)
## 功能：
> “在科研过程中，我们需要快速浏览海量的英文文献。为了加快扫描文献的速度，我们通常会使用一些大模型来帮我们把扫下来的文献翻译成中文。要在没有本地 GPU 显存的情况下实现这一目标，我们需要利用云端的大模型推理服务。该Python 脚本，利用 **Hugging Face Inference Providers** 的免费层级（Free Tier），可自动将一批英文论文的标题和摘要翻译成中文。并且实现了进度显示和断点续传
------

## 环境配置
### 1. 获取HuggingFace Token并设置
#### 1.1 获取HuggingFace Token
1. 访问 https://huggingface.co/settings/tokens
2. 创建新的token（需要读取权限）
3. 复制token

#### 1.2 设置Token方式（任选其一）
##### 方式A：设置环境变量
```bash
# Linux/Mac
export HF_TOKEN="你的token"
# Windows PowerShell
$env:HF_TOKEN="你的token"
```
##### 方式B：使用huggingface-cli
```
# 终端输入
pip install huggingface_hub
hf auth login
# 粘贴你的token
```

### 2. 需要的python第三方包
按照requirements_fix.txt下载

## 运行方式
### 1. 改需要翻译的文件名
把`df = pd.read_csv("iccv2025.csv")`双引号内部改成翻译的目标文件
### 2. 运行即可
### 3. 如果翻译到一半出现:
`Error code: 402 - {'error': 'You have reached the free monthly usage limit for cerebras. Subscribe to PRO to get 20x more included usage, or add pre-paid credits to your account.'}`
则可以尝试把脚本中`time.sleep(5)`数字改长，等待一段时间（约一分钟）之后重新执行脚本，可从当前出错位置继续翻译后面内容