+++
title = '如何用Stable Diffusion WebUI入门AI绘图'
date = '2026-05-11'
draft = false
tags = ['create']
+++

> 折腾三小时装环境、显卡驱动报错、命令行弹窗乱飞——这是很多人入坑AI绘图的真实起点。**Stable Diffusion WebUI 入门**不需要你啃代码或搞深度学习，下载解压点几下就能跑出第一张图。这篇教程从零开始，20分钟内让你记住操作逻辑，避开新手最常踩的五个坑。


## Stable Diffusion WebUI 入门：软件安装与环境配置
## 环境与硬件准备

**Stable Diffusion WebUI 入门**的第一步不是下载软件，而是确认你的硬件能否跑起来。文本生成图像对显卡要求非常高，尤其是显存。

- **显卡**：必须为 NVIDIA 独立显卡，显存至少 **4GB**（6GB 以上更稳妥）。AMD 或 Intel 显卡也可用，但需要额外配置 DirectML 或 ROCm 分支，新手建议直接上 NVIDIA。
- **内存**：至少 **16GB** RAM。若低于此，启动时可能直接报错退出。
- **磁盘空间**：运行至少需要 **20GB** 剩余空间，其中模型文件本身约 2–7GB。
- **操作系统**：Windows 10/11 或 Linux（Ubuntu 22.04 测试最稳定）。macOS 不支持官方 Stable Diffusion 模型，需用专用 fork。

如果你用的是笔记本或轻薄本，很大概率显存不足。此时可先试 **`--medvram`** 启动参数，牺牲速度换取稳定性。

> 显存不足是新手最常见的问题，不是技术问题，是物理限制。把启动参数记下来——`--medvram` 或 `--lowvram`。

---

## 安装核心依赖

