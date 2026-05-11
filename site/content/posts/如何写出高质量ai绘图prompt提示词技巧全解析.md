+++
title = '如何写出高质量AI绘图prompt？提示词技巧全解析'
date = '2026-05-11'
draft = false
tags = ['create']
+++

> 你花半小时写了一段“详细描述”，结果AI绘图出来的不是三头六臂就是背景糊成鬼。问题不在AI，在你不会写prompt。**AI 绘图 prompt 提示词技巧**能让你的指令从“随便画个猫”变成“太平洋岛礁上戴着反光墨镜的写实猫，戏剧光，微距，2:3画幅”——5种结构技巧+反面排除法，读完后3分钟就能让出图质量翻倍。


## AI 绘图 prompt 的通用结构：从主体到细节的公式化写作
新手最容易犯的错误：写 prompt 靠玄学，想到哪写到哪。一张图生成三次，三次风格完全不像同一个东西。

**AI 绘图 prompt 提示词技巧**的第一步，就是掌握一个标准化的结构公式。这个公式不在乎你用 Midjourney v6.1 还是 Stable Diffusion XL 1.0，底层逻辑一致：**主体 + 媒介 + 环境 + 光照 + 角度**。

### 一个不够，五个来凑

以 [4] 中的经典案例为例，改造前后的对比非常明显：

- **无效 prompt**: `a cat`
- **有效 prompt**: `Pov Highly defined macrophotography of a realistic cat wearing reflective sunglasses relaxing at the tropical island, dramatic light --ar 2:3 --v 5`（来源 [4]）

差别在哪？前者只有一个“主体”。后者按公式拆解：
1.  **主体 (Subject)**: `a realistic cat wearing reflective sunglasses`
2.  **媒介 (Medium)**: `macrophotography`（指定了这是微距摄影，决定景深感）
3.  **环境 (Environment)**: `tropical island`（背景不再是空气）
4.  **光照 (Lighting)**: `dramatic light`（阴影和高光的具体品质，是生成电影感的关键）
5.  **角度 (Angle)**: `Pov`（第一人称视角，主动控制构图）

> **关键技巧**：把每个元素当作一个“参数”来写，用逗号隔开。AI 对逗号分隔的理解远好于复杂的主谓宾长句（来源 [1]）。

### 从抽象到具体的转换法则

很多人卡在“写细节”这一步。转换法则很简单：**把形容词换成具体名词或技术术语**。

- 抽象：`beautiful face` → 具体：`symmetrical face, high cheekbones, clear skin, photorealistic texture`
- 抽象：`good lighting` → 具体：`cinematic lighting, soft rim light, volumetric fog`
- 抽象：`nice background` → 具体：`cyberpunk cityscape, neon signs, rain-soaked asphalt`

参考 [2] 中提到的 AI Art Prompt Builder，其核心逻辑就是将用户的模糊输入转化为类似“`35mm film photography, f/1.8 aperture, shallow depth of field`”这样的结构化指令。

> **注意**：如果你一开始无法同时掌控五个元素，先固定“主体”和“媒介”两个最底层的参数。其他三个根据生成效果逐步微调。错误出在哪一步，就改对应位置的参数，不要全盘推翻重写。


---


## 反向提示词：用 Negative Prompt 排除不想要的元素
AI绘图默认会“平均”所有出现的特征。不加限制，它倾向于填充画面——增加多余四肢、模糊背景、扭曲人脸。**Negative Prompt（反向提示词）** 直接告诉AI不要画什么，比反复修改正向prompt更高效。

Midjourney与Stable Diffusion处理反向提示词的语法不同，但逻辑一致。

### Midjourney使用 `--no` 参数

在prompt末尾加上 `--no` 并列出排除对象。多个元素用逗号分隔。

- 生成写实人物，排除多余肢体和模糊细节：`photorealistic portrait of a man, dramatic lighting --ar 2:3 --no extra limbs, blurry face, duplicate head`
- 生成科幻城市夜景，排除现代元素：`cyberpunk city street at night, neon lights, rain --no cars, humans, billboards`

> 注意：`--no` 不适合否定抽象概念。否定“ugly”（丑陋）通常无效，因其本身就是主观修饰，AI难以量化。应排除具体物体：`--no deformed hands` 远比 `--no ugly` 有效。

