---
title: "DeepSeek V4 接入 Claude Code 教程：详细步骤"
slug: "deepseek-v4-接入-claude-code-教程详细步骤"
keyword: "DeepSeek V4 接入 Claude Code 教程"
category: "手动测试"
date: "2026-05-11"
search_volume: N/A
difficulty: "N/A"
word_count: 9748
generated_by: "deepseek-v4-flash"
---

> 你正在使用 Claude Code 写代码，突然收到“API 配额用尽”或“用量已达上限”的提示。进度被打断，开销还在涨——这是不少开发者开始寻找替代方案的真实起点。如果你也有类似经历，这篇 DeepSeek V4 接入 Claude Code 教程 能直接帮你换个模型、保留工作流程。
> 
> 本教程的目标是把 Claude Code 的驱动模型从 Anthropic 官方 API 切换到 DeepSeek V4-Pro。完成后，你可以在相同终端界面里继续使用 Claude Code 的全部工具链（文件编辑、命令行、代码搜索），而流水按 DeepSeek 的定价走——成本仅为原生 API 的零头，配置过程大约三分钟。
> 
> 我会拆解具体的环境变量设置、模型标识符确认步骤，以及一个可选的动态切换方案（通过claude-code-router实现），让你在多个模型之间灵活切换。配置中有几处容易踩坑，我会用实际错误日志说明如何排查。
> 
> 下面直接进入第一步。


## DeepSeek V4 接入前的准备工作：API Key 和环境要求
你需要准备三样东西：一个 **DeepSeek 账户**、一个**有效的 API Key**，以及**正确的环境变量配置方式**。本教程中使用的模型标识符为 **DeepSeek V4-Pro**，这一点务必确认，因为后续所有流量都指向这个端点。

### Step 1：注册并创建 API Key

