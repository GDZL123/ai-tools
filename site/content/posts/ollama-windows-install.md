---
date: '2026-05-11T13:17:37+08:00'
draft: false
title: 'Ollama Windows Install'
slug: "ollama-windows-install"
keyword: "Ollama Windows 本地安装教程"
category: "AI本地部署"
---


> 你下载了一个开源大模型，想在本地运行，却发现需要配置复杂的Python环境和CUDA工具包。如果你正在寻找一份靠谱的Ollama Windows本地安装教程，这篇文章会一步步带你完成。
> 
> Ollama将模型下载、服务启动、API调用整合进一个安装程序。Windows上安装Ollama很简单：去官网下载OllamaSetup.exe（约745MB，支持Win10/11），双击运行即可。它安装在用户账户内，无需管理员权限。安装后，你就能通过命令行下载并运行模型，比如`ollama run deepseek-r1:7b`。
> 
> 这篇教程覆盖从下载、安装、模型管理到环境变量的配置。你不需要提前装Python或Docker。所有步骤都基于Ollama官方文档和社区常用设置，确保兼容性。
> 
> 下面，我们从下载安装程序开始。


## 安装前的系统要求与准备工作
Ollama 官方推荐在 **Windows 10（版本 1803 或更高）** 或 **Windows 11** 上安装，且必须为 **64 位系统**。如果你使用家庭版或专业版，均可正常运行；但长期运行多轮对话或推理任务，建议使用专业版以享受更完整的系统资源调度。

硬件方面，Ollama 本身占用极小，但模型推理依赖内存和存储：
- **系统内存至少 8GB**，运行 7B 参数模型需要空闲内存 ≥6GB。16GB 内存可流畅支持 13B 参数模型。
- 安装程序仅占用 **745MB 磁盘空间**，但模型文件会单独下载到 `%USERPROFILE%\.ollama`。一个 7B 模型约消耗 **4–5GB**，13B 约 **8–10GB**，请提前预留足够空间。
- CPU 需支持 **AVX 指令集**（大多数 2013 年后 x86-64 处理器均具备），否则 Ollama 会拒绝启动。

> 如果计划使用 **NVIDIA GPU** 加速推理，确保已安装 **NVIDIA 显卡驱动（≥版本 452.39）**。Ollama 在 Windows 上会自动调用 CUDA 运行时，但不会自动安装 CUDA Toolkit，因此建议额外安装 **CUDA 11.0+**。

网络条件同样关键：下载安装程序和模型文件需要稳定的互联网连接。美国或欧洲服务器速度更快，国内用户可考虑配置 **镜像源**（如使用 `OLLAMA_HOST` 环境变量指向国内加速节点），但这属于安装后的配置步骤。

这篇 **Ollama Windows 本地安装教程** 假设你已确认上述条件——只需核对一次，后续步骤即可直接执行。


---