### Stable Diffusion使用 `Negative prompt` 字段

SD系列（包括SDXL和SD 1.5）在txt2img界面的“Negative prompt”文本框中填写。常见排除项是一个组合词串，节省token，提高出图稳定性。

**推荐SD反向提示词组合（来源 [1]）：**

`worst quality, low quality, ugly, deformed, blurry, low resolution, bad anatomy, bad hands, extra fingers, missing fingers, fused fingers, cropped, jpeg artifacts, text, watermark, signature`

此组合排除三类问题：
1. **画质缺陷**：`worst quality, low quality, blurry, low resolution, jpeg artifacts`
2. **解剖错误**：`bad anatomy, bad hands, extra fingers, missing fingers, fused fingers`
3. **干扰元素**：`text, watermark, signature, cropped`

### 权重微调：针对顽固错误

当AI反复画出同一个错误（如第6根手指），可单独加重排除权重。SD中语法为：`(extra fingers:1.4)`。括号外系数越大，排除力度越强。系数1.4-1.6效果明显，1.8以上可能影响其他正常区域。

**真实场景对比**：生成人像时，正向prompt `cinematic portrait of a woman` 有30%几率出现六指。加上 `(extra fingers:1.5)` 后，20张图零出错。这正是AI绘图prompt提示词技巧中，用最小改动解决最大问题的典型方法。

反向提示词不是“写一次就完”。每次新风格或新模型，建议生成2-3张图，观察共性错误，将重复出现的元素加入Negative Prompt。随模型社区更新（如SDXL 1.0的解剖结构比1.5更稳定），反向提示词也需要精简。


---


## 关键参数与风格控制：比例、版本、Stylize 值如何影响画面
主体描述写得再细，如果参数没调对，AI依然会给出意料外的画面。**AI 绘图 prompt 提示词技巧**除了正向和反向指令，还包括末尾的几个关键数值参数。它们独立于文本描述，直接控制画面比例、模型版本和风格化强度，优先级高于任何形容词。

### 画面比例（`--ar`）：先定构图骨架

`--ar` 后跟两个冒号分隔的数字，例如 `--ar 16:9`。比例影响景别和画面重心，不指定则默认 1:1（方形）。

- **1:1**：对称构图、头像、产品展示。AI 倾向于填充中心区域，背景细节较少。
- **3:2**：传统摄影比例，适合风景、环境人物。
- **16:9**：宽屏电影感，水平空间被拉伸，AI 会在左右两侧添加更多环境元素（如天空、建筑物）。
- **2:3**：竖版肖像、社交媒体封面，紧贴主体，背景压缩。

> **注意**：不同版本对 `--ar` 的响应略有差异。Midjourney v6.1 严格遵循比例裁剪，SDXL 则可能自动扩展画布并补全背景。建议每改一次比例就重新生成 2-3 张确认裁切效果。

### 模型版本（`--v`）：引擎决定基础能力

`--v` 指定 Midjourney 的模型版本。当前主流是 `--v 6.1`（2024年9月更新）。版本差异直接影响写实度、解剖准确性和风格多样性。

- **`--v 5`**：高写实，但手部、复杂肢体偶尔出错。适合风景、静物。
- **`--v 5.2`**：改进了光影，支持更高一致性，但风格化倾向变低。
- **`--v 6` / `--v 6.1`**：解剖错误大幅减少，理解长 prompt 能力更强，支持 `--style raw` 去除内置美感滤镜。

如果你发现生成的人物手指断裂、面部扭曲，优先检查 `--v` 是否太低。用 `--v 6.1` 配合 `--no extra limbs` 通常能解决 80% 的结构问题。

### 风格化值（`--s` / `--stylize`）：审美干预强度

`--s` 后接 0–1000 的整数（默认 100）。它控制 AI 在构图、色彩、纹理上的“创意偏移”程度。

- **`--s 0` – `--s 100`**：低风格化。AI 严格遵循描述，画面写实、保守，细节较少。
- **`--s 250` – `--s 500`**：中等风格化。色彩更饱和，光影更戏剧，背景元素丰富。适合人物肖像、科幻场景。
- **`--s 750` – `--s 1000`**：强风格化。AI 主动添加纹理、光晕、夸张构图，甚至改变主体形状。适合概念艺术、梦幻风格。