1. **安装 Python**：下载 [Python 3.10.6](https://www.python.org/downloads/release/python-3106/)（务必准确到这个版本，3.11+ 可能兼容性问题）。安装时勾选 **“Add Python to PATH”**。
2. **安装 Git**：从 [git-scm.com](https://git-scm.com/) 下载当前版，一路默认即可。用于从 GitHub 拉取代码。
3. **下载 WebUI**：打开命令提示符（cmd），进入你想存放的文件夹，执行：
   ```bash
   git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
   ```
   如果网络慢，可使用国内镜像（如 `git clone https://github.com.cnpmjs.org/AUTOMATIC1111/stable-diffusion-webui.git`），但注意镜像可能滞后 1–2 天。

---

## 首次启动与常见修复

克隆完成后，双击 `webui-user.bat`（Windows）或运行 `./webui.sh`（Linux）。首次启动会自动下载 pytorch、xformers 等依赖，耗时 10–30 分钟。

**常见错误与解决：**

- **“No module named torch”**：通常因为 Python 版本不对。检查 `python --version` 是否为 3.10.x。
- **“CUDA out of memory”**：关闭浏览器标签页，减少后台应用。或在 `webui-user.bat` 中给 `COMMANDLINE_ARGS` 添加 `--medvram`。
- **“Failed to install packages”**：尝试使用代理或换国内 pip 镜像。修改 `webui-user.bat`，在 `set COMMANDLINE_ARGS=` 上一行添加：
  ```bash
  set PIP_EXTRA_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
  ```

启动成功后，浏览器会自动打开 `http://127.0.0.1:7860`，你可以看到 Stable Diffusion WebUI 的主界面。如果浏览器没弹窗，手动输入这个地址即可。

> 第一次启动慢是正常的，第二次起会快很多。若中间卡住超过 10 分钟，按 `Ctrl+C` 中断，重新运行。不要反复尝试同一条崩溃命令，先加启动参数。

---

## 验证安装

在界面上方的 **prompt** 输入框里随便写一句英文（如 `astronaut riding a horse`），点击 **Generate**。等几十秒，一张 512×512 的图片就会出现在右侧。如果你看到了画面，说明 **Stable Diffusion WebUI 入门**的环境配置已经完成了。


---


## 文生图基础操作：从提示词到第一张图片
打开 WebUI 后，你看到的主界面分三块：左上角是提示词输入区，右侧是图像预览，下方是参数面板。**Stable Diffusion WebUI 入门**的核心操作就是填充左侧的两个输入框，然后点 Generate。

## 写提示词：正面与反面

**正向提示词（Prompt）** 描述你想要的画面，用英文单词或短语，逗号分隔。例如：`a majestic dragon perched on a castle tower, sunset sky, highly detailed, digital painting, artstation`。**负面提示词（Negative Prompt）** 排除你不想看到的东西，新手最常用的组合是：`nsfw, ugly, blurry, low quality, deformed, extra limbs, bad anatomy`。

- 提示词权重控制：用 `(word:1.2)` 提高某词影响力，`(word:0.8)` 降低。括号层数越多权重越大，例如 `((dragon))` 比 `(dragon)` 更强调。
- 风格关键词：在末尾加 `art by greg rutkowski, cinematic lighting` 可快速获得特定美术风格，但个别画师名字可能被模型较难识别。
- **负面提示词别漏**：空着的话，模型容易生成粗糙、重复的画面。把上述负面词存成一个文本，每次复制粘贴。

> 新手最常见的错误：只写正面提示词，忽略负面。结果生成的人脸多一根手指或背景模糊——加几个负面词基本能解决。

## 参数设置：跑出第一张图

主界面右侧基本参数默认值已能工作。几项关键参数需理解：

- **Sampling steps**：采样步数，默认 **20**。步数越高细节越丰富，但超过 30 收益递减。20–25 是多数模型的最优区间。
- **Sampling method**：采样器，推荐 `Euler a`（速度快，风格柔和）或 `DPM++ 2M Karras`（细节更锐利，步数 20–30）。
- **Width / Height**：默认 **512×512**。这是多数模型训练的基础尺寸，改太大（如 1024）会显存溢出或图像变形。若需要 4:3 或 16:9，用 512×768 或 768×512 更稳妥。
- **CFG Scale**：提示词相关度，默认 **7**。值越大，模型越严格遵循提示词，但超过 12 会让画面僵硬或过饱和。4–10 是常用范围。
- **Seed**：随机种子。**-1** 表示每次随机。固定一个种子（例如 `123456`）后，相同参数可复现同一画面。调试时建议固定种子，方便对比参数变化的影响。

在提示词输入框填入 `astronaut riding a horse`，负面提示词填上面的负面清单，采样器选 `Euler a`，步数 20，尺寸 512×512，点击 **Generate**。几十秒后，右侧出现图片——这就是你的第一张图。

> 如果图片全是噪点或完全黑屏，检查步骤数是否过低（<10），或者正面提示词为空。另外，显存不足时建议更小尺寸（如 384×384）加上 `--medvram` 参数。

## 保存与批量生成

生成后图片自动保存在 `outputs/txt2img-images` 文件夹，按日期分类。你还可以用 **Batch count**（批次数量）和 **Batch size**（每批图片数）一次生成多张。例如 Batch count=4，Batch size=1，生成 4 张不同种子图。Batch size 增加会同时占用更多显存，新手只调 Batch count 即可。

掌握这些，你就能自由组合提示词与参数，每次点击生成都会看到不同的结果。当你对画面不满意时，下一步就是更换模型——不同的 checkpoint 会完全改变画风。


---


## 图片生成核心参数详解：采样器、步数与CFG Scale
采样器决定了噪声逐步还原为画面的路径，不同采样器对细节和速度影响显著。**Stable Diffusion WebUI 入门**用户常纠结选哪个，其实只需记住三类：

- **Euler / Euler a**：速度最快，风格偏柔和，适合快速出图或测试提示词。步数≤20时效果稳定。
- **DPM++ 2M Karras**：细节更锐利，光影对比强，推荐步数20–30。新手首选，兼顾质量与速度。
- **DDIM**：可还原性强（相同种子+步数能复现），但风格偏平淡，较少用于常规文生图。

其他如 LMS、Heun 差异细微，同组别选一个记住即可。若显存紧张，选 **Euler a** 省资源；追求锐度选 **DPM++ 2M Karras**。

---

## 步数：不是越多越好

步数（Sampling steps）控制噪声去除过程的迭代次数。多数模型在 **20–25 步** 达到最佳细节，超过 30 步带来的提升肉眼几乎不可察觉，反而拖慢生成速度。实测对比：

- 10 步：画面模糊，主体轮廓尚可。
- 20 步：细节丰富，纹理清晰。
- 40 步：与 25 步差异极小，生成时间翻倍。

> 固定种子，用 15、20、25、30 各跑一张，你会发现 20–25 是性价比拐点。显存不足时降到 15 也能接受。

---

## CFG Scale：提示词紧箍咒

CFG Scale 控制模型对提示词的忠诚度。默认 **7** 是多数模型的推荐起点。具体表现：

- **< 4**：模型自由发挥，与提示词相关性弱，可能产生意外创意，但容易偏离主题。
- **4–7**：常用范围。值越低，画面越有“艺术松弛感”；值越高，提示词中的每个词都被强化。
- **> 12**：过拟合，画面出现强白色光晕、颜色过饱和、物体边缘硬化，甚至产生诡异重复纹理。

调参时，先固定步数 20，采样器 DPM++ 2M Karras，从 CFG=5 开始，每步加 1 对比效果。**若提示词包含人物，CFG 7–9 能更好保持五官结构；风景类可用 5–7 让背景更柔和。** 注意：CFG 与步数共同影响结果，低步数（<15）搭配高 CFG（>10）容易产生噪点碎片。

掌握这三个参数后，你可以用同一组提示词快速压缩搜索空间——**先定采样器，再调步数，最后微调 CFG**。这是 **Stable Diffusion WebUI 入门**最有效的调试顺序。


---


## 图生图与局部重绘：修复与扩展图像的方法
文生图能凭空造画面，但很多实际需求是围绕已有图像修改——修复脸部崩坏、替换背景、把涂鸦变成成品。**Stable Diffusion WebUI 入门**的第二大标签页“img2img”就是干这个的。它用一张输入图 + 一段提示词，生成一张风格相似但细节不同的新图。

---

### 图生图：从一张图出发

切换到 **img2img** 标签，左侧多了一个图片上传区。拖拽一张图进去，下方参数基本和文生图一致，但多了一个关键值 **Denoising strength**（去噪强度）。这个值控制新图与原图的相似度：

- **0.3–0.4**：轻微修改，保持轮廓，适合修复小瑕疵或颜色微调。
- **0.5–0.7**：中等改动，构图保留，风格和细节可大幅变化。新手首选范围。
- **> 0.8**：接近全盘重画，原图只剩隐约构图。

> 每次修改用同样种子 + 同样 Denoising strength，可以复现风格偏移。调试时固定种子，用 0.4、0.6、0.8 各跑一次，快速找到合适强度。

**实际场景**：拍了一张照片想转成插画风。上传照片，提示词写 `digital painting, anime style, vibrant colors`，Denoising strength 设 0.6，采样器用 DPM++ 2M Karras，步数20。输出画面会保留人物姿势，但材质和光影完全改变。

注意：输入图尺寸最好与生成尺寸一致（通常 512×512），否则模型会先缩放再处理，导致脸部拉伸。

---

### 局部重绘：只改你需要的地方

局部重绘（Inpainting）是图生图的子功能，在 **img2img** 页面下方有一个“Inpaint”区域。上传图片后，用刷子工具在画面上涂抹——白色区域是要重绘的部分，黑色区域保留。**Stable Diffusion WebUI 入门**新手最容易忽略的一个设置：蒙版模式（Inpaint masked / Inpaint not masked），默认是只重绘白色区域。

**关键参数**：

- **Mask blur**：蒙版边缘羽化大小，默认 4。值越大，重绘区域与原图过渡越自然。修人脸时建议 8–12，避免拼接痕迹。
- **Inpaint area：Whole picture / Only masked**：选“Only masked”只重绘白色区域，速度更快，且原图其余部分完全不变。推荐新手一直选这项。
- **Denoising strength**：在局部重绘中同样有效，0.5–0.7 效果最好。太高会让蒙版内内容与原图风格割裂。

**实操举例**：你生成了一个 AI 美女，但手指多了两根。用刷子把多余手指涂白，提示词写 `hand, five fingers, normal anatomy`，负面词加 `deformed, extra fingers`，Denoising 设 0.6，点击生成。几秒后手指恢复正常。

> 如果重绘区域意外变黑或漏白，检查蒙版模式是否选了“Inpaint not masked”（反转）。默认是“Inpaint masked”，不要改。

**扩展画布（Outpaint）**：局部重绘的另一种用法——用“Resize and fill”配合较大尺寸（如 768×768），并在边缘涂白，模型会自动填充四周内容。但需要多次迭代才能获得连贯画面，入门阶段先掌握基础修复即可。

图生图与局部重绘是纠正 AI 随机性的最直接手段。一次生成不满意，不要重跑提示词，而是把当前图拖进 img2img，微调参数和蒙版，往往几轮就能出你想要的结果。


---


## 常见问题与故障排查：显存不足与模型加载失败
OOM（显存溢出）直接崩掉，模型加载后报“KeyError”或白屏——这两个故障占据了新手求助帖的八成。**Stable Diffusion WebUI 入门**的卡点往往不是操作,而是硬件限制或文件放错位置。

## 显存不足：最直接的物理瓶颈

当你点击 Generate 后终端弹出 `RuntimeError: CUDA out of memory. Tried to allocate XX MiB`，这就是显存用完了。解决顺序如下：

- **加启动参数**：编辑 `webui-user.bat`，在 `set COMMANDLINE_ARGS=` 后追加 `--medvram`。如果还报错，换成 `--lowvram`。`--medvram` 将 UNet 分块计算，显存占用从 6GB 降到 4GB 左右；`--lowvram` 更激进，会逐层卸载再加载，性能损失约 40%，但 2GB 显存也能勉强跑。
- **缩小生成尺寸**：从 512×512 降到 384×384 甚至 320×320。WebUI 允许自定义宽高，但低于 256 会让画面失去细节。
- **关闭多余进程**：浏览器标签页、Chrome 硬件加速、录屏软件都会吃显存。一个 Chrome 标签页可占用 200–500MB 显存。
- **降低 Batch count**：一次只生成一张图。Batch size 持续为 1，Batch count 再多也只是排队，不额外占显存。

> **关键检查点**：运行任务管理器（Ctrl+Shift+Esc），查看“GPU 内存”行。如果生成前就已占用 80% 以上，即使 `--medvram` 也可能失败。此时唯一解法是升级显卡或使用云端服务。

## 模型加载失败：路径与格式问题

WebUI 启动时报 `KeyError: 'model.diffusion_model.input_blocks.0.0.weight'` 或界面右侧模型下拉菜单为空，原因通常是模型文件放错位置或格式不对。

- **模型存放路径**：所有 checkpoint（.ckpt 或 .safetensors 文件）必须放在 `stable-diffusion-webui/models/Stable-diffusion/` 目录下，不能放子文件夹，也不能改名成中文或特殊字符。例如 `realisticVisionV51_v51VAE.safetensors` 正确，`写实模型.safetensors` 会导致 UI 识别不到。
- **文件完整性**：模型下载中断会产生空文件或不完整文件。命令行切换到模型目录，运行 `python -c "import torch; m=torch.load('你的模型.safetensors', map_location='cpu'); print('OK')"`。如果报错，重新下载。**Stable Diffusion WebUI 入门**用户最常踩的坑：用迅雷下载中途手动暂停再继续，文件已损坏，必须重新下载。
- **版本兼容性**：Stable Diffusion v1.x 与 v2.x 的模型不能混用。v2.x 模型加载到 v1.x WebUI 会报 `KeyError`。检查模型文件名是否包含 `v1-5` 或 `sd2` 字样。当前 WebUI 默认支持 v1.5。如需使用 SDXL 模型，必须切换到专用分支或使用 Forge 版本。

> 若模型下拉菜单为空，检查 `models/Stable-diffusion` 文件夹是否存在，且文件扩展名是否为 `.safetensors` 或 `.ckpt`。一个 2–7GB 的文件，若大小只有几百 KB，那就是来源出错，去 Hugging Face 重新下载。

**验证方法**：在模型下拉菜单切换模型后，看终端输出是否提示 `Loading weights from ...` 且无错误。如果有红色 `AssertionError`，说明模型文件损坏或版本不匹配。


---


## 进阶技巧：ControlNet与LoRA模型的使用
ControlNet 和 LoRA 是 WebUI 生态中最实用的两个扩展，能大幅控制画面构图和统一角色风格。**Stable Diffusion WebUI 入门**阶段掌握这两个，输出质量可以比只靠提示词高一个量级。

### 安装 ControlNet：骨架控制

ControlNet 是一个扩展，不是内置功能。安装步骤：

- 打开 WebUI，进入 **Extensions** → **Available** → 搜索 "ControlNet" → 找到 "sd-webui-controlnet" → 点击 **Install**。
- 重启 WebUI。顶部会多出 **ControlNet** 折叠面板。
- 下载 ControlNet 专用模型。主流是 `control_v11p_sd15_openpose.pth`（姿态骨架）和 `canny`（边缘检测）。去 Hugging Face 的 `lllyasviel/ControlNet-v1-1` 下载 .pth 文件，放进 `models/ControlNet/` 文件夹。

**实操场景**：你有一个角色的特定姿势想复现。上传一张带姿态的图到 ControlNet 面板，预处理器选 `openpose_full`，Control Weight 设 **0.7–1.0**。生成后角色姿势完全遵循源图，但服装、背景由你的提示词决定。

**关键参数**：
- **Preprocessor**：`canny` 生成线稿，`depth` 保留景深，`openpose` 捕捉人体骨骼。初学者先固定用 `canny`。
- **Control Weight**：0.0–2.0，1.0 为平衡点。值越大，模型越严格遵循 ControlNet 输出。构图不稳定时提到 1.2，想保留更多创造力降到 0.6。
- **Guidance Start / End**：控制 ControlNet 生效的时间段。推荐 Start=0.0, End=0.8，最后 20% 步数让模型自由微调细节，避免僵硬感。

> ControlNet 会额外消耗显存。`canny` + 512×512 约占用 0.5GB，`openpose` 约 1GB。如果显存小于 6GB，保持 ControlNet 面板折叠（不加载模型）直到使用时再展开。

### LoRA 模型：风格与角色指纹

LoRA 是轻量级微调权重文件（通常 30–200MB），注入 base model 来改变特定风格或角色。安装和使用更简单：

- 下载 .safetensors 文件（如 `maids_sd15.safetensors`），放到 `models/Lora/` 文件夹。
- 在文生图/图生图界面，点击提示词框右侧的 **Show Extra Networks** 按钮（或直接打开 **Extra** 面板），找到 LoRA 标签，点击即可插入 `<lora:maids_sd15:1>` 到提示词中。
- 后面的数字是权重，通常 **0.5–1.2**。风格偏弱增加权重，过拟合则降低到 0.6–0.8。

**常见搭配**：LoRA + 特定角色概念（如“某个动漫角色”、“写实皮肤纹理”）叠加多个 LoRA 也是允许的，但总权重之和不要超过 2.0，否则画面混乱。示例：

```
a portrait of character, <lora:chara_1:0.8>, <lora:realistic_skin:0.6>
```

LoRA 需要与 base model 版本匹配。SD 1.5 的 LoRA 不能用于 SDXL。下载时注意文件名是否标注 `sd1.5` 或 `sdxl`。

> 如果 LoRA 不生效或报错 `KeyError: 'lora_te'`，检查模型文件夹路径是否包含中文/空格，或尝试在设置中启用 `Ignore mismatched sizes` 选项。

ControlNet 和 LoRA 真正让 **Stable Diffusion WebUI 入门**用户突破“全靠提示词撞大运”的阶段。先装好 ControlNet 跑一次姿态控制，再找一个喜欢的 LoRA 测试权重，能立刻感受到画面可控性的提升。


---


## 总结
## 总结与建议

从安装环境到ControlNet，你已走完**Stable Diffusion WebUI入门**的核心路径。多数新手在完成第一张图后就停止探索，但实际上只需要调整两三个习惯，出图效率就能翻倍。

**优先训练提示词直觉**：别急着换模型。先用默认模型（`v1-5-pruned-emaonly`）配合一组固定参数（采样器Euler a，步数20，CFG 7，种子固定），反复修改提示词，观察每次变化。写100张图后，你自然会形成“哪些词对细节有效”的判断力。

**参数组合推荐**：我自己的常用基线是 **DPM++ 2M Karras + 步数25 + CFG 7**。遇到画面太僵硬时，CFG降到5.5；需要更多细节时，步数提到30并切换到`DPM++ SDE Karras`（速度稍慢但纹理更锐利）。**重要原则**：一次只改一个参数，其他锁定，才能知道哪个调整起了作用。

**资源管理**：
- 生成图片默认存在`outputs/txt2img-images`，每周清理一次，删除明显失败的批次，否则磁盘很快占满。
- 模型文件只会越来越大。只保留你实际使用的模型（通常2–3个），把不用的`.safetensors`移到备份目录，而非删除。
- 显存优化参数写成启动脚本：在`webui-user.bat`中固定`--medvram --xformers`，避免每次手动输入。

**保持WebUI更新**：AUTOMATIC1111每月都有小版本更新，修复bug和增加功能。在WebUI内`Extensions`->`Check for updates`一键更新。如果更新后出现错误，备份`stable-diffusion-webui`文件夹后重装最省事。

> **新手最常见误区**：遇到问题先重装。90%的故障通过调整启动参数或检查模型路径就能解决。重装是最后手段。

**社区资源推荐**：
- **Civitai**（civitai.com）：模型和LoRA的集中下载地，注意看模型说明里标注的base model版本（sd1.5 / sdxl）。
- **Hugging Face**：官方模型和ControlNet预处理器模型源。
- **Reddit r/StableDiffusion**：英文社区，搜“Common issues and fixes”帖子能解决大部分疑难。

**Stable Diffusion WebUI入门**最核心的认知是：这不是一个“点一下就能出大师级作品”的工具。它需要你理解参数间的相互作用（步数×CFG×采样器），需要你管理好自己的提示词库和模型库，更需要你在反复失败中积累经验。保持每次生成后至少问自己一句：“这个结果，是我哪个参数导致的变化？” 持续三个月，你就能用同样的界面输出和别人完全不同的质量。