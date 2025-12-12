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
创建一个.env文件并在里面写入`HF_TOKEN=你的token`

### 2. 需要的python第三方包
按照requirements_fix.txt下载

## 运行方式
### 1. 运行前
- 把`df = pd.read_csv("iccv2025.csv")`双引号内部改成翻译的目标文件
- 如果需要翻译一篇新的内容，需要手动删除checkpoint.json文件
### 2. 运行
### 3. 运行时：
如果翻译到一半出现:
`Error code: 402 - {'error': 'You have reached the free monthly usage limit for cerebras. Subscribe to PRO to get 20x more included usage, or add pre-paid credits to your account.'}`
则可以尝试把脚本中`time.sleep(5)`数字改长，等待一段时间（约一分钟）之后重新执行脚本，可从当前出错位置继续翻译后面内容

如果需要指定位置的续传：
在checkpoint.json文件删除该行后面编号（从0开始编号），即可实现从该行后面续传