实际效果参考：一个 prompt `a realistic cat` 在 `--s 100` 下是普通猫照；在 `--s 750` 下猫眼会反射斑驳光线，毛发光泽增强，背景可能出现抽象条纹。**过度使用 `--s` 会让写实画面失真**，所以先固定 `--v` 和 `--ar`，再逐步微调 `--s`。

这三个参数可组合写在prompt末尾，顺序不限：`... --ar 16:9 --v 6.1 --s 250`。调整它们比重写描述更省时间，是排查“画面为什么不好看”的第一站。


---


## 光线、构图与视角：用专业摄影语言提升 AI 绘图 prompt 细节
把“光线”改成“在下午4点的金色时刻，背光，45度侧逆光”。这个转换看起来简单，效果却差一个量级。AI 绘图 prompt 提示词技巧的进阶玩法，是用专业摄影术语替换日常词汇，让模型切换回“摄影师模式”。

### 光线描述：从“亮”到“具体的光质”

AI 理解的“亮”只是亮度值，而 `dramatic lighting`、`volumetric lighting`、`rim light` 这类词直接调用了模型训练集中的百万级打光参数。以 [4] 中的 `dramatic light` 为例，它把单光源场景变成了高反差+明暗交界线的电影效果。

常用的光线类型及代码效果：
- **`golden hour`**：暖色调、长阴影、低角度光源。适合风景、人像。
- **`cinematic lighting`**：主光+补光+轮廓光三布光，人物面部立体感强。
- **`hard light` / `soft light`**：硬光产生锐利阴影（适合硬汉肖像），柔光模糊阴影（适合女性、产品）。
- **`volumetric fog`**：空气中的光柱或雾状效果，提升纵深感和氛围。

> 注意：在Midjourney v6.1中，光线词必须放在prompt前1/3段才有效，位置越靠后权重越低。SDXL则对光线词的位置不敏感，但建议加在“环境”部分之后。

### 构图描述：用镜头语言控制景别

AI默认生成“看到全部”的画面。你想突出局部，就必须主动说明。核心构图参数包括：
- **景别**：`close-up`（特写）、`macro shot`（微距）、`wide angle`（广角）、`extreme wide shot`（超广角）。微距会把主体放大到占据画面80%以上，广角则拉出巨大背景。
- **景深**：`shallow depth of field`（前景清晰背景模糊）、`deep depth of field`（全清晰）。SDXL对景深的理解比Midjourney好，但 `--s 500` 以上时会主动破坏浅景深。
- **镜头规格**：`35mm`（人文视角）、`85mm`（人像黄金焦段）、`fish-eye lens`（变形效果）。**这些术语等同于给AI一个“镜头配置文件”，比写“相机从上往下拍”更精确。**

### 视角描述：决定画面代入感

视角改变观众与主体的心理距离，摄影行业的标准视角词同样适用于prompt：
- **`Pov` (第一人称)**：镜头当作眼睛，主体在画面中看镜头。配合 `close-up` 会有极强的代入感。
- **`low angle` (低角度)**：物体显得高大、有压迫感，适合建筑、英雄姿态。
- **`top-down` (俯视)**：适合产品展示、桌面场景，减少背景干扰。
- **`side view` (侧视)**：适合人物剪影、轮廓展示。

以 [4] 中那只猫为例，如果你改为 `top-down macro shot of a realistic cat, soft daylight`，图像会立即变成一张俯拍的产品级猫零食封面——视角变了，用途跟着变。上述技巧与结构公式、反向提示词结合，能最大限度降低生成结果的不确定性。


---


## 针对不同 AI 绘图工具的 prompt 适配技巧：Midjourney vs Gemini vs SD
Midjourney vs Gemini vs Stable Diffusion 的语法差异比很多人想象的更大。同一个 prompt 在不同工具里输出可能完全两样。**AI 绘图 prompt 提示词技巧**必须针对具体工具做适配，不能“一套模板通杀”。

### Midjourney：参数驱动，位置敏感

