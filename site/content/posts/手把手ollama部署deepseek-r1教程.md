+++
title = '手把手Ollama部署DeepSeek R1教程'
date = '2026-05-11'
draft = false
tags = ['deploy']
+++

> 每次点开DeepSeek都在转圈提示服务器繁忙，明明写了漂亮的提示词却白白浪费——别忍了。这个**Ollama 部署 DeepSeek R1 教程**，十分钟内让模型在你的电脑上跑起来，摆脱网络依赖。


## Ollama安装前的硬件评估与系统要求
DeepSeek R1 系列模型从 1.5B 到 70B 参数不等，不同蒸馏版本的硬件需求差异明显。在开始 **Ollama 部署 DeepSeek R1 教程** 前，先用几分钟对照你的机器配置，避免下载后跑不动。

### 显卡显存：最低 2GB，推荐 8GB+

- **DeepSeek-R1-Distill-Qwen-1.5B**：约 1GB 显存，集成显卡或纯 CPU 也能运行（响应慢）。
- **DeepSeek-R1-Distill-Qwen-7B / DeepSeek-R1-Distill-Llama-8B**：量化后约 4–5GB 显存，推荐 **6GB** 以上（如 GTX 1060 6GB 或 RTX 3060 12GB）。
- **DeepSeek-R1-Distill-Qwen-14B**：量化后约 8–9GB 显存，需 **10GB+**（如 RTX 3080 10GB 或 RTX 4090）。
- **DeepSeek-R1 (671B 完整版)**：非量化需 **超过 400GB**，普通用户无法本地部署，跳过。

> 若显卡显存不足，可依赖 **系统内存**（使用 `--numa` 或 CPU-only 模式），但推理速度会慢 3–5 倍。内存至少 **16GB**，推荐 **32GB** 以上。

### CPU 与系统内存：不强制，但会影响体验

- 纯 CPU 运行 7B 模型需 **8GB 系统内存**（可用），14B 模型需要 **16GB**。
- 推荐 **至少 16GB 内存**，同时运行其他应用时避免卡顿。
- 操作系统支持 Windows 10+（x64）、macOS 11+（Intel 或 Apple Silicon）、以及主流 Linux 发行版（Ubuntu 20.04+、Debian 11+）。

### 硬盘空间：至少预留 10GB

- 1.5B 模型约 1GB，7B 模型约 4–5GB，14B 模型约 8–10GB。
- Ollama 自身占用约 500MB，模型默认存储在 `~/.ollama/models`（Linux/macOS）或 `C:\Users\<用户名>\.ollama\models`（Windows）。可更改存储路径，具体见下一节。

确认好硬件后，下一步就是下载安装 Ollama。如果显存紧张，可以优先选择 7B 的量化版本（Q4_K_M），在 4GB 显存的显卡上也能流畅对话。


---


## 下载并安装Ollama的两种方式（一键脚本与手动包）
Ollama 支持 **Linux、macOS 和 Windows**，安装方式因系统而异。我给你两种最实用的选择。

### 一键脚本（Linux / macOS）

打开终端，执行以下命令：

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

系统会自动完成依赖检查、软件包下载和配置。整个过程通常 **30 秒到 1 分钟**。安装完成后，运行 `ollama --version` 确认版本（当前稳定版为 `0.5.7`）。如果遇到权限错误，前面加 `sudo` 即可。

> 该脚本仅针对 Linux（x86_64 / ARM64）和 macOS（Intel / Apple Silicon）。Windows 用户请往下看。

### 手动安装包（Windows / macOS 图形化）