前往 [platform.deepseek.com](https://platform.deepseek.com) 注册账户。登录后进入 **API Keys** 页面，点击创建新 Key。创建完成后立即**复制并保存到本地**——页面刷新后 Key 值不再可见。

> 注意：DeepSeek 为新用户提供 **500 万 token 免费额度**（截止文档发布时有效）。你无需预充值即可完成本教程的全部测试步骤。

### Step 2：确认 API 端点与模型名称

DeepSeek V4 的官方 API 基地址为：

```
https://api.deepseek.com/v1
```

使用的模型名称是 **deepseek-v4-pro**（注意大小写）。如果你使用第三方代理（如阿里云百炼），端点地址会不同——后续章节会单独说明。

### Step 3：配置环境变量（macOS / Linux）

将 API Key 写入 shell 配置文件（`~/.zshrc` 或 `~/.bashrc`）：

```bash
export DEEPSEEK_API_KEY="sk-你的Key"
export DEEPSEEK_BASE_URL="https://api.deepseek.com/v1"
export CLAUDE_CODE_MODEL="deepseek-v4-pro"
```

执行 `source ~/.zshrc` 使配置生效。**验证方法**：终端运行 `echo $DEEPSEEK_API_KEY`，如果输出完整 Key 字符串则配置成功。

> **常见陷阱**：如果 Key 中包含特殊字符（`$`, `!`, `\`），必须用**单引号**包裹，否则 shell 会解析出错，导致接入后请求返回 401 认证失败。

完成上述步骤后，你的终端环境已经具备发起 DeepSeek V4 API 请求的能力。接下来需要将这些变量传递给 Claude Code 的启动过程。


---


## 配置 Claude Code 连接 DeepSeek V4-Pro 的详细步骤
这一节是 **DeepSeek V4 接入 Claude Code 教程**的核心操作步骤。前面的准备工作只配好了环境变量，但 Claude Code 默认仍会请求 Anthropic 的 API。你需要告诉它把流量转给 DeepSeek。

### 启动 Claude Code 并指定端点

在终端中运行以下命令，Claude Code 会自动读取已配置的 `DEEPSEEK_API_KEY` 和 `DEEPSEEK_BASE_URL`：

```bash
claude
# 或指定模型名称，覆盖默认模型选择逻辑：
claude --model deepseek-v4-pro
```

Claude Code 启动时会在标准输出打印一行日志，类似 `Provider: deepseek` 或 `Model: deepseek-v4-pro`。如果看到的是 `anthropic` 或 `claude-sonnet-4`，说明环境变量没有被读取——请重新检查 `~/.zshrc` 中的变量名拼写和引号。

> **关键验证**：在 Claude Code 界面中输入 `/status`。输出中 `model` 字段应为 `DeepSeek-V4-Pro`，同时 `API Base URL` 应显示为 `https://api.deepseek.com/v1`。任何一个字段不对，后续对话都会失败。

如果想临时换回官方 API，无需修改配置文件，只需在启动时附加原生 Key 即可：

```bash
CLAUDE_MODEL="claude-sonnet-4-20250514" claude
```

### 确认流量走 DeepSeek 端点

一个可靠的方法是让 Claude Code 执行一条简单查询，然后对照 DeepSeek 官方 API 控制台的用量统计页面检查。例如，发送一条“请输出数字 42”的指令。如果 `DeepSeek-V4-Pro` 模型返回的正是 `42`，且几分钟后控制台中出现该请求的记录，则连接无误。

常见问题：
- **401 Unauthorized**：Key 中有特殊字符且未用单引号包裹。
- **模型不存在**：`--model` 传入的名称拼写错误——正确值为 `deepseek-v4-pro`，注意连字符和下划线不能混用。
- **超时**：`DEEPSEEK_BASE_URL` 漏了 `/v1` 路径。

如果上述步骤全部通过，你的 Claude Code 已经使用 DeepSeek V4-Pro 驱动。此时，[claude-code-router](https://github.com/musistudio/claude-code-router) 可以让你在 `/model` 命令中动态切换模型——无需重启终端，这属于高级用法，适用后文的多模型场景。


---


## 验证接入是否成功：/status 命令与模型确认
输入 `/status` 后，第一眼就看 **model 字段**。如果显示 `DeepSeek-V4-Pro`，且 `API Base URL` 是 `https://api.deepseek.com/v1`，说明 **DeepSeek V4 接入 Claude Code 教程**的核心配置已经生效。

### 两种确认方式

- **直接在 Claude Code 界面输入** `/status`。输出中 `model` 值若不是 `DeepSeek-V4-Pro`，立刻检查环境变量 `CLAUDE_CODE_MODEL` 的拼写——常见错误是用下划线代替连字符。
- **发送一次测试请求**。让 Claude Code 执行 `echo "42"`，返回结果后去 DeepSeek 官方控制台的用量统计页面核对。如果几分钟内出现该请求记录，流量走通。

> 注意：如果跳过此步骤，后续的代理配置将无法生效。每次切换模型或端点后，都应重新执行一次 `/status` 确认。

### 常见失败场景

- **`model` 显示 `claude-sonnet-4-20250514`**：`DEEPSEEK_BASE_URL` 或 `DEEPSEEK_API_KEY` 未被读取。检查 shell 配置文件中是否漏了 `export`，或变量名拼写错误。
- **/status 命令无返回**：模型名称拼错导致连接中断。正确值必须为 `deepseek-v4-pro`，注意大小写和连字符。
- **401 Unauthorized**：API Key 中若包含 `$`、`!`、`\` 等特殊字符，用单引号包裹 `'sk-...'` 即可解决。

你也可以在启动时使用 `claude --model deepseek-v4-pro --verbose` 观察更详细的日志输出，`Provider` 行若显示 `deepseek` 而非 `anthropic`，说明连接正常。

如果以上任一方法通过，你的终端已经跑在 DeepSeek V4-Pro 上。后续若需动态切换模型，`claude-code-router` 的 `/model` 命令可以让你不用重启终端就换回 Claude 或其他模型。


---


## 多模型切换：使用 Claude Code Router 实现动态路由
### 安装 claude-code-router

单模型连接跑通后，你会发现一个实际问题：想对比 DeepSeek V4-Pro 和 Claude Sonnet 的代码输出，或者遇到 DeepSeek 临时限流时换回官方模型，都需要退出终端、修改环境变量再重启。`claude-code-router` 解决了这个痛点——它在 Claude Code 内部注册了一个 `/model` 命令，让你在 **不关闭会话** 的情况下动态切换驱动模型。

安装方式有两种，选一个就行：

- **全局安装**（推荐）：`npm install -g claude-code-router`，安装后终端直接可用 `ccr` 命令。
- **免安装直接运行**：`npx claude-code-router`，但每次启动都会重新下载，建议用于快速测试。

### 配置多 Provider

安装后，运行 `ccr init` 会在 `~/.claude-code-router/config.json` 生成配置文件。你需要为每个想切换的 provider 填入 **API Key 和 Base URL**。示例如下：

```json
{
  "providers": {
    "anthropic": {
      "apiKey": "sk-ant-...",
      "baseUrl": "https://api.anthropic.com/v1"
    },
    "deepseek": {
      "apiKey": "sk-你的Key",
      "baseUrl": "https://api.deepseek.com/v1"
    }
  },
  "modelAliases": {
    "claude": "anthropic:claude-sonnet-4-20250514",
    "ds-v4": "deepseek:deepseek-v4-pro"
  }
}
```

> **注意**：每个 provider 的 `apiKey` 都需要独立设置，不能简单继承 shell 环境变量。你可以在配置文件中使用 `${DEEPSEEK_API_KEY}` 引用环境变量，避免明文硬编码。

`modelAliases` 为常用模型起短名，方便 `/model` 切换时输入。

### 在 Claude Code 中切换模型

启动 Claude Code 前，先执行 `ccr start`，它会在后台注入路由。之后在 Claude Code 会话中输入：

```
/model ds-v4
```

几秒后输出会显示 `Switched to model: deepseek:deepseek-v4-pro`。你也可以直接输入模型全名：

```
/model deepseek:deepseek-v4-pro
```

输入 `/model` 不加参数可查看当前所有已注册的 provider 和可用模型列表。**这个列表只包含你在 `modelAliases` 中定义的条目**，未别名的模型不会显示。

完成 **DeepSeek V4 接入 Claude Code 教程** 的前三步后，建议立即安装 `claude-code-router`，因为后续调试代理或临时换模型时，不用反复重启进程。对于需要部署到特定区域或使用更低价格的第三方代理，你只需在 `providers` 的 `deepseek` 项中修改 `baseUrl` 即可，下一节会说明具体配置。


---


## 常见错误排查：API 密钥错误、模型不可用、超时处理
从 `/status` 确认模型正确，到实际对话中遇到问题，中间有几个常见的坑。下面直接列出我在配置反馈中最常遇到的三个错误。

### API 密钥错误：401 Unauthorized

这是最常见的错误，错误日志会直接显示 `401`。**原因几乎都是 shell 环境变量中的特殊字符问题。**

如果你在 `~/.zshrc` 中这样写：
```bash
export DEEPSEEK_API_KEY=sk-abc$def!ghi
```
那么 `$def` 和 `!ghi` 会被 shell 解释为变量。**正确的做法是使用单引号包裹：**
```bash
export DEEPSEEK_API_KEY='sk-abc$def!ghi'
```
单引号阻止了变量展开。完成后重新 `source ~/.zshrc`，并用 `echo $DEEPSEEK_API_KEY` 确认输出是否和 Key 一致。

另一个容易忽略的点是 Key 尾部的换行符。如果你从网页直接复制，有时会带上不可见字符。**建议用 `echo -n $DEEPSEEK_API_KEY | wc -c` 检查长度**，预期为 32 或 48 字符（根据官方 Key 格式）。

### 模型不可用：Model Not Found

错误日志显示 `Model 'deepseek-v4-pro' is not found`。你在 **DeepSeek V4 接入 Claude Code 教程** 中指定的模型标识符有拼写问题。

- 错误写法：`deepseek_v4_pro`（下划线）、`DeepSeek-V4-Pro`（大小写混用）
- **正确值必须全部小写，且用连字符连接：`deepseek-v4-pro`**

> 如果你使用的是第三方代理（如阿里云百炼），模型名称可能是 `deepseek-v4-pro-240526` 或类似带日期的版本。**必须从代理平台的文档中确认完整名称**，不能照抄官方示例。

### 超时处理：请求一直卡住

如果对话发送后几分钟才响应，或直接超时，首先检查 `DEEPSEEK_BASE_URL` 是否缺少 `/v1` 路径。常见错误是配置成 `https://api.deepseek.com`（漏了 `/v1`），导致请求路由错误。

可以用 `curl` 单独测试端点是否可达：
```bash
curl -I https://api.deepseek.com/v1
```
如果返回 `HTTP/2 200` 说明网络正常。如果超时，可能是代理或 VPN 干扰。对于中国大陆开发者，**推荐使用阿里云百炼作为代理**，配置方式只需修改 Base URL 为阿里云提供的地址，其余步骤不变。

完成 DeepSeek V4 接入 Claude Code 教程的配置后，这些错误排查方法会直接节省你反复查看文档的时间。


---


## 成本优化配置：为 DeepSeek V4 设置 API 调用限制与账单提醒
启动 Claude Code 后直接对话，成本是实时发生的。如果你没有设置任何限制，一次复杂代码生成的消耗可能远超预期而毫无预警。**在 DeepSeek V4 接入 Claude Code 教程**中，这一步容易被忽略，却直接影响预算控制。

### 在 DeepSeek 控制台设置调用限制

登录 [platform.deepseek.com](https://platform.deepseek.com)，进入 **Usage & Billing** 页面。你可以设置以下两种限制：

- **月度预算上限**：设置每月最大消耗金额，例如 **$20**。超过后 API 请求会被自动拒绝，不会产生超额费用。
- **单次请求上限**：限制单次对话的最大 token 消耗。DeepSeek V4-Pro 的上下文窗口为 **128K**，建议将 max_tokens 设置为 **4096** 或 **8192**，避免模型无限制生成。

> **注意**：月度预算的生效有轻微延迟，大约在超过限制后的 **1-2 分钟内**触发。建议设置一个低于月预算 80% 的“告警阈值”，提前收到通知。

### 配置账单提醒

DeepSeek 控制台提供三种通知渠道：

- **邮件提醒**：添加验证后的邮箱地址，选择告警触发比例（50%、80%、90%），系统会在接近阈值时发送邮件。
- **Webhook 推送**：输入你的 Webhook URL（如 Slack、Discord、飞书），每次用量变化时推送实时数据。
- **控制台内置面板**：在 Dashboard 首页查看当日、当周、当月用量曲线。**建议每次完成代码任务后扫一眼**，养成习惯。

### 通过环境变量控制消耗

在 `~/.zshrc` 中添加以下限制：

```bash
export DEEPSEEK_MAX_TOKENS=4096
export DEEPSEEK_TEMPERATURE=0.1
```

`DEEPSEEK_TEMPERATURE=0.1` 降低生成随机性，减少不必要的重复输出，间接节省 token。如果你使用 `claude-code-router`，可以在配置文件中单独为 `deepseek` provider 设置 `maxTokens: 4096`，覆盖全局默认值。

如果你部署了阿里云百炼代理，代理平台一般也提供自己的用量面板。**建议同时在 DeepSeek 官方和代理平台各设一道限制**，形成双重保护，避免因为代理统计延迟导致超额。


---


## 高级技巧：在 Claude Code 中自定义 DeepSeek V4 的上下文窗口
### 高级技巧：在 Claude Code 中自定义 DeepSeek V4 的上下文窗口

DeepSeek V4-Pro 的上下文窗口官方标称为 **128K tokens**，但 Claude Code 默认会保留整个对话历史。一次对话积累几十轮后，即使你只问一个小问题，API 也会把全部上下文发送出去——既不必要，也浪费 token。本 **DeepSeek V4 接入 Claude Code 教程** 的高级技巧教你如何精细控制上下文窗口的长度。

#### 通过环境变量限制 max_tokens

Claude Code 启动时会读取 `DEEPSEEK_MAX_TOKENS` 环境变量，并在每次请求中附带该值。在 `~/.zshrc` 中添加：

```bash
export DEEPSEEK_MAX_TOKENS=4096
export DEEPSEEK_CONTEXT_LIMIT=32768   # 可选，限制历史总长度
```

设置后，每轮回复不超过 4096 tokens。**长代码生成任务建议设为 8192**，避免中间截断。如果你使用 `claude-code-router`，可以在 `~/.claude-code-router/config.json` 的 `deepseek` provider 中覆盖：

```json
"deepseek": {
  "apiKey": "${DEEPSEEK_API_KEY}",
  "baseUrl": "https://api.deepseek.com/v1",
  "maxTokens": 4096,
  "maxContext": 65536
}
```

`maxContext` 控制历史窗口的 token 上限（包含输入和输出），超出部分会被截断。**注意**：`maxContext` 必须小于模型支持的 128K，建议设为 64K 作为平衡。

#### 在单条指令中临时调整

Claude Code 本身不提供 `/max-tokens` 命令，但你可以通过 `claude-code-router` 的 `/model` 切换别名时附带参数。在 `modelAliases` 中定义带参别名：

```json
"modelAliases": {
  "ds-short": "deepseek:deepseek-v4-pro?max_tokens=2048&temperature=0.1",
  "ds-long": "deepseek:deepseek-v4-pro?max_tokens=16384&temperature=0.5"
}
```

输入 `/model ds-short` 即切换到 2K 短回复模式，适合快速问答；`/model ds-long` 则用于完整代码生成。这种方法**无需重启终端**，也无需修改配置文件。

#### 验证生效

发送一条长测试指令，例如“写一个 500 行 Python 程序并逐行注释”。观察回复是否在第 4096 token 附近截断。也可以查看 DeepSeek 控制台的“Usage Log”，看 `max_tokens` 字段是否为设定值。若不符，检查环境变量名拼写——**务必使用大写和下划线**（如 `DEEPSEEK_MAX_TOKENS`），Claude Code 只识别这种格式。

> **注意**：DeepSeek V4 的 128K 上下文只在该模型最新版本中完整支持。如果你通过第三方代理（如阿里云百炼）使用 `deepseek-v4-pro-240526`，其上下文可能被限制为 32K。务必在代理文档中确认 `context_length` 参数，并相应调低 `maxContext` 值，否则会触发 `400 Bad Request` 错误。


---


## 总结
## 总结与建议

完成本 **DeepSeek V4 接入 Claude Code 教程** 的全部步骤后，你的开发环境已经具备用 DeepSeek V4-Pro 驱动 Claude Code 的能力。但配置只是起点，长期稳定使用需要遵循几条原则。

### 日常操作 checklist

每次启动 Claude Code 前，养成两个习惯：

- **运行 `/status` 验证模型**：检查 `model` 字段是否为 `DeepSeek-V4-Pro`，`API Base URL` 是否匹配你的端点。尤其是切换网络环境或重启终端后，这一步能提前拦截配置漂移。
- **查看 DeepSeek 控制台的用量面板**：确认当日消耗未超出预算。**月度限制建议设为 $20**，单次请求 max_tokens 控制在 **4096** 以内，避免意外超支。

### 场景化配置建议

不同使用场景的最佳配置不同，下面给出三组可直接套用的模板：

| 场景 | 推荐模型别名 | `maxTokens` | `maxContext` | 备注 |
|------|-------------|-------------|--------------|------|
| 快速问答 / 调试 | `ds-short` | 2048 | 16384 | 降低随机性，`temperature=0.1` |
| 代码生成 / 重构 | `ds-long` | 8192 | 65536 | 允许完整输出，`temperature=0.5` |
| 批量任务 / 自动化 | `ds-batch` | 4096 | 32768 | 开启 `stream: true`（需 router 支持） |

通过 `claude-code-router` 的 `modelAliases` 为每个场景定义别名，你可以在同一个会话中 `/model ds-short` 切换，**无需退出终端**。

### 长期维护注意两点

- **每隔两周检查一次环境变量**：系统更新、shell 配置迁移可能导致 `~/.zshrc` 被覆盖。用 `echo $DEEPSEEK_API_KEY | wc -c` 核对 Key 长度，并确认 `DEEPSEEK_BASE_URL` 仍然是 `https://api.deepseek.com/v1`。
- **关注模型版本更新**：DeepSeek V4 的 `deepseek-v4-pro` 标识符可能随新版本而变（例如添加日期后缀）。本教程中所有配置基于 **2025年5月的官方文档**，如果你的请求返回 `Model not found`，请先去 [platform.deepseek.com](https://platform.deepseek.com) 查看最新模型列表。

> 如果你在公司团队中推广此配置，建议将 `~/.claude-code-router/config.json` 和 `~/.zshrc` 的配置片段纳入团队知识库或配置管理仓库，**确保新成员能 5 分钟完成接入**。

**最终建议**：用 `/model` 切换替代多终端启动。在同一会话中对比 DeepSeek V4-Pro 和 Claude Sonnet 的输出，比退出重开要高效得多。配置完成后，下一步值得尝试的是**通过第三方代理（如阿里云百炼）降低延迟**——在 `providers` 中新增 `aliyun` 端点，使用 `/model ds-aliyun` 即可切换，无需修改任何其他配置。