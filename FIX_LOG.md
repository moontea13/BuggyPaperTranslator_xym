# 修改记录
## 做的时候修复的一些未声明的坑：
   - `import request` -> 拼写错误 requests; `import qtmd` -> 拼写错误 tqdm显示进度
   - 每次翻译后`sleep(1000)`，目的是为了避免触发翻译API的速率限制，但是时间过长，所以可以调短时间，但是过短（如`sleep(3)`）则会触发API速率限制（出现如下代码报错）。
      > Error code: 402 - {'error': 'You have reached the free monthly usage limit for cerebras. Subscribe to PRO to get 20x more included usage, or add pre-paid credits to your account.'}
   
      简单做了一个测试：如果在执行之间没有用过这个API，则sleep(5)即可顺利跑完要求的翻译文档，如果之前用过这个API，可能会被中断。
   - 翻译写入的函数中有诸多错误：
     - 需要加入表头。
     - 表头并没有id的元素，故改为title来区分识别每一个文章。
     - 同时原代码只翻译了abstract没有翻译title。
     - 文件 result.csv 在每次循环中都以写入模式（"w"）打开，每次迭代都会覆盖之前的内容。应该改为追加模式（"a"）。
   - 大模型翻译的时候会加空行影响输出格式样式，在prompt中加命令即可解决。同时，使用csv中writer.writerow可以按照格式每行写入，故引入了csv库函数。
   - 翻译到后半程调用api时出现提示。每次重新生成时都是前半程（约15条能翻译成功，后面翻译失败），故不是总量到达限制，应该是请求频率过高所以限制

## 按照要求修改的内容
   - requirements_fix.txt是使用`pipreqs . --encoding=utf8 --savepath=requirements_fix.txt`自动生成的，包含的均为实际用到的库，但是版本号可能略有出入
   - API 升级：使用`OpenAI` 兼容接口
   - 模型的参数若干错误的修复说明:
     - `temperature`为文本创造性，参数设置在0-0.3适合学术论文翻译
     - `max_tokens`为输出长度，1个token ≈ 0.75个单词 ≈ 1-2个汉字，需要留出一定空间
   - **Prompt 优化**：简单优化了一下，声明了角色和一些要求
   - **异常处理**：使用了 `tenacity`重试机制（最多重复尝试次数设置为5，尝试时间间隔成指数级增长，如果最终尝试失败则返回的异常信息为最后一次尝试的异常原因信息）
   - **Token 安全**：已经改为从环境变量读取。不过我使用的环境变量读取方式是从命令行临时写入，所以没有用到`python-dotenv`这个包
   - **断点续传**：使用记录日志的形式实现，将成功翻译的条目记录进入（checkpoint.json）下一次进入程序会跳过成功条目。在测试时使用了sleep(3)来制造触发API的速率限制