Midjourney v6.1 的核心规则：**文本描述 + 末尾参数**。光线词必须放在 prompt 前 1/3 段，越靠后权重越低。

对比写法（同样描述“写实猫”）：
- **Midjourney**
  `macro photography of a realistic cat, dramatic light --ar 2:3 --v 6.1 --s 250`
- **Stable Diffusion XL**
  正向框：`macro photography of a realistic cat, dramatic light`
  负向框：`worst quality, blurry, bad anatomy, extra fingers`
- **Gemini 2.5 Flash**
  `一张微距摄影写实猫，戏剧光，画面比例2:3`

差异在哪？
- MJ：参数用 `--` 前缀，**位置顺序影响权重**。
- SD：**Positive + Negative 双框结构**，支持权重语法 `(bad hands:1.4)`。
- Gemini：**无参数系统**，比例必须融入自然语言描述。

### SD：权重语法与组合排除

SD 独有的权重微调是其他工具没有的。示例：`(extra fingers:1.5), (deformed hands:1.4), worst quality`

这套语法在 MJ 中完全无效。MJ 的 `--no extra limbs` 只能排除物体，不能加重惩罚。

### Gemini：长文本与中文优势

根据官方文档，Gemini 2.5 Flash 的 token 限制是 **32,768**（来源[3]），远超 MJ 和 SD。这意味着：

- 可以写 5-8 行的详细描述，AI 不会丢失信息
- 直接写中文比例描述：`16:9宽幅画面`
- 适合复杂场景：`一个戴反光墨镜的写实猫，在太平洋岛礁上，午后的金色光线，微距`

> **实用忠告**：不要在同一工具中混用另一工具的语法。MJ 参数在 SD 中会被忽略，SD 权重写法在 MJ 中产生乱码。每次切换工具前，先确认对方支持的指令集。


---


## 迭代优化法：如何通过重写与测试逐步逼近理想输出
理想输出很少一次生成。第一版总有些问题：构图不对、光线太平、主体位置偏离预期。**AI 绘图 prompt 提示词技巧**的核心不是“一次性写好”，而是“快速迭代”——通过小步重写加对比测试，在3-5轮内逼近目标。

### 对比测试：用“三张定基调”

不要只生成一张图就判断好坏。一次至少出 **3张**，对比找出共性缺陷：

- **构图偏移**：如果3张主体都偏右，调整角度词 `from left` 或 `centered composition`
- **光线偏差**：如果3张都太暗，加 `bright` 或提高 `\--s` 值50点
- **风格不一致**：如果一张写实、一张卡通，检查 `\--v` 版本是否稳定，或加 `photorealistic, 8k` 强化写实标记

对比完成后，只改一个变量。这是**单变量原则**——改错时能立刻定位到是哪个参数引起的偏差。

### 精准修改：改词而不是改描述

发现“颜色偏离”后，不要整句推倒重写。定位到是“环境”部分的颜色词不准，只替换那一个词：
- 原：`tropical island, green foliage`
- 改：`tropical island, turquoise water, white sand`
- 试：看结果是否变得更贴近预期

> **关键**：Midjourney v6.1 对词序敏感，修改范围越小，AI 的响应越可预测。

如果修改后新问题出现（如背景变模糊），检查是否是新词带来的副作用。这时可以加 `\--no blurry background` 排除，而不是再换一组描述。

### 版本控制：记住每一步的prompt

每次修改后，保存prompt并记录版本号和生成时间。一个可复用的格式：
```
v1: prompt + \--ar 16:9 \--v 6.1 \--s 250 (2025-02-15)
v2: v1基础上 cat改为 golden retriever
v3: v2基础上 s改为 500
```

这样做的好处是：当某个版本效果特别好，你能直接复现。当某个修改失败，也能快速回退，不必从头写。

**迭代的核心是“小步快跑”**：一次改一个词或一个参数，生成3张，对比，再改下一个。三轮迭代后，你的prompt就从“能用”变成“稳定出高质量图”。


---


## 三大常见错误：冗长、冲突、缺乏场景——以及如何避免
写 prompt 最常见的坑有三个：形容词堆砌、抽象意图描述、缺乏背景约束。避开它们，输出质量会立刻提升。

### 冗余的形容词堆砌

```beautiful majestic gorgeous stunning breathtaking amazing``` —— 五六个形容词夸同一件物体。AI 不会平等关注每个词，而是随机组合两个，导致每张图风格不一样。

**解决办法**：只保留 1-2 个精准形容词，其他交给主词和参数控制。

- 原：`a beautiful majestic stunning cat`
- 改：`a elegant cat, macro photography`
- 省下的 token 留给场景描述。

> 关键原则：**形容词描述状态，名词和参数控制风格**。去掉 `beautiful`，结果通常更好。

### 抽象的意图描述

`a sad photo` — 模型不理解“悲伤”。它只能回应物理特征：五官、光线、构图。

不要写情感，写物理特征：
- × `a romantic atmosphere`
- √ `soft warm light, shallow depth of field, rose petals in foreground`

`a futuristic feel` → `sleek metal surfaces, neon blue lighting, floating holograms`

**AI 绘图 prompt 提示词技巧**：所有抽象词都是干扰。改成可测量的视觉元素：颜色、纹理、形状、光照角度。

### 缺乏场景与背景约束

只写 `a cat`，模型会默认填充背景——可能是白色 studio、草地、太空站、水墨画。这是**风格冲突**的源头。

明确背景，即使只是简单一句：
- × `a cat`
- √ `a cat on a weathered wooden fence, morning mist`

背景描述的优先级：**单元素优于多元素**。如果写 `a cat, a tree, a house`，模型可能平均分配注意力导致主体不突出。要么写 `a cat on a porch`，要么用 Negative prompt 强制排除其他物体。

> 注意：背景越具体，主体越稳定。空背景默认是模型平均值——往往是最无聊、最混乱的输出。

如果不填背景，可以用 `--no background` 或 `--no scenery` 强迫模型聚焦主体。但这只适用于 Midjourney v6.1+ 和 SD XL，Gemini 不支持 Negative prompt，必须用自然语言明确。


---


## 总结
写好 prompt 只是第一步。真正让输出质量稳定的，是**可复用的工作流**。**AI 绘图 prompt 提示词技巧**的最终阶段不是记忆所有语法，而是建立一套自己的检查流程。

### 写 prompt 的标准流程

每次生成前，按三个步骤过一遍：
1.  **套结构公式**：**主体 + 媒介 + 环境 + 光照 + 角度**，缺哪个补哪个。这是兜底模板。
2.  **追加参数**：先设 `--ar` 确定构图骨架，再调 `--v` 确定模型版本，最后用 `--s` 微调风格强度。
3.  **填反向池**：根据图生图结果，把重复出现的错误加入 Negative Prompt。手部问题用 `(extra fingers:1.5)`，画质问题用 `worst quality, blurry`。

> 这个流程约30秒。跳过它直接写描述，出图后修图的时间是它的10倍。

### 一份可打印的检查清单

把下面内容记在备忘录里。每次卡壳时逐一比对：

- [ ] 主体是否只有一个？（多主体请分别描述，用“and”连接）
- [ ] 光线是否用专业术语而非日常词？
- [ ] 是否设置了画面比例？（默认1:1不是你想要的）
- [ ] Negative prompt 是否包含至少3个常见排除项？
- [ ] 是否开启了迭代流程？（生成3张，改1个参数，再生成3张）

### 常见问题快速对应表

| 问题 | 调整方向 | 示例 |
|------|----------|------|
| 主体位置偏移 | 改角度词 | 加 `centered composition` 或 `from left` |
| 手指/解剖错误 | 加强反向提示 | `(extra fingers:1.5)`，或检查 `--v` 版本 |
| 风格不一致 | 调整 `--s` 值 | 写实图 `--s 100`，概念图 `--s 500` |
| 背景太复杂 | 加 `--no background` | 或改环境描述为单元素 |
| 画面太暗 | 改光线词 | 把 `dramatic light` 换成 `soft daylight` |

### 最后一句执行力建议

**别囤积技巧文档。** 打开你的 AI 绘图工具，选一个之前生成失败的 prompt，按本文的流程重写一次。**一次实践胜过十页理论。** 你会发现，高质量图片的生成规律并不神秘——它只是一组可重复、可调试的输入指令。