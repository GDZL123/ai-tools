---
date: '2026-05-11T13:33:23+08:00'
draft: false
title: 'ComfyUI Windows 安装教程：新手一步步图文指南'
---


> 这篇文章解决新手在 Windows 上安装 ComfyUI 时经常遇到的版本选择混乱和运行失败问题。通过这篇 ComfyUI Windows 安装教程 新手，你会掌握使用官方安装包和便携版两种方法，从下载、解压到启动的全部步骤，以及避开常见错误的技巧。


## 检查系统要求与下载准备
在安装之前，先确认你的电脑满足最低要求。ComfyUI 依赖 **Python 3.10 或 3.11**（官方推荐 3.10.11），以及 **NVIDIA 显卡驱动**（至少 525 或更新版本）。如果你使用的是 AMD 或 Intel 集成显卡，流程稍有不同，但本教程以 **NVIDIA GPU + Windows 10/11 64 位** 为准。

**关键的准备工作有两项：**

- 前往 [NVIDIA 官网](https://www.nvidia.com/Download/index.aspx) 下载并安装最新驱动。旧驱动（低于 525）会导致 CUDA 组件不可用，ComfyUI 启动时报 `CUDA error: no kernel image is available`。
- 确认系统已经安装了 **Git**，用于后续拉取自定义节点。如果未安装，从 [git-scm.com](https://git-scm.com/) 下载默认选项安装即可。

> 注意：如果你的系统盘空间紧张，请确保 ComfyUI 安装路径所在盘有 **至少 20GB 空闲空间**（仅程序本体 + 一个 SD 模型文件）。

下载官方包有两种选择。在本文所述的 **ComfyUI Windows 安装教程 新手** 流程中，我推荐使用 **Windows 便携版**，因为它无需手动配置 Python 环境，开箱即用。下载地址：

- 官方桌面版安装包：[ComfyUI Desktop (Windows)](https://docs.comfy.org/zh/installation/desktop/windows) – 自带安装向导，但版本更新稍慢。
- 便携版（本文使用）：从 [GitHub Releases](https://github.com/comfyanonymous/ComfyUI/releases) 下载 `ComfyUI_windows_portable_nvidia.7z`。当前最新（2025年5月）为 v0.3.9，文件约 2.1GB。

**下载后务必做两件事：**
1. 使用 **7-Zip** 而非系统自带解压工具，避免解压过程中文件损坏或路径过长报错。
2. 将解压后的文件夹放在 **非中文、无空格** 的路径下，例如 `D:\ComfyUI`。中文路径会导致 Python 导入模块时出现 `SyntaxError`。


---


## 使用官方安装包一键安装
双击官方安装包安装，是新手最直接的上手方式，不需要敲命令或配置环境变量。下载的 `.exe` 文件（约 1.8GB）是一个完整的桌面应用程序，安装过程由向导引导。

**桌面版安装包 vs. 便携版的选择：**

- **桌面版**：自带自动更新，安装时可选定制组件（如是否安装 VC++ 运行库），但更新版本通常滞后便携版 1-2 周。
- **便携版**：解压即用，版本最新，但更新时需要手动覆盖文件（可保留 `models` 文件夹和 `custom_nodes` 文件夹）。
- 如果你不确定选哪个，**我推荐便携版**——它更灵活，后续迁移也很方便。

**安装桌面版（如果选择）：**

1. 双击 `ComfyUI_Desktop_Setup.exe`，一路点击“下一步”。
2. 安装路径建议改为 `D:\ComfyUI`（任何非中文、无空格的盘符），避免 C 盘空间不足。
3. 安装完成后，桌面生成启动快捷方式。双击启动，首次运行会自检 CUDA 和 PyTorch 版本，耗时约 2-5 分钟。

**安装便携版（强烈推荐，本教程使用）：**

1. 确保已经用 **7-Zip** 将 `ComfyUI_windows_portable_nvidia.7z` 解压到纯英文路径下，例如 `D:\ComfyUI`。
2. 进入解压后的文件夹，找到 `run_nvidia_gpu.bat`，**右键 → 以管理员身份运行**。
3. 终端窗口会闪动，自动下载初次运行所需的依赖。等待输出信息中出现 `To see the GUI go to: http://127.0.0.1:8188`。

> 注意：首次运行如果提示“缺少 vcruntime140.dll”，则需要安装 [VC++ 2015-2022 Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)，这是几乎所有 Windows 图形软件的前提条件。

**常见错误与处理：**

- 启动后浏览器打开空白页面：检查终端是否报 `CUDA out of memory`，这是显存不足。在 `webui.bat` 同目录下创建 `--lowvram` 的快捷方式或直接修改 `run_nvidia_gpu.bat`，在 `main.py` 后面追加 `--lowvram`。
- 双击 `.bat` 文件无反应：用记事本打开它，检查第一行 `@echo off` 下是否有乱码，保存为 **ANSI 编码** 再运行。
- 报错 `No module named 'torch'`：说明 Python 环境未加载。便携版已内置嵌入的 Python，不要手动去系统路径中安装 PyTorch。

> 提示：若你已有从其他渠道下载的 Stable Diffusion 模型（如 `sd_xl_base_1.0.safetensors`），可以直接复制到 `ComfyUI\models\checkpoints\` 目录下，重启后即可使用。

通过这个 ComfyUI Windows 安装教程 新手的步骤，安装包已经就绪。现在文件夹内会有一个干净的 ComfyUI 界面，你可以马上打开浏览器访问 `http://127.0.0.1:8188`，一个空白工作流等待你拖入节点。要让它真正跑起来，还需要加载一个 SD 模型文件。


---


## 使用第三方整合包快速起步
对于不想手动管理几十个自定义节点的新手，第三方整合包是更省事的选择。它直接预装了你可能需要的大部分节点，下载解压就能用，省去逐个克隆仓库的麻烦。

**推荐整合包：YanWenKun/ComfyUI-Windows-Portable**

这是目前社区最活跃的第三方打包方案，基于官方便携版改造，内置 **40+ 常见自定义节点**，例如 ControlNet、AnimateDiff、IP-Adapter 等。它的 GitHub 仓库（[YanWenKun/ComfyUI-Windows-Portable](https://github.com/YanWenKun/ComfyUI-Windows-Portable)）提供两个版本：

- **完整版**（约 3.5GB）：含 ComfyUI 本体 + 预装节点，**不含 SD 模型**。
- **轻量版**：仅包含核心节点，约 800MB。

**使用步骤：**

1. 在 Releases 页面下载最新 `.7z` 文件（当前 v2025.05，约 3.5GB）。使用 **7-Zip** 解压到纯英文路径，例如 `D:\ComfyUI_Portable`。
2. 进入 `ComfyUI_Windows_Portable` 文件夹，双击 `run_nvidia_gpu.bat`（无需管理员身份，普通双击即可）。首次运行会检查 Python 环境和节点依赖，耗时约 1-2 分钟。
3. 终端出现 `Starting server... http://127.0.0.1:8188` 后，浏览器打开该地址即可看到工作区。

> 注意：整合包不包含 Stable Diffusion 模型文件，你需要自行将 `.safetensors` 或 `.ckpt` 文件放入 `ComfyUI\models\checkpoints\` 文件夹。若已有模型，复制进去后刷新网页即可在节点中选到。

**与官方便携版的主要区别：**

- **节点预装**：官方版仅含极少数基础节点，整合包直接带齐 ControlNet 辅助、视频工具、区域重绘等高频节点，无需再逐个安装。
- **配置微调**：作者已优化了 `extra_model_paths.yaml`，多模型路径自动识别；同时预设了 `--highvram`（8GB+显存可用）和 `--lowvram`（4GB 以下）的启动参数，你只需在 `.bat` 文件中注释或取消注释对应行即可切换。
- **更新机制**：版本更新时，下载新包并覆盖除 `models`、`custom_nodes`、`input`、`output` 文件夹以外的内容即可，旧配置和模型保留。

如果你希望快速体验 ComfyUI 的完整生态，这个整合包是当前最成熟的解决方案。一个典型的 **ComfyUI Windows 安装教程 新手** 场景是：解压 → 放模型 → 双击运行 → 浏览器打开。整个流程不到 5 分钟。

整合包启动后，你会看到空白工作流。接下来需要往 canvas 上拖入第一个节点——**CheckpointLoaderSimple**，然后选择你放入的模型文件。


---


## 放置模型文件与基础配置
`ComfyUI\models\` 是 ComfyUI 所有模型文件的根目录。每个模型类型对应一个子文件夹，**必须放置准确**，否则节点加载时会报 `failed to load checkpoint` 或 `no such file`。

### 模型目录结构

解压后的 `models` 目录下默认有这些子文件夹：

- **checkpoints**：主模型（`.safetensors` 或 `.ckpt`），Stable Diffusion 1.5 / XL / 3 等都在这里。单个文件 2–7GB。
- **vae**：VAE 模型，用于改善色彩和细节。可选，但建议放入配套 VAE（如 `vae-ft-mse-840000`）。
- **loras**：LoRA 微调模型，文件通常 50–300MB。
- **controlnet**：ControlNet 模型，用于姿态、深度、边缘控制。文件名通常包含 `control_v11` 或 `controlnet`。
- **upscale_models**：放大模型，如 ESRGAN、4x-UltraSharp。
- **embeddings**：Textual Inversion 嵌入（`.pt` 或 `.safetensors`），文件几十 KB。
- **clip**：CLIP 模型，用于文本编码。便携版已自带，一般无需改动。

> 如果你从其他来源（如 SD WebUI）复制模型，直接复制 `.safetensors` 文件到对应目录即可。**不要随意修改文件名中`/`或特殊符号**，Python 解析路径时会报错。

### 基础配置：启动参数与系统设置

启动 `run_nvidia_gpu.bat` 前，**建议用记事本编辑该文件**，在最后一行 `main.py` 后面添加参数。常用参数：

- `--lowvram`：显存低于 6GB 时启用，降低 GPU 占用，牺牲部分速度。
- `--highvram`：显存 12GB+ 时使用，模型常驻显存，速度最快。
- `--port 8189`：默认 8188 被占用时，更换端口。
- `--listen 0.0.0.0`：允许局域网内其他设备访问 WebUI（注意防火墙）。
- `--force-fp16`：强制半精度推理，减少显存占用（部分模型不兼容）。

示例修改后的一行（以 8GB 显存为例）：
```
.\python_embeded\python.exe -s ComfyUI\main.py --windows-standalone-build --highvram
```

**另存为 ANSI 编码**：如果文件中出现乱码（比如中文注释），用记事本“另存为”时选择编码“ANSI”，否则终端输出乱码且可能无法启动。

### 配置外部模型路径

如果你已经在 Windows 上安装了 SD WebUI，模型文件重复占用双倍磁盘空间。ComfyUI 支持通过 `extra_model_paths.yaml` 加载外部目录。

1. 复制 `ComfyUI\extra_model_paths.yaml.example` 为 `extra_model_paths.yaml`（去掉 `.example`）。
2. 用记事本打开，找到 `stable-diffusion-webui` 部分，将 `base_path` 改为你的 WebUI 根路径，例如：
   ```yaml
   stable-diffusion-webui:
        base_path: D:\stable-diffusion-webui\
        checkpoints: models\Stable-diffusion\
        vae: models\VAE\
        loras: models\Lora\
        controlnet: extensions\sd-webui-controlnet\models\
   ```
3. 保存后重启 ComfyUI。现在在 CheckpointLoaderSimple 节点里就能直接选到 WebUI 目录下的模型，**无需复制文件**。

> 路径分隔符一律用反斜杠 `\`，且**不要以反斜杠结尾**（除非指定了子目录）。YAML 缩进使用两个空格，不要用 Tab。

通过这个 **ComfyUI Windows 安装教程 新手** 的配置步骤，模型文件就和 ComfyUI 绑定在了一起。启动后，你会在 CheckpointLoaderSimple 节点的下拉菜单中看到所有模型名称；如果空白，检查目录是否正确或刷新页面。


---


## 首次启动与界面概览
双击 `run_nvidia_gpu.bat` 后，终端窗口滚动输出依赖检查信息，最后一行显示 `To see the GUI go to: http://127.0.0.1:8188`。**这条消息才是启动成功的标志**，而不是终端窗口消失或出现乱码。打开 Chrome/Edge，输入该地址，回车，看到浅灰色背景的空白画布，就是 ComfyUI 的主界面。

### 主界面由三个核心区域组成

- **顶部菜单栏**：左起依次是 `File`（新建、加载工作流）、`Queue`（当前任务队列）、`History`（已生成图像）、`View`（缩放、对齐网格）。新手最常用的是 `File → Load Default` 加载官方示例工作流，以及 `Queue Prompt` 按钮（快捷键 `Ctrl+Enter`）提交生成任务。
- **左侧节点面板**：默认显示 **Node Menu**，分类罗列所有可用节点，例如 `Loaders`、`Samplers`、`Conditioning`。**如果节点列表为空**，检查终端是否报 `No module named 'custom_nodes'`——便携版已内置节点，但首次运行需要联网下载依赖，若网络被墙则需手动安装。可以在面板右上角的搜索框直接输入节点名过滤。
- **中央画布**：拖入节点后显示在此处，支持鼠标滚轮缩放、按住 `鼠标中键` 平移。节点之间的连线从输出端口（右侧圆点）拖到输入端口（左侧圆点）即可建立数据流。

> 启动后若看到左上角红色提示 `Missing Node: ... `，说明当前工作流引用了未经安装的自定义节点。本教程使用的官方便携版/整合包已包含常用节点，不会报错。如果使用纯净官方版，需手动从 GitHub 克隆对应仓库到 `custom_nodes\` 文件夹。

画布右侧还有一个 **属性面板**，点击任意节点后显示其参数。例如拖入一个 `CheckpointLoaderSimple` 节点（位于 Loaders 分类），属性面板会出现模型选择下拉菜单——**此处应能看到你之前放入 `models\checkpoints\` 的模型文件名**。如果下拉列表空白，刷新页面或重启 ComfyUI。

**首次启动后建议做两件事**：
1. 按下 `Ctrl+Enter` 提交空白工作流（会报错，但能确认服务端响应正常）。终端输出 `Prompt executed in 0.0 seconds` 则网络层面无问题。
2. 在节点面板搜索 `KSampler`，拖入画布，连线一个最小推理流程（CheckpointLoader → CLIPTextEncode → KSampler → VAEDecode → SaveImage）——这一步验证模型加载和 GPU 调用是否成功。

界面的各个元素都可以通过 `View → Toggle Node Panel` 或快捷键 `Tab` 隐藏/显示。这个 **ComfyUI Windows 安装教程 新手** 的环境至此搭建完毕，画布上的下一个操作，就是拖入第一个节点并加载模型。


---


## 安装必备自定义节点与插件
官方便携版只包含最基本的加载和采样节点。要运行ControlNet、AnimateDiff、IP-Adapter等工作流，必须手动安装**自定义节点**。安装前，确保ComfyUI已完整关闭，终端窗口已退出。

**两种安装方式：**

- **使用Git克隆（推荐）**：打开终端（CMD），`cd`到`ComfyUI\custom_nodes\`目录，执行命令 `git clone https://github.com/ltdrdata/ComfyUI-Manager.git`。**这是最常用的节点管理器**，安装后可在ComfyUI界面内直接搜索、安装、更新其他节点。
- **直接下载ZIP**：访问节点的GitHub仓库主页，点击`Code → Download ZIP`。将ZIP文件内容解压到`ComfyUI\custom_nodes\`下，确保每个节点一个独立文件夹，例如`ComfyUI-Manager`。解压后文件夹名称必须与仓库名一致，否则ComfyUI不识别。

> 注意：从GitHub克隆或下载ZIP时，请关闭任何VPN或代理工具。部分节点依赖国内镜像站点安装额外依赖，VPN会导致连接失败。如果你有技术背景，可以在终端设置代理环境变量 `set http_proxy=http://127.0.0.1:7890`，但新手建议直连。

**安装节点管理器后的操作：**

重启ComfyUI，浏览器刷新后，顶部菜单栏会多出 **Manager** 菜单。点击它，选择`Install Custom Nodes`，在弹出的搜索框中输入节点名（例如`ComfyUI-AnimateDiff-Evolved`），点击`Install`。管理器会自动处理Git克隆和依赖安装。

**新手必装的5个节点：**

- **ComfyUI-Manager**：安装节点、更新、备份工作流的核心工具。
- **ComfyUI-Impact-Pack**：提供Inpaint、Segment Anything等高级图像处理。
- **ComfyUI-AnimateDiff-Evolved**：视频生成与动画（需额外下载运动模块模型）。
- **ComfyUI-IPAdapter_plus**：图像提示词适配器，用于风格迁移、参考图。
- **Efficiency Nodes**：精简工作流，用单个节点替代多个标准节点。

**常见错误修复：**

- 启动后报错`ModuleNotFoundError: No module named 'xxx'`：说明节点依赖的Python包未安装。打开`custom_nodes\该节点文件夹\requirements.txt`，查看需安装的包。然后在终端中执行 `python -m pip install -r requirements.txt`（便携版用户：`.\python_embeded\python.exe -m pip install -r requirements.txt`）。
- 工作流保存后出现红色节点：重新安装该节点或检查`custom_nodes`文件夹内是否有同名的重复文件夹，删除一个即可。
- 节点管理器搜索不出结果：检查是否为最新版本。在`custom_nodes\ComfyUI-Manager`下执行`git pull`更新，或直接删除文件夹重新克隆。

通过这个 **ComfyUI Windows安装教程 新手** 的节点安装步骤，你现在拥有了一个可扩展的ComfyUI环境。节点管理器已经就绪，任何社区节点都可以一键添加。


---


## 运行第一个文生图工作流
现在进入实际操作环节。双击 `run_nvidia_gpu.bat` 确保 ComfyUI 已启动，浏览器打开后，画布上一片空白。**你的第一个任务是搭建一条最小推理链路**——从加载模型到保存图像，共6个节点。

### 拖入核心节点

在左侧节点面板的搜索框中依次输入以下节点名，拖入画布：

1. **CheckpointLoaderSimple**：位于 `Loaders` 分类。拖入后，属性面板会显示模型下拉菜单——**确保已出现你放入 `models\checkpoints\` 的模型文件名**，例如 `sd_xl_base_1.0.safetensors`。如果列表为空，刷新页面或重启 ComfyUI。
2. **CLIPTextEncode**（需要两个）：分别用于正面提示词和负面提示词。搜索 `CLIPTextEncode` 拖入两次。第一个节点重命名为 `positive`（双击节点标签），第二个重命名为 `negative`。
3. **KSampler**：位于 `Samplers` 分类。这是采样核心，控制步数、CFG、种子等参数。
4. **VAEDecode**：将潜在空间表示解码为像素图像。
5. **SaveImage**：将最终图像保存到 `output\` 文件夹。

### 连接节点（顺序很重要）

从输出端口（右侧圆点）拖向输入端口（左侧圆点）：

- **CheckpointLoaderSimple → CLIPTextEncode (positive)**：`CheckpointLoaderSimple` 的 `CLIP` 输出口连接到 `positive` 节点的 `clip` 输入口。
- **CheckpointLoaderSimple → CLIPTextEncode (negative)**：同样用 `CLIP` 输出连接第二个节点的 `clip` 输入口。
- **CheckpointLoaderSimple → KSampler**：`CheckpointLoaderSimple` 的 `model` 输出口连接到 KSampler 的 `model` 输入口。
- **positive CLIPTextEncode → KSampler**：`positive` 节点的输出口（唯一）连到 KSampler 的 `positive` 输入口。
- **negative CLIPTextEncode → KSampler**：同理，连接到 `negative` 输入口。
- **KSampler → VAEDecode**：KSampler 的 `latent` 输出口连到 VAEDecode 的 `samples` 输入口。
- **VAEDecode → SaveImage**：VAEDecode 的 `image` 输出口连到 SaveImage 的 `images` 输入口。

连接完成后，画布应类似一条从左到右的主链路。**若某个端口旁出现红色高亮，说明连接类型不匹配**——检查是否拖错了端口（例如将 `model` 输出连到了 `clip` 输入）。

### 设置生成参数并运行

双击 KSampler 节点展开属性面板：

- **steps**：首次运行设为 `20`（平衡速度与质量）。
- **cfg**：保持默认 `8`。
- **sampler_name**：`euler`（通用采样器）。
- **scheduler**：`normal`。
- **denoise**：`1.0`（文生图模型不需要降噪）。

双击两个 CLIPTextEncode 节点，在 `text` 字段中输入提示词。正面写 `a cute cat, high quality, detailed`，负面写 `ugly, blurry, low quality`。**提示词可以是中文**，但建议用英文短语以提升模型理解。

点击顶部菜单栏的 **Queue Prompt** 按钮（或按快捷键 `Ctrl+Enter`）。终端窗口会显示加载模型进度条：`Loading checkpoint: sd_xl_base_1.0`。首次加载可能需要 30-60 秒（取决于模型大小和硬盘速度）。**如果终端报错 `CUDA out of memory`**，减小 `steps` 或 `batch_size`（在 KSampler 中），或者在启动参数中添加 `--lowvram`。

生成完成后，画布下方会弹出一个小窗口，显示生成的预览图。同时 `ComfyUI\output\` 文件夹中会出现一个 PNG 文件（命名格式 `ComfyUI_00001_.png`）。**右键该文件可打开“在资源管理器中显示”**。

> 如果预览图全黑或完全是噪点，检查模型是否已损坏——换一个 `.safetensors` 格式的模型重试。便携版和整合包预置的 `sd_xl_base_1.0` 是推荐的首选模型。

这个 **ComfyUI Windows 安装教程 新手** 环境中的第一个文生图工作流已经跑通。后续可以在此基础上添加 ControlNet、LoRA 等节点，但核心链路始终不变：模型加载 → 编码 → 采样 → 解码 → 保存。


---


## 常见安装问题与解决方法
### 启动时黑窗口一闪而逝

这是最常见的错误，通常由**显卡驱动不兼容**或**缺失VC++运行库**引起。先确认你已安装最新版NVIDIA驱动（至少需要 **545.92** 版本）。打开 `ComfyUI\run_nvidia_gpu.bat` 右键编辑，查看 `set CUDA_VISIBLE_DEVICES=0` 这一行——如果你的显卡有多个GPU，保留 `0` 即可，单卡默认正确。若仍闪退，安装 [VC++ 2015-2022 Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)（64位版本）。完成后双击 `run_nvidia_gpu.bat`，终端窗口应正常显示启动日志。

> 注意：如果你的系统是Windows 10 20H2以下，便携版可能无法启动，建议升级系统或使用整合包。

### 浏览器无法打开 ComfyUI

启动后终端显示 `Starting server on 127.0.0.1:8188`，但Chrome/Edge访问 `http://127.0.0.1:8188` 一直白屏或超时。**先检查端口是否被占用**：在终端按 `Ctrl+C` 停止，然后执行命令 `netstat -ano | findstr :8188`。如果有输出占用进程，终止该进程（记下PID后通过任务管理器结束），或修改启动参数改用其他端口：用记事本打开 `run_nvidia_gpu.bat`，在 `python main.py` 后面加上 `--port 8189`，保存后重新运行。

### 加载模型时提示“CUDA out of memory”

当使用SDXL模型（约6-7GB显存）且显存低于8GB时容易触发。**彻底解决**：在`run_nvidia_gpu.bat`的`python main.py`后面添加 `--lowvram` 参数，保存后重启。此参数会降低显存占用，但生成速度会变慢约20%-30%。如果显存只有4GB，建议使用SD1.5模型（约2GB）。另外，关闭后台其他占用显卡的程序（如浏览器硬件加速、视频渲染等）。

### 终端报错“No module named 'torch'”

便携版自带Python和Torch，但有时用户误删了 `python_embeded` 文件夹或文件不完整。**修复方法**：重新下载官方便携包 [ComfyUI_windows_portable_nvidia.7z](https://github.com/comfyanonymous/ComfyUI/releases) 解压覆盖原目录（不要删除 `models` 文件夹）。如果使用整合包，检查安装目录下是否有 `python_embeded\python.exe` 存在。若缺失，需重新解压整合包。

### 模型文件不显示在加载列表中

模型放入 `ComfyUI\models\checkpoints\` 后，刷新ComfyUI界面（F5）或重启程序，下拉菜单仍没有文件。**常见原因**：模型文件名后缀必须是 `.safetensors` 或 `.ckpt`，且不能有中文字符。将文件名改为纯英文（例如 `sd_xl_base_1.0.safetensors`）。若仍不显示，检查文件是否损坏——尝试用其他模型（如官方示例模型 `v1-5-pruned-emaonly.safetensors`）验证。另一个可能性：你使用了整合包，模型路径可能不同，请确认整合包说明中指定的模型目录。

**注意**：本 **ComfyUI Windows 安装教程 新手** 中所有模型放置规则均遵循官方标准路径。如果使用第三方整合包（如 [YanWenKun/ComfyUI-Windows-Portable](https://github.com/YanWenKun/ComfyUI-Windows-Portable)），其模型目录可能为 `ComfyUI\models\checkpoints` 不变，但预装多个自定义节点，启动时更慢属正常现象。

### 生成图像全黑或黑白噪点

排除模型损坏后，检查工作流连接：确保 `VAEDecode` 节点正确接收了 `KSampler` 的 `latent` 输出。若连接正确，问题可能出在**参数设置**。`KSampler` 中的 `denoise` 设置为 `1.0`（文生图无误），`cfg` 设为 7-8，`steps` 设为 20。若使用了 `scheduler` 为 `ddim_uniform` 可能不稳定，切换到 `euler` 或 `normal`。尝试恢复默认工作流：点击 ComfyUI 界面右侧的 **Load Default** 按钮，会载入一个标准文生图模板。

### 端口冲突导致“Address already in use”

如果之前运行的 ComfyUI 没有正确关闭，再次启动时会出现此错误。**解决**：在终端执行 `taskkill /f /im python.exe` 强制结束所有Python进程。然后重新运行 `run_nvidia_gpu.bat`。如果常用多个ComfyUI实例，建议为不同实例分配不同端口（如8188和8189）。


---


## 总结
### 配置备份与迁移建议

当你花时间调通工作流、装好自定义节点后，**备份 `custom_nodes` 和 `models` 文件夹**是最值得做的事。这两个文件夹占用了你绝大部分的安装精力。具体做法：将 `ComfyUI\custom_nodes` 和 `ComfyUI\models` 复制到另一个盘或网盘根目录，命名如 `ComfyUI_backup_2025-05`。下次重装系统或换电脑时，解压新版便携包，直接**覆盖**这两个文件夹即可恢复原有环境。模型文件很大（单个SDXL约6GB），建议只备份 `models\checkpoints` 中你真正常用的2-3个模型，其余按需下载。

> 注意：`extra_model_paths.yaml` 的配置路径与当前系统盘符绑定。迁移到新电脑后，记得用记事本修改 `base_path` 指向的盘符（例如从 `D:` 改为 `E:`），否则外部模型路径会失效。

### 学习资源与进阶路径

安装只是门槛，更多技巧在于工作流设计。推荐三个最高效的学习渠道：

- **官方示例工作流**：在ComfyUI界面点击 `Load Default`，手抄并理解每个节点的作用。这是最直接的入门方式。
- **OpenArt 工作流分享站**：访问 [openart.ai/workflows](https://openart.ai/workflows)，搜索“ComfyUI workflow”——大多数带有预览图和下载链接。下载 `.json` 文件拖入画布即可加载。
- **B站UP主“秋葉aaaki”系列教程**：该UP主持续更新ComfyUI节点详解视频，尤其针对ControlNet和AnimateDiff的配置。视频中会标注当前使用的ComfyUI版本（例如 v0.3.9）和PyTorch版本（2.1.0），对照你现在的环境可避免版本不兼容问题。

当你需要某个特定效果（如换脸、视频转绘），优先在GitHub搜索 `ComfyUI-` 前缀的仓库，README中通常有工作流截图和节点安装说明。

### 环境维护与社区支持

保持环境稳定比安装新功能更重要。**养成两个习惯**：每周运行一次 `git pull` 更新节点（在 `custom_nodes\` 子文件夹下逐目录执行）；每次更新节点前，用ComfyUI Manager的 `Backup Workflows` 功能保存当前工作流。如果更新后某节点报错，回滚方法：在 `custom_nodes` 中找到该文件夹，执行 `git log` 查看提交记录，`git checkout <上次正常提交的hash>` 还原。

> 当你在操作中遇到本文没有覆盖的报错，将终端日志完整复制到 [ComfyUI Issues](https://github.com/comfyanonymous/ComfyUI/issues) 搜索框，十有八九已有解决方案。

这套 **ComfyUI Windows 安装教程 新手** 的流程完成后，你已经具备从零搭建生成环境的全部基础技能。接下来所有高级功能——视频生成、3D模型导出、实时绘画——都是在这个画布上不断添加新节点和连线而已。