- **Windows**：访问 [ollama.com/download](https://ollama.com/download) 下载 `.exe` 安装程序，双击运行，一路默认即可。安装后 Ollama 会自动启动为后台服务，任务栏出现羊驼图标代表成功。
- **macOS**（也可用脚本，但手动包更直观）：下载 `.dmg` 文件，拖入 Applications 文件夹，首次打开需在“安全性与隐私”中允许。

两种方式都会将 Ollama 安装到系统路径。检查方法：打开命令行（Windows 用 `cmd` 或 `PowerShell`），输入 `ollama` 并回车，看到可用命令列表即安装成功。如果提示“不是内部或外部命令”，尝试**重启终端**或卸载重装。

> 安装后模型默认存储在 `~/.ollama/models`（Linux/macOS）或 `C:\Users\用户名\.ollama\models`（Windows）。若需要迁移目录，待模型下载后再操作，具体方法别担心，**本 Ollama 部署 DeepSeek R1 教程**的后续部分会详细说明。

现在 Ollama 已就绪，下一步就是拉取 DeepSeek R1 模型并开始使用了。


---


## 通过Ollama命令行下载并运行DeepSeek R1模型
## 通过Ollama命令行下载并运行DeepSeek R1模型

打开终端（macOS/Linux）或命令提示符/PowerShell（Windows），运行 `ollama` 确认服务正常。现在只需一条命令即可拉取模型。

### 选择模型版本并下载

DeepSeek R1 官方在 Ollama 仓库中发布了多个蒸馏版本。你根据前文硬件评估选定的型号执行以下命令：

```bash
# 1.5B 版本（适合低配或纯CPU）
ollama pull deepseek-r1:1.5b

# 7B 版本（4GB 显存可用）
ollama pull deepseek-r1:7b

# 8B (Llama蒸馏) 版本（6GB 显存推荐）
ollama pull deepseek-r1:8b

# 14B 版本（需10GB以上显存）
ollama pull deepseek-r1:14b
```

首次拉取会下载完整的 GGUF 量化文件。例如 7B 模型约 4.5GB，14B 约 9.2GB，下载速度取决于你的网络。Ollama 会显示进度条，**中途关闭终端不影响后台下载**，再次执行同名 pull 命令会恢复进度。

> 如果只想下载量化精度较低、体积更小的版本，例如 **DeepSeek-R1-Distill-Qwen-7B 的 Q4_K_M**，可使用标签 `deepseek-r1:7b-q4_K_M`（体积约 3.9GB）。完整的标签列表可在 [Ollama 模型库](https://ollama.com/library/deepseek-r1) 查看。

### 运行模型并测试

下载完成后，直接运行：

```bash
ollama run deepseek-r1:7b
```

终端进入交互模式，你会看到 `>>>` 提示符。输入任何问题，模型会逐字生成回复。例如输入“请用中文介绍你自己”，DeepSeek R1 会展示其思考链标记（`<think>...</think>`）和最终回答。

- 按 **Ctrl+D** 或输入 `/bye` 退出交互模式。
- 使用 `ollama run` 时也可一次性传入提示：`ollama run deepseek-r1:7b "解释什么是量子计算"`
- 如果显存不足导致运行卡死，按 **Ctrl+C** 强制停止，换用更小的模型或开启 `--numa` 参数：`ollama run deepseek-r1:1.5b --numa`

### 验证模型存储位置与切换路径

模型默认存放在 `~/.ollama/models/blobs`（Linux/macOS）或 `C:\Users\用户名\.ollama\models\blobs`（Windows）。可通过设置环境变量 `OLLAMA_MODELS` 更改存储目录。例如 Linux 下：`export OLLAMA_MODELS=/data/ollama/models`，然后重启 Ollama 服务。**变更完成后已有的模型不会自动迁移**，需手动移动 blobs 文件夹或重新 pull。

运行成功后，这个 **Ollama 部署 DeepSeek R1 教程** 的核心环节就完成了。如果想用图形界面与模型聊天，可以直接接入 Open WebUI 或 Chatbox，下一节会详细配置方法。


---


## 修改模型存储路径与从GGUF文件自定义创建模型
默认模型存储在 `~/.ollama/models`，但系统盘空间不够时，你需要改路径。同时，如果你已经下载了 GGUF 格式的 DeepSeek R1 文件，也可以直接用 Ollama 加载，无需再次拉取。本节覆盖这两个常见需求。

### 修改模型存储路径：环境变量与服务重启

Ollama 通过 `OLLAMA_MODELS` 环境变量控制模型存放目录。**设置前请先关闭所有运行中的 Ollama 进程**（Windows 任务管理器结束 `ollama.exe`，Linux/macOS 执行 `systemctl stop ollama` 或 `killall ollama`）。

**Windows 永久设置**：  
1. 右键“此电脑” → 属性 → 高级系统设置 → 环境变量。  
2. 新建系统变量，变量名 `OLLAMA_MODELS`，变量值例如 `D:\AI\Models`。  
3. 重启电脑或重新启动 Ollama 服务（在服务管理器中找到 `Ollama` 并重启）。  
4. 验证：运行 `ollama list` 查看模型列表，如果没有模型，说明路径已变空。

**Linux/macOS 永久设置**（以 `~/.bashrc` 或 `~/.zshrc` 为例）：  
```bash
echo 'export OLLAMA_MODELS=/mnt/data/ollama/models' >> ~/.bashrc
source ~/.bashrc
systemctl --user restart ollama   # 若使用用户服务
# 或 killall ollama && ollama serve &
```
**迁移已有模型**：变量生效后，`ollama list` 显示为空。你需要手动将旧目录下的 `blobs` 和 `manifests` 文件夹复制到新路径，然后重新运行 `ollama list`。如果复制后依然不显示，重启 Ollama 即可。

> 如果只是临时测试，在启动 Ollama 前设置一次环境变量即可：`export OLLAMA_MODELS=/tmp/test_models && ollama serve`。

### 从 GGUF 文件自定义创建模型

假设你已下载了 DeepSeek R1 的 GGUF 文件（例如 `deepseek-r1-8b-Q4_K_M.gguf`），可以通过 **Modelfile** 创建供 Ollama 使用的模型。

1. 将 GGUF 文件放入一个目录，例如 `/data/gguf/`。  
2. 在同目录下创建 Modelfile（无扩展名）：
   ```dockerfile
   FROM ./deepseek-r1-8b-Q4_K_M.gguf
   ```
   如果需要自定义 `temperature`、`top_p` 等参数，可在后面追加：
   ```dockerfile
   PARAMETER temperature 0.7
   PARAMETER top_p 0.9
   ```
3. 执行创建命令：
   ```bash
   ollama create deepseek-r1:8b-mybuild -f ./Modelfile
   ```
   整个过程通常在几秒内完成，因为只是基于本地文件注册元数据。

4. 验证并运行：
   ```bash
   ollama list   # 确认新模型出现
   ollama run deepseek-r1:8b-mybuild
   ```

**注意事项**：  
- Modelfile 中 `FROM` 路径支持绝对路径或相对路径，建议使用绝对路径避免歧义。  
- 同一个 GGUF 文件可以绑定多个 `ollama create` 命令，创建不同参数配置的版本。  
- 若 Ollama 运行时提示“无效的 GGUF”，检查文件完整性或是否使用正确的模型（DeepSeek R1 蒸馏版）。  

这两个操作在 **Ollama 部署 DeepSeek R1 教程** 中非常实用——尤其当系统盘空间告急，或你想用自己下载的量化文件避免重复下载时。完成路径修改或自定义模型后，后续的对话和 API 调用都会自动应用新配置。


---


## 搭配Chatbox或Open WebUI实现可视化交互对话
从终端里敲命令终究不方便，尤其是在调试提示词或观察长回复时。**Chatbox** 和 **Open WebUI** 是两个主流的选择，它们能直接挂载你刚用 Ollama 部署的 DeepSeek R1，提供聊天窗口、历史记录和对话管理。

### 用 Chatbox 连接本地模型（Windows / macOS / Linux）

Chatbox 是一款轻量桌面客户端，支持接入 Ollama 的 HTTP API。

1. 从 [chatboxai.app](https://chatboxai.app) 下载对应系统的安装包（当前版本 `2.3.5`）。安装后启动。
2. 进入设置 → “模型提供方”，选 **Ollama**。  
   - API 地址默认 `http://localhost:11434`，一般无需修改。  
   - 模型名称写你之前 pull 的完整名字，例如 `deepseek-r1:7b`。点击“连接测试”，绿色提示即成功。
3. 在主界面新建对话，选择刚配置的模型即可开始聊天。支持多轮对话和上下文记忆，无需额外配置。

> 如果连接报错，检查 Ollama 是否在后台运行（`ollama serve`）。Windows 用户可在任务栏羊驼图标右键 → “Show log” 查看端口占用情况。

### 用 Open WebUI 搭建 Web 聊天界面（推荐团队使用）

Open WebUI 是一个自托管的 Web 应用，功能更丰富：用户管理、对话历史搜索、Markdown 渲染、RAG 文件上传等。支持 Docker 和 pip 两种安装方式。

**Docker 部署（推荐）：**

```bash
docker run -d -p 3000:8080 \
  -v open-webui:/app/backend/data \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:main
```

启动后浏览器访问 `http://localhost:3000`，注册第一个账号即为管理员。进入设置 → “模型”，Ollama 基础 URL 保持 `http://host.docker.internal:11434`（Windows/macOS Docker 会自动映射）。点击刷新，下拉列表中应出现你已下载的 DeepSeek R1 模型。

**pip 本地安装（无需 Docker）：**

```bash
pip install open-webui
open-webui serve
```

访问 `http://localhost:8080`。注意此方式会直接使用本机的 Ollama 服务，模型列表自动同步。

### 关键配置细节

- 两种工具都默认请求 Ollama 的 `http://localhost:11434`。如果你修改过 Ollama 端口（比如启动时指定了 `OLLAMA_HOST=0.0.0.0:11435`），需在工具中同步更改 API 地址。
- 如果想让局域网其他设备访问你的对话界面，Open WebUI 的 Docker 容器启动时加 `--network host`；Chatbox 本身是桌面客户端，不支持局域网共享。
- 遇到模型回复中断或不响应，先切回命令行 `ollama run deepseek-r1:7b` 确认模型本身正常。若命令行正常，检查工具中的模型名称是否完全一致（包括大小写和标签名）。

可视化工具让 **Ollama 部署 DeepSeek R1 教程** 的成果真正可用，日常写代码、写文档、翻译都可以直接在这两个界面上完成，比翻来覆去敲命令行省心得多。


---


## 使用LangChain与Ollama构建本地RAG知识库应用
使用 LangChain 与 Ollama 构建本地 RAG 知识库应用

前几节你已能在终端或图形界面与 DeepSeek R1 单轮对话，但本地文档检索（RAG）场景需要更系统的方案。**LangChain** 配合 **Ollama** 可以快速搭建一个本地知识库问答系统：上传你的 PDF、Markdown 或代码文件，让模型基于文档内容回答，而非依赖其预训练知识。这个过程无需联网，数据完全留在本地。

### 准备 Python 环境与依赖

确保已安装 Python 3.10+，然后创建虚拟环境并安装核心库：

```bash
pip install langchain langchain-community langchain-chroma langchain-ollama chromadb pypdf
```

- `langchain-ollama` 封装了 Ollama 的 Chat 与 Embedding API，当前版本 `0.2.0`。
- `chromadb` 是向量数据库，用于存储文档片段。
- `pypdf` 用于读取 PDF 文件（如不需要可跳过）。

此外，还需要一个**嵌入模型**。DeepSeek R1 本身是生成模型，不提供文本向量。推荐使用 Ollama 上的 `nomic-embed-text`（约 274MB），直接 pull：

```bash
ollama pull nomic-embed-text
```

> 这个嵌入模型专门用于将文本转为向量，大小约 274MB，显存消耗极低（CPU 也能跑）。如果显存紧张，也可使用 `all-minilm`（约 50MB）。

### 创建 RAG 流水线：加载 → 分割 → 向量化 → 检索

下面的 Python 脚本演示了完整流程（以单个 PDF 文件为例）：

```python
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain.chains import RetrievalQA

# 1. 加载文档
loader = PyPDFLoader("./your_document.pdf")
docs = loader.load()

# 2. 切分为块（chunk_size=500，chunk_overlap=50）
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
splits = text_splitter.split_documents(docs)

# 3. 初始化向量存储（使用 nomic-embed-text）
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectordb = Chroma.from_documents(documents=splits, embedding=embeddings, persist_directory="./chroma_db")

# 4. 创建检索器 + LLM
retriever = vectordb.as_retriever(search_kwargs={"k": 3})   # 返回前3个最相关块
llm = ChatOllama(model="deepseek-r1:7b", temperature=0.3)   # 低温度使回答更精准

# 5. 构建 RAG 问答链
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff"  # 将检索到的块直接填充进提示
)

# 6. 提问
query = "这篇文档的主要内容是什么？"
response = qa_chain.invoke(query)
print(response["result"])
```

**关键配置说明：**
- `chunk_size=500`：每段文本约 500 字符，适合普通文档；技术手册可调至 1000。
- `k=3`：检索返回 3 个片段，过少可能遗漏信息，过多会增加 token 消耗。
- `temperature=0.3`：RAG 场景建议 ≤0.5，避免模型偏离检索内容自由发挥。

### 验证与调优

首次运行会创建 `./chroma_db` 目录，并计算所有文档的向量（CPU 上处理 100 页 PDF 约需 2-3 分钟）。后续提问直接复用该向量库，无需重新加载。

如果回答质量不理想，检查两点：
1. **文档分块是否合理**：过大的 chunk 会让噪声淹没关键信息；过小则缺乏上下文。可以尝试 `chunk_size=300` 或 `chunk_overlap=100`。
2. **检索器返回内容**：在脚本中加入 `retriever.get_relevant_documents(query)` 打印实际检索到的块，确认它们包含了答案的信息。如果空白，检查 PDF 是否文字（不是扫描图片）以及嵌入模型是否正常。

这个 **Ollama 部署 DeepSeek R1 教程** 中构建的 RAG 应用，让模型不再依赖训练数据中的知识，而是根据你提供的文档实时生成回答。你可以将代码封装成 Flask 服务或集成到 Open WebUI 的知识库功能中，实现更丰富的交互。


---


## 常见错误排查与显存不足时的性能调优技巧
## 常见错误排查与显存不足时的性能调优技巧

**首要排查方向**：先确认 Ollama 服务在运行。终端输入 `ollama ls`，若能列出模型列表则服务正常。若报 `Error: connect ECONNREFUSED ::1:11434`，执行 `ollama serve` 后台启动。Windows 用户常遇到第一次运行 `ollama run` 时未启动守护进程，打开任务管理器找 `ollama.exe` 进程即可确认。

模型下载失败或中断时，删除残留文件后重试（`ollama rm deepseek-r1:7b` 然后重新 pull）。如果网络不稳定，尝试设置 `OLLAMA_ORIGINS=*` 环境变量后再启动（常见于反向代理场景）。

---

### 显存不足时的核心调优策略

**策略一：换用更小量化版本**  
同样是 DeepSeek R1 1.5B 参数，`q2_k` 仅需约 1.2GB 显存，`q4_k_m` 约 2.5GB。在 `ollama run` 时明确指定 tag：

```bash
ollama run deepseek-r1:1.5b-q2_k   # 仅需2GB显存
```

实测在 4GB 显存（NVIDIA GTX 1650）上，`q4_k_m` 勉强运行，但生成速度约 3 tokens/s；换用 `q2_k` 后速度提升至 8 tokens/s。更低压缩意味着更低质量，但长文本场景下仍可接受。

**策略二：卸载 GPU 层至 CPU**  
通过 `--num-gpu` 参数控制模型使用的 GPU 层数。将层数设为 0 则完全在 CPU 上推理（需系统内存 ≥ 16GB）：

```bash
ollama run deepseek-r1:7b --num-gpu 0
```

此方式显存占用降至 200MB 以下，但生成速度骤降（7B 模型在 i7-12700H 上约 1-2 tokens/s）。若显存不足但显存较大，可尝试 `--num-gpu 12`（默认 33 层），部分层在 GPU 部分在 CPU 混合运行。

**策略三：限制上下文长度（`ctx`）**  
默认上下文为 2048 token，显存占用与上下文线性相关。对简单问答可减少到 512：

```bash
OLLAMA_CTX=512 ollama run deepseek-r1:7b
```

或通过 `~/.ollama/api.override` 配置文件全局设置（创建 JSON 文件 `{"num_ctx": 512}`）。1024 上下文比默认 2048 节省约 30% 显存，适合短对话场景。

**策略四：调整线程数与并发**  
CPU 推理场景设置 `OLLAMA_NUM_THREADS` 为物理核心数（非逻辑核心），避免过高的线程争抢。GPU 推理时 `OLLAMA_NUM_PARALLEL` 设为 1，防止多请求爆显存。

> 常见错误 `out of memory (OOM)` 在 4GB 显存机器上运行 7B 模型时极其常见。此时 `ollama ps` 命令可查看当前所有模型的显存分配，及时清理不再使用的模型：`ollama stop <model-name>`。

---

### 硬件兼容性要点

- **Intel Arc 显卡**需设置 `OLLAMA_INTEL_GPU=0` 回退到 CPU 或使用 `--num-gpu 0`，否则报 `driver not found`。
- **AMD ROCm 用户**检查 `rocminfo` 输出，若未检测到 GPU 则自动启用 CPU。
- **8GB 内存的笔记本**运行 7B 模型时建议同时限制 `--num-gpu 0` 和 `ctx=512`，否则系统 swap 会导致整个 UI 卡死。

本 **Ollama 部署 DeepSeek R1 教程** 的调优核心就是“量化版本 + 上下文控制 + 层卸载”三脚架。具体组合需根据你机器的显存和内存实测调整，没有银弹。


---


## 总结
这个 **Ollama 部署 DeepSeek R1 教程** 覆盖了从硬件评估到 RAG 应用的完整链路。最后几条建议帮你巩固整个流程，确保部署结果稳定可用。

### 模型选型：7B Q4_K_M 是普适平衡点

- 显存 4–6GB：选 `deepseek-r1:7b-q4_K_M`（约 3.9GB），日常对话和代码翻译足够流畅。
- 显存 10GB+：选 `deepseek-r1:14b` 或 `deepseek-r1:14b-q4_K_M`，推理质量明显提升。
- CPU-only 或集成显卡：只推荐 `1.5b` 版本，或用 `--num-gpu 0` 强行跑 7B 但接受 1–2 tokens/s 的速度。

> 量化标签不要盲目追最低（如 q2_k），质量损失在长文本推理中会被放大。优先试 q4_k_m，出显存 OOM 再降级。

### 环境配置：改存储路径要在模型下载前

- 系统盘空间不足时，**先**设置 `OLLAMA_MODELS` 环境变量，再执行 `ollama pull`，避免后续迁移 blobs 文件夹的麻烦。
- Windows 用户设置后需重启 Ollama 服务（任务管理器 → 服务 → Ollama → 重启）。Linux 用户用 `systemctl --user restart ollama`。
- 如果已经下载了模型并想移动，手动复制 `blobs` 和 `manifests` 到新路径，然后 `ollama list` 验证。**不要直接删除旧目录**，复制成功后再清空。

### 日常使用：可视化界面与脚本任选

- 个人开发者：**Chatbox** 零配置，`http://localhost:11434` 填上去即可。
- 团队协作：**Open WebUI**（Docker 部署）支持多用户和对话历史搜索，端口 `3000` 默认开放。
- RAG 场景：复制前文的 Python 脚本，将 `chunk_size` 设为 500，嵌入模型用 `nomic-embed-text`。如果回答空泛，调低 `temperature` 到 0.2，并增加 `k` 值到 5。

### 性能瓶颈时的止损操作

- 显存不足：`ollama run deepseek-r1:7b --num-gpu 12`（将部分层卸载到 CPU），或直接 `--num-gpu 0`。
- 推理卡顿：设置 `OLLAMA_CTX=512` 临时环境变量，上下文长度减半，显存节省约 30%。
- 多模型冲突：运行 `ollama ps` 查看当前加载的模型，用 `ollama stop deepseek-r1:7b` 逐个卸载。

以上配置能让你稳定地使用 DeepSeek R1 进行本地推理，无论是日常问答、代码生成还是文档检索，都无需依赖云服务。所有数据保留在本地，隐私可控。