## 下载Ollama官方安装程序
打开浏览器，进入[Ollama官方下载页面](https://ollama.com/download)。页面会自动识别你的操作系统，并显示一个蓝色**"Download for Windows"**按钮。点击后，浏览器会开始下载**OllamaSetup.exe**。

当前最新安装包的名称格式为`OllamaSetup_v0.5.12.exe`（版本号可能会更新），文件大小约**745MB**。下载速度取决于你的网络带宽——50Mbps宽带通常需要1.5–2分钟，国内用户若下载缓慢可尝试挂载代理。

下载过程有几点需要注意：

- **不要使用第三方下载器加速**，部分下载器会截断文件或修改签名，导致后续安装时出现"无法验证发布者"警告。
- 如果浏览器提示"此文件可能损害你的设备"，忽略即可。OllamaSetup.exe由Ollama Inc.数字签名，可直接保留。
- 下载完成后，建议右键点击安装程序 → **属性** → **数字签名**，确认签名方为"Ollama Inc."且状态显示"正常"。此举可确保你拿到的是官方正版文件，不是伪造包。

> 安全提示：永远只从 `https://ollama.com/download` 下载。网上存在第三方打包版本，可能捆绑广告软件或修改过注册表行为。

若你使用命令行下载（比如在PowerShell中）：  
```powershell
Invoke-WebRequest -Uri "https://ollama.com/download/OllamaSetup.exe" -OutFile "OllamaSetup.exe"
```
但需要提前知道当前版本号的精确URL。更推荐直接从浏览器下载，避免版本号匹配错误。

OllamaSetup.exe下载完成后，下一步就是双击运行安装程序。


---


## 在Windows上安装Ollama的完整步骤
双击 `OllamaSetup.exe` 启动安装程序。系统弹出 **用户账户控制(UAC)** 询问是否允许此应用更改设备——点击 **“是”**。安装器不会要求你选择安装目录或同意复杂许可协议，整个过程通常 **30秒内** 完成。

安装器默认将 Ollama 安装在当前用户的 `%LOCALAPPDATA%\Programs\Ollama` 路径下，**无需管理员权限**。它会在开始菜单创建快捷方式，并将可执行文件路径添加到该用户的 PATH 环境变量中。安装完成后，任务栏右下角会出现 Ollama 托盘图标（一只骆驼头像），说明服务已在后台自动启动。

### 验证安装是否成功
打开 **命令提示符(cmd)** 或 **PowerShell**，输入以下命令：

```cmd
ollama --version
```

如果返回类似 `ollama version is 0.5.12` 的信息，说明安装成功。若提示 `'ollama' 不是内部或外部命令`，可关闭当前终端窗口重新打开，让 PATH 刷新。如果依然无效，检查 `%LOCALAPPDATA%\Programs\Ollama` 是否确实存在于系统环境变量 `Path` 中，或手动添加。

### 常见安装问题与处理
- **安装过程中被 Windows Defender 拦截**：少数情况下，Ollama 的安装行为会被误报。此时可暂时关闭实时保护（设置 → 更新和安全 → Windows 安全中心 → 病毒和威胁防护 → 管理设置 → 关闭实时保护），安装后再重新开启。或者将 `OllamaSetup.exe` 添加到排除项。
- **安装后 Ollama 托盘图标消失**：在 PowerShell 中运行 `ollama serve` 手动启动服务，查看控制台输出是否有错误。常见原因是端口 11434 被占用，关闭占用该端口的程序后重启服务即可。
- **修改默认安装位置**（非必需）：通过设置环境变量 `OLLAMA_INSTALL_DIR` 指向自定义路径，再执行安装程序。但官方建议保持默认，因为模型数据路径`%USERPROFILE%\.ollama`才是存储大头。

> 注意：Ollama 安装后即注册为 **当前用户级别的后台服务**，随用户登录自动启动。如果你需要将 Ollama 作为系统服务（如开机无需登录即可运行），参考官方文档的“Install as a system service”部分，但这对大多数《Ollama Windows 本地安装教程》读者并非必要。

安装完成后，Ollama 服务处于待命状态，现在可以通过 `ollama list` 查看本地已有模型，或直接运行 `ollama run deepseek-r1:7b` 下载并启动第一个模型。


---


## 验证Ollama是否安装成功
安装完成后，需要从多个角度确认Ollama服务真正就绪。单纯的`ollama --version`只验证可执行文件存在，但无法保证后台服务、API端口或模型加载正常。这篇**Ollama Windows 本地安装教程**提供三层验证方法，覆盖命令行、服务端口和实际模型运行。

### 命令行基础验证
打开**PowerShell**或**命令提示符**，依次执行以下命令：

```powershell
ollama --version
```

预期输出类似 `ollama version is 0.5.12`（版本号可能更高）。若提示"不是内部命令"，关闭终端重新打开（PATH变量刷新），或手动检查 `%LOCALAPPDATA%\Programs\Ollama` 是否在系统环境变量中。

然后执行：

```powershell
ollama list
```

如果首次安装且未下载模型，输出显示 `NAME    ID    SIZE    MODIFIED` 空表头。**这并非错误**——说明服务正常启动，只是模型仓库为空。若提示 `Error: connection refused`，说明后台服务未运行，跳过此步，直接进入服务端口验证。

> 如果 `ollama list` 返回连接错误，不必先解决模型问题，重点检查服务进程是否存活。

### 服务端口与API验证
Ollama 默认在 **localhost:11434** 监听 HTTP 请求。通过以下方式验证：

- **检查端口监听**：在管理员 PowerShell 中运行
  ```powershell
  netstat -an | findstr :11434
  ```
  应看到 `LISTENING` 状态。
- **查询API根路径**：运行
  ```powershell
  curl http://localhost:11434
  ```
  返回 `Ollama is running`。
- **浏览器访问**：直接打开 `http://localhost:11434`，若页面显示纯文本 `Ollama is running`，说明服务和API均工作正常。

如果端口未被监听，在命令行执行 `ollama serve` 手动启动服务。控制台输出 `Starting Ollama...` 和 `Listening on 127.0.0.1:11434` 即为正常。若输出 `listen tcp 127.0.0.1:11434: bind: address already in use`，说明有另一个Ollama进程在运行，或端口被其他程序占用（如WSL、旧版Ollama）。用 `taskkill /IM ollama.exe /F` 结束所有进程后重新启动。

### 模型下载与运行验证
上述验证通过后，下载一个轻量模型测试实际推理能力。执行：

```powershell
ollama run deepseek-r1:1.5b
```

首次运行会自动下载约 1.1GB 的模型文件，进度条显示下载百分比。下载完成后进入交互式对话模式，输入 `hello` 并回车，应获得英文或中文回复。按 `Ctrl+D` 退出。

- 若下载时出现 `Error: pull model manifest: context deadline exceeded`，说明网络连接不稳定。可尝试挂载代理，或配置国内镜像源（参考后续环境变量章节）。
- 如果下载正常但对话无响应，检查内存占用：打开任务管理器 → 性能，确保空闲内存 ≥ 4GB（1.5B模型约占用 2GB）。

> 注意：`ollama run` 成功证明整个链路（安装、服务、模型下载、推理）均正常。如果只验证到API端口而跳过实际运行，后续可能因内存不足或模型损坏而在使用时才暴露问题。

现在，你可以通过 `ollama run` 下载并开始使用模型。


---


## 下载并运行你的第一个大语言模型
### 选择一个入门模型

下载模型前先明确两个选择：模型尺寸和参数版本。推荐从 **DeepSeek-R1:1.5b**（1.5B 参数）开始——它只有约 **1.1GB**，能在 8GB 内存的单核 CPU 上流畅运行，对话响应时间通常 2-5 秒。如果你的内存 ≥16GB 且有 NVIDIA GPU（显存≥4GB），可选 **7B 参数模型**，比如 `llama3.2:3b`（约 2.0GB）或 `deepseek-r1:7b`（约 4.5GB）。强烈建议首次跑最小模型，避免下载中途因内存不足被系统 kill。

### 执行下载命令

打开 **命令提示符** 或 **PowerShell**，输入：

```cmd
ollama pull deepseek-r1:1.5b
```

`pull` 命令会直接下载模型文件到 `%USERPROFILE%\.ollama\models`，不启动对话。进度条显示下载速度（MB/s）和预估剩余时间。以 100Mbps 宽带为例，1.1GB 文件约 **90 秒** 完成。如果网络慢，可等进度条走到 100% 后再进行下一步。

> 注意：`pull` 和 `run` 的区别——`pull` 只下载，不启动服务；`run` 会先自动下载再进入交互。首次使用建议用 `pull` 方便在后台观察资源占用（比如打开任务管理器查看磁盘 I/O）。

### 运行并测试模型

下载完成后，执行：

```cmd
ollama run deepseek-r1:1.5b
```

出现 `>>>` 提示符即表示模型已加载完毕，等待输入。输入一条中文问题，比如“你好，介绍一下自己”，然后按回车。模型会逐字生成回复，**CPU 推理时内存占用约 2.5GB**，GPU 推理则约 1.8GB（显存）。若输入回车后无响应超过 30 秒，按 `Ctrl+C` 中断，检查任务管理器里 `ollama_llama_server.exe` 进程是否持续高 CPU（>90%）——可能是可用内存不足，尝试关闭浏览器标签页后重试。

### 退出与常用操作

- **退出对话**：按 `Ctrl+D` 或输入 `/bye`。
- **重启对话（清空历史上下文）**：输入 `/clear`。
- **查看已下载的模型**：在 `ollama` 外键入 `ollama list`。
- **删除模型**：`ollama rm deepseek-r1:1.5b`（释放磁盘）。

运行第一个模型后，你就完成了 **Ollama Windows 本地安装教程** 的核心目标。后续可通过 `ollama run` 切换其他模型（如 CodeGemma、Mistral），或结合 `ollama pull` 预先缓存常用模型备用。


---


## 常见安装问题与解决方法
### 模型下载失败或速度极慢

如果 `ollama run deepseek-r1:1.5b` 在下载阶段报错 `Error: pull model manifest: context deadline exceeded`，通常是网络连接不稳定或被阻断。国内用户可尝试以下方案：

- **配置 HTTP 代理**：在 PowerShell 中执行 `$env:HTTP_PROXY="http://127.0.0.1:7890"` 和 `$env:HTTPS_PROXY=$env:HTTP_PROXY`（替换为你的代理地址），然后再运行 `ollama pull`。注意，这个环境变量只在当前终端生效，若需永久生效，添加至系统环境变量。
- **使用镜像源**：设置 `OLLAMA_HOST` 指向国内加速节点，例如 `https://ollama.mirror.example.com`（需自行寻找稳定源）。但这属于安装后配置，详见本文后续环境变量章节。
- **重试并预留空间**：模型下载被中断后，重新执行 `ollama pull` 会断点续传。确保 `%USERPROFILE%\.ollama` 所在磁盘剩余空间大于模型大小（1.5B 模型约 1.1GB，7B 约 4.5GB）。

> 如果下载进度条长时间不动（超过 5 分钟），按 `Ctrl+C` 取消，检查网络是否联通：`ping ollama.com`，若超时则需解决代理或更换网络环境。

### GPU 未被识别

你的机器明明有 NVIDIA 显卡，但 Ollama 依然使用 CPU 推理（推理速度慢、CPU 占用 100%）。检查点：

1. 确认 **NVIDIA 驱动版本 ≥ 452.39**：在命令行输入 `nvidia-smi`，查看右上角 **Driver Version**。如果低于此版本，请前往 NVIDIA 官网更新驱动。
2. 安装 **CUDA 11.0 或更高**：Ollama for Windows 依赖 CUDA 运行时，但安装程序不会自动安装。从 NVIDIA 官网下载 CUDA Toolkit（例如 12.5）并安装，安装时选择“精简安装”即可。
3. 验证 GPU 可见性：在 PowerShell 中运行 `ollama run deepseek-r1:1.5b` 并同时打开任务管理器 → 性能 → GPU 0，观察 **CUDA** 或 **Compute_0** 曲线是否跳动。若始终为 0，执行 `$env:CUDA_VISIBLE_DEVICES="0"` 强制指定 GPU。
4. 使用 `ollama ps` 查看当前模型使用的设备：输出会显示 `deepseek-r1:1.5b (GPU)` 或 `(CPU)`。若为 CPU，则说明 GPU 未被启用。

> 若你使用的是 AMD 或 Intel 集成显卡，目前 Ollama 在 Windows 上仅支持 NVIDIA GPU。集成显卡会回退到 CPU 推理，这是正常行为。

### 启动后 Ollama 自动退出或无法连接

有时双击托盘图标后，任务栏中骆驼图标消失，或者 `ollama list` 返回 `Error: connection refused`。手动排查：

- **手动启动服务**：打开 PowerShell，执行 `ollama serve`。查看输出是否有 `listen tcp 127.0.0.1:11434: bind: address already in use`。若有，说明端口被占用（如 WSL 2 的接口）。使用 `netstat -ano | findstr :11434` 查看 PID，然后 `taskkill /PID <PID> /F` 终止占用进程。
- **修改默认端口**：如果端口冲突无法解决，设置环境变量 `OLLAMA_HOST=0.0.0.0:11435`，然后重新运行 `ollama serve`。之后所有命令需通过 `ollama --host 0.0.0.0:11435 run <model>` 或修改 API 地址。
- **检查 Windows 事件查看器**：打开事件查看器 → Windows 日志 → 应用程序，筛选来源为“Ollama”的错误信息，常见原因是权限不足或模型文件损坏。删除损坏模型（`ollama rm <model>`）后重新下载。

### 模型加载后立即崩溃或无响应

模型下载成功，`ollama run` 进入 `>>>` 提示符，但输入内容后程序闪退或长时间无响应。这是典型的**内存不足**或**模型文件损坏**。

- **内存不足**：打开任务管理器 → 性能，确认**可用内存** ≥ 模型推荐值。1.5B 模型需 ≥ 3GB，7B 模型需 ≥ 6GB。若不足，关闭 Chrome 标签页、VS Code 等大型应用，或换用更小模型（如 `qwen2.5:0.5b`，仅 0.5GB）。
- **模型文件损坏**：运行 `ollama rm <model>` 删除，重新 `ollama pull`。如果下载过程不稳定，可使用 `ollama pull --insecure` 跳过 TLS 验证（仅用于测试，不推荐生产环境）。
- **CPU 不支持 AVX**：较老 CPU（如 2012 年以前）可能因缺少 AVX 指令集导致崩溃。在 `ollama serve` 的输出中查看有无 `CPU does not have AVX support` 字样。若出现，只能更换硬件或使用云端服务。

> 如果上述方法均未解决，建议卸载 Ollama，删除 `%USERPROFILE%\.ollama` 文件夹（备份模型），然后重新安装最新版安装程序。这是最稳妥的“核武器”方案，尤其适合那些系统环境混乱的用户。

这篇 **Ollama Windows 本地安装教程** 已覆盖绝大多数安装异常。若遇到未收录的问题，可查阅 Ollama 官方 issues 页面（https://github.com/ollama/ollama/issues），或运行 `ollama serve --verbose` 获取完整日志以寻求帮助。


---


## 进阶：配置Ollama服务与API调用
### 设置服务监听与跨域访问

默认情况下，Ollama只监听 `127.0.0.1:11434`，仅本机可访问。若想让局域网其他设备（或WSL 2）调用，需要修改环境变量。在 **系统环境变量** 中添加：

- `OLLAMA_HOST=0.0.0.0:11434`（允许所有IP）
- `OLLAMA_ORIGINS=*`（允许所有来源，仅开发环境使用）

设置后**重启Ollama**（通知栏右键退出，再重新双击 `OllamaSetup.exe`）。验证：在另一台设备浏览器访问 `http://<你的IP>:11434`，应返回 `Ollama is running`。

> 注意：暴露到公网有安全风险。生产环境应配合反向代理（如Nginx）添加鉴权，或只绑定内网IP。

### 使用curl测试API接口

Ollama提供RESTful API。无需额外启动Web服务，`ollama serve` 已在后台运行。用 `curl` 发送 `POST` 请求即可：

```bash
curl -X POST http://127.0.0.1:11434/api/generate -d '{
  "model": "deepseek-r1:1.5b",
  "prompt": "用一句话解释量子计算",
  "stream": false
}'
```

参数 `stream: false` 让Ollama一次性返回完整JSON，适合调试。响应中 `response` 字段即为生成文本。若需持续对话，改用 `/api/chat` 接口并传入 `messages` 数组。

### 用Python SDK编程调用

推荐安装 `ollama` Python库（版本≥0.4.0）。命令：

```bash
pip install ollama
```

脚本示例：

```python
import ollama

response = ollama.chat(
    model='deepseek-r1:1.5b',
    messages=[{'role': 'user', 'content': '鲁迅为什么打周树人？'}]
)
print(response['message']['content'])
```

首次运行会自动下载模型依赖（若模型尚未pull，Ollama会先下载）。`ollama.chat()` 默认使用流式输出，如需完整响应同上设置 `stream=False`。

> 如果报错 `Connection refused`，检查环境变量 `OLLAMA_HOST` 是否与代码中 `ollama.Client(host='http://127.0.0.1:11434')` 一致。

### 查看运行时模型列表与资源占用

通过 `ollama ps` 命令查看当前活跃模型及其占用情况。输出示例：

```
NAME                    ID              SIZE      PROCESSOR    UNTIL
deepseek-r1:1.5b        123abc...       1.1 GB    100% CPU     4m22s
```

`PROCESSOR` 列显示推理设备（CPU或GPU）。`UNTIL` 表示模型会在空闲多久后被卸载（默认5分钟）。如需强制立刻卸载，运行 `ollama stop deepseek-r1:1.5b`。

API接口对应：`GET /api/ps` 返回JSON格式的当前进程列表，可集成到监控面板。

本教程通过这一节展示了如何将Ollama从命令行工具扩展为可编程的服务，从而融入你的AI工作流。下一篇将讨论如何将模型集成到第三方应用（如ChatGPT-on-CLI或Obsidian插件）。


---


## 如何卸载与升级Ollama
### 卸载步骤

Ollama 的卸载不留下残留，推荐两种方式：

- **通过设置卸载**：打开 Windows 设置 → 应用 → 应用和功能，找到 **Ollama**，点击“卸载”。系统会提示确认，完成后删除 `%USERPROFILE%\.ollama` 文件夹。此文件夹保存了所有已下载模型和配置文件——如果需要保留模型用于重装后复用，把它复制到其他目录再删除。
- **命令行静默卸载**：适用于批量部署场景。找到 `OllamaSetup.exe` 的原始安装包，以管理员身份运行 `OllamaSetup.exe /uninstall`。卸载完成后同样手动清理 `.ollama` 文件夹。

> 如果之后计划重新安装本教程中的模型，建议先通过 `ollama list` 记录模型名称和大小，卸载前再用 `ollama push` 备份至私人仓库（或直接复制模型文件）。但最省事的做法是保留 `.ollama` 文件夹不动——重装后 Ollama 自动识别已有模型。

### 升级方法

Ollama 会提示有新版本，但 Windows 上不会自动升级。手动升级步骤：

1. **下载新版安装程序**：访问 [Ollama 官方下载页](https://ollama.com/download) 获取最新 `OllamaSetup.exe`。写此文时最新稳定版为 **0.5.11**。
2. **直接运行安装程序**：无需先卸载旧版。安装程序会自动检测并覆盖升级，保留现有模型和环境变量。
3. **验证版本**：在 PowerShell 中运行 `ollama --version`，输出应显示新版本号。

如果遇到升级后模型无法加载的极少数情况，执行 `ollama pull <model>` 重新下载兼容的新版模型文件即可。本 **Ollama Windows 本地安装教程** 中所有操作在升级后均无需重复配置——环境变量、代理设置、API 端口等保持不变。


---


## 总结
从最初检查系统兼容性到成功跑完 `deepseek-r1:1.5b`，你已经走完了这篇 **Ollama Windows 本地安装教程** 的完整流程。安装本身只需 **30 秒** 和一条命令，真正影响体验的是硬件规划与网络准备。以下是几条长期使用建议。

### 模型选择与硬件匹配
- **8GB 内存**：只跑 1.5B–3B 参数模型（如 `qwen2.5:1.5b`），推理时留出至少 3GB 空闲内存给系统。
- **16GB 内存**：可流畅运行 7B 模型（`deepseek-r1:7b` 或 `llama3.2:8b`），但不要同时打开多个大模型或多个浏览器标签页。
- **32GB+ 内存 + NVIDIA GPU（≥6GB 显存）**：可以尝试 13B–70B 模型，GPU 推理速度比 CPU 快 **3–5 倍**。用 `ollama ps` 确认模型确实跑在 GPU 上。
- **磁盘预留**：每个 7B 模型约 4–5GB，多模型用户建议至少留出 **30GB 空闲空间**。定期运行 `ollama rm <model>` 删除不再使用的模型，避免磁盘占满。

### 环境变量是核心配置入口
Ollama 在 Windows 上的配置主要通过环境变量完成，而非图形界面。建议在系统环境变量中设置以下三项：

- `OLLAMA_HOST=127.0.0.1:11434`（保持默认，仅本机访问）
- `OLLAMA_KEEP_ALIVE=5m`（模型空闲 5 分钟后卸载，可改为 `0` 立即卸载以释放内存）
- `OLLAMA_MODELS`（可选，将模型存储路径指向大容量磁盘，如 `D:\ollama_models`）

> 修改环境变量后必须重启 Ollama：右键托盘图标 → 退出，再重新运行 `ollama serve`。

### 安全与日常维护
- **只从 `ollama.com/download`** 下载安装程序。第三方打包版可能篡改注册表或捆绑程序。
- **防火墙规则**：如果开启了 `OLLAMA_HOST=0.0.0.0`，务必在 Windows 防火墙中限制来源 IP，只允许内网子网访问 11434 端口。
- **定期升级**：Ollama 每月发布 1–2 个版本，修复漏洞并优化推理性能。直接运行新版安装程序覆盖即可，模型和配置不受影响。
- **日志排查**：遇到异常先查看 `ollama serve --verbose` 的输出，比搜索网络更高效。

这篇教程的安装部分到此结束。如果你需要将 Ollama 集成到代码编辑器、自动化脚本或家庭服务器中，下一段可以关注 **Ollama 环境变量的完整参考** 和 **通过 Docker 部署的差异**——两者都能进一步拓展本地 AI 的使用场景。