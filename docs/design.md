# CLI Style 设计草案

本文是一份讨论稿，用来解释 ChatStyle 想统一什么、不统一什么，以及为什么这些约定对 ChatArch 后续的 `chatxxx` 工具有价值。它不是最终 API 清单，而是用来避免 X-Y 问题的设计地图。

## 背景和意图

ChatArch 是一个用于沉淀各类工具的 GitHub 组织。后续会出现很多 `chatxxx` 形式的 CLI 项目，例如面向发布、文档、网络、证书、数据处理或开发流程的工具。

这些 CLI 项目通常由 `chattool pypi` / `chatpypi init` 初始化。ChatStyle 的角色是在模板初始化阶段成为默认依赖，让新工具天然继承同一套 CLI 行为规范，而不是在每个项目里复制交互代码。

这些工具的业务不同，但 CLI 交互问题高度重复：

- 参数缺失时是否补问。
- 什么情况下允许进入交互。
- 自动化环境如何禁止 prompt。
- token、password、API key 如何展示和输入。
- select、checkbox、confirm 如何表现。
- 默认值来自哪里，prompt 里显示什么。
- 错误信息如何让用户知道下一步怎么做。
- 新项目通过 `chatpypi init` 初始化时如何默认获得一致体验。

ChatStyle 的核心目标不是做一个复杂 TUI 框架，也不是抽象所有可能的 CLI 框架能力，而是给 ChatArch 系列 CLI 工具提供一组小而稳定的公共交互规范和 runtime helper。只要某个能力不能被多个 `chatxxx` 工具共同复用，就不应该进入 ChatStyle。

## 一句话定义

ChatStyle 是 ChatArch CLI 工具的交互规范和轻量 runtime。

它应该让下游项目可以说：

> 我只负责业务逻辑；CLI 缺参补问、交互开关、敏感值显示、多选和通用输出都按 ChatStyle 来。

## 设计目标

### 统一行为

同一组织下的 CLI 工具应该在常见场景里表现一致：

- `-i` 强制当前命令交互。
- `-I` 禁止交互，适合脚本和 CI。
- 缺少可恢复参数时，TTY 可用才自动补问。
- 非 TTY 不阻塞等待输入。
- secret 展示永远 mask。
- select/checkbox 的交互方式一致。

### 降低模板复杂度

`chatpypi init` 生成新项目时，不应该复制一大段 prompt 和 resolver 代码。模板只需要依赖：

```toml
dependencies = ["click>=8.0", "chatstyle"]
```

然后在命令里使用 ChatStyle 的公共 API。

### 保持基础库通用

ChatStyle 不应该知道 ChatTool、某个 API、某个配置文件路径或某个业务命令。它只提供可复用的 CLI 交互积木。

### 保持自动化友好

ChatArch 工具经常会被脚本、CI、GitHub Actions 或 cron 使用。交互体验不能牺牲自动化稳定性。

因此所有 prompt 能力都必须有非交互路径：传齐参数、使用默认值、或者快速失败。

## 非目标

ChatStyle 不做这些事情：

- 不做完整 TUI 应用框架。
- 不接管业务命令流程。
- 不读取或写入下游项目配置。
- 不执行安装、系统命令、`sudo` 或远端 API。
- 不定义 ChatTool 专属文案。
- 不保证每个项目的视觉品牌都完全一样。

ChatStyle 统一的是“CLI 行为和基础表现”，不是所有业务体验。判断一个能力是否应该进入 ChatStyle 的标准是：它是不是 ChatArch 系列 CLI 工具共同需要的规范，而不是某个工具的一次性便利函数。

## 概念模型

ChatStyle 可以拆成四层：

```text
User Intent
  ↓
Command Input Contract
  ↓
Interaction Runtime
  ↓
Presentation Primitives
  ↓
Business Logic
```

### User Intent

用户表达意图有三种方式：

- 显式参数：`--name demo --token xxx`
- 交互回答：缺参后 prompt 输入
- 默认值：命令、配置或环境提供的默认值

ChatStyle 只负责把这些输入合并成一组完整 values，不决定业务如何执行。

### Command Input Contract

命令输入契约描述“这个命令需要哪些字段”。当前对应 `CommandSchema`：

- `CommandField`：字段名、prompt 文案、类型、默认值、是否 required、是否 sensitive。
- `CommandConstraint`：跨字段约束。
- `CommandSchema`：一个命令的字段集合和约束集合。

它的作用是让缺参补问变成声明式，而不是每个命令手写一套 if/else。

### Interaction Runtime

Interaction runtime 处理“什么时候 prompt、如何失败、如何合并输入”：

- `interactive=True`：用户明确要求交互。
- `interactive=False`：用户明确禁止交互。
- `interactive=None`：自动模式。
- TTY 可用：可以补问。
- TTY 不可用：不能补问，必须快速失败或使用已有默认值。

### Presentation Primitives

Presentation primitives 是最底层的交互和展示积木：

- text/path input
- confirm
- select
- checkbox
- secret mask
- heading/note/status
- command suggestion
- priority chain

这些能力应保持业务中立。

### Business Logic

业务逻辑属于下游项目，例如：

- 创建 GitHub PR。
- 发布 PyPI 包。
- 生成证书。
- 修改 DNS。
- 写配置文件。
- 调用某个 API。

ChatStyle 不进入这一层。

## 缺参数约定

缺参数处理是 ChatStyle 的核心价值之一。

推荐规则：

1. 可恢复参数不要在 Click option 上设置 `required=True`。
2. 使用 `CommandField(required=True)` 声明业务上必需的字段。
3. callback 内调用 `resolve_command_inputs()`。
4. resolver 根据 interactive 策略决定补问或失败。

示例：

```python
import click

from chatstyle import CommandField, CommandSchema, add_interactive_option, resolve_command_inputs

SCHEMA = CommandSchema(
    name="publish",
    fields=(
        CommandField("package", prompt="package name", required=True),
        CommandField("repository", prompt="repository", default="pypi"),
        CommandField("token", prompt="api token", sensitive=True, required=True),
    ),
)


@click.command()
@click.option("--package", required=False)
@click.option("--repository", required=False)
@click.option("--token", required=False)
@add_interactive_option
def publish(package, repository, token, interactive):
    values = resolve_command_inputs(
        schema=SCHEMA,
        provided={"package": package, "repository": repository, "token": token},
        interactive=interactive,
        usage="Usage: publish --package TEXT [--repository TEXT] [--token TEXT] [-i|-I]",
    )
    run_publish(values)
```

行为预期：

- 参数齐全：直接执行。
- 参数缺失且 TTY 可用：自动补问可恢复字段。
- 参数缺失且 `-i`：强制补问；无 TTY 则失败。
- 参数缺失且 `-I`：不补问，直接失败。
- 参数缺失且非 TTY：不补问，直接失败。

## Interactive 开关

ChatStyle 统一三态 interactive：

| 状态 | 来源 | 含义 |
| --- | --- | --- |
| `True` | `-i` / `--interactive` | 强制进入当前命令交互流程 |
| `False` | `-I` / `--no-interactive` | 禁止 prompt，适合自动化 |
| `None` | 未指定 | 自动模式，只有 TTY 可用且缺少可恢复字段时 prompt |

这里有两个重要边界：

- `-i` 不是“进入全局向导”，只作用于当前命令。
- `-I` 是自动化契约，必须保证不会阻塞。

## Mask 和敏感值

敏感值包括：

- token
- password
- API key
- app secret
- webhook secret
- private key 片段

约定：

- 输入时隐藏。
- 展示时 mask。
- 日志、异常、summary 不输出原文。
- 如果空输入表示保留旧值，prompt 必须明确说明。

例子：

```text
current: ab****yz
Token (enter to keep):
```

## Choice 和多选

ChatStyle 提供统一的 choice 表达，不要求下游项目直接依赖 questionary 的细节。

原则：

- `questionary` 可用时提供更好的交互体验。
- 不可用时 fallback 到 Click。
- 选项的 label 给人看，value 给程序用。
- 空选项不能变成业务异常，应由调用方决定如何处理。
- checkbox 支持多选，但不应膨胀成复杂 TUI 状态机。

## 输出风格

ChatStyle 的输出层应该提供通用表现，而不是业务解释。

合理的通用能力：

- heading
- note
- success/warning/error/info status
- key-value summary
- suggested commands
- priority chain

需要谨慎的能力：

- setup 专属 helper
- 某个业务命令专属 summary
- 自动执行系统命令
- 带业务语义的错误恢复建议

### 关于 setup 的重新理解

“setup 阶段输出、建议命令、配置优先级展示”最初来自 setup 命令场景，但这些能力并不是 setup 独有。

更合理的抽象是：

- 流程阶段展示：任何长流程命令都需要。
- 建议命令展示：doctor、deploy、repair、setup 都可能需要。
- 配置优先级展示：所有读取配置的 CLI 都可能需要。

因此实现上应避免给 `setup` 单独开小灶。当前方向是把它们归入通用 output/flow 能力：

```python
render_stage("Check environment")
render_suggested_commands(["sudo systemctl restart demo"])
render_priority_chain(["CLI option", "ENV", "config file", "default"])
```

当前保留 `chatstyle.setup` 作为兼容和场景化 wrapper，而不是核心抽象。

## ChatStyle 和 chattool pypi

ChatStyle 的主要落点是配合 `chattool pypi` / `chatpypi init` 创建 ChatArch 系列 CLI 工具。模板阶段应该只生成最少代码：

- 添加 `chatstyle` 依赖。
- 使用 Click 作为命令框架。
- 使用 `CommandSchema` 描述输入。
- 使用 `add_interactive_option()` 提供 `-i/-I`。
- 使用 `resolve_command_inputs()` 完成缺参补问。
- 使用 `mask_secret()`、select/checkbox helper 处理常见交互。

模板不应该复制 ChatStyle 内部实现。

## API 分层建议

### 稳定公共 API

适合放在 `chatstyle.__init__`：

- `CommandField`
- `CommandSchema`
- `CommandConstraint`
- `resolve_command_inputs`
- `add_interactive_option`
- `ask_text`
- `ask_path`
- `ask_confirm`
- `ask_select`
- `ask_checkbox`
- `mask_secret`

### 候选公共 API

需要进一步讨论命名和边界：

- `render_heading`
- `render_note`
- `render_status`
- `render_suggested_commands`
- `render_priority_chain`
- `render_flow_start`
- `render_stage`
- `render_success`
- `render_warning`
- `render_failure`
- `render_commands`
- `create_choice`
- `get_separator`

### 不应公开或应谨慎公开

- 下划线 helper。
- 绑定某个业务场景的 helper。
- 需要可选依赖对象作为参数的 API。
- 会执行系统命令或写文件的 API。

## 模块边界草案

建议长期模块边界：

```text
chatstyle.schema       输入契约
chatstyle.resolve      输入解析和补问流程
chatstyle.click        Click 集成
chatstyle.interactive  TTY 和 interactive 策略
chatstyle.prompt       prompt 原语
chatstyle.choice       choice 表达和 adapter
chatstyle.mask         敏感值显示和输入
chatstyle.output       通用输出表现
chatstyle.flow         流程阶段、建议命令、优先级链等通用流程展示
chatstyle.errors       CLI 错误 helper
chatstyle.constants    共享常量
```

这里 `flow` 是核心流程展示模块；`setup` 只作为场景 wrapper 保留。

## 设计原则

### 小核心

宁愿 API 少一点，也不要把单个项目的便利函数做成基础库公共契约。

### 可降级

Rich、questionary、prompt_toolkit 都是体验增强，不是运行前提。

### 自动化优先

所有交互能力都必须能被显式参数或 `-I` 绕过。

### 声明式优先

缺参补问和默认值尽量由 schema 描述，不在每个 command callback 里复制 if/else。

### 业务外置

ChatStyle 不知道“发布、证书、DNS、PR、setup”具体意味着什么。

## 待讨论问题

1. `chatstyle.setup` 是否继续保留为长期 wrapper，还是在正式发版前移出顶层导出？
2. 输出层应该提供哪些稳定 API：只提供 heading/note，还是也提供 status/summary/table？
3. `CommandSchema` 是否应该支持更丰富的 choice value/label 对象，而不是 `Sequence[str]`？
4. `prompt_if_missing` 的命名是否准确？是否应该改成 `prompt_if_defaulted` 或 `confirm_default`？
5. 错误信息是否需要结构化错误码，方便自动化调用方识别？
6. `chatpypi init` 模板应该生成多复杂的示例：只展示 text/path/secret，还是也展示 select/checkbox？
7. 是否需要项目级 preset，例如 `standard_cli_schema()`，还是保持完全显式？
8. 文档中是否应该把 ChatStyle 定义为“规范优先，runtime 其次”？

## 当前建议

短期建议：

- 保留 `CommandSchema` 作为核心。
- 强化 prompt、mask、interactive 和 Click 集成测试。
- 将 setup 场景能力收敛到通用 flow/output API。
- 文档优先讲概念和约定，再讲 API。
- `chatpypi init` 只依赖 ChatStyle，不复制实现。

长期建议：

- ChatStyle 作为 ChatArch CLI 行为规范的单一来源。
- 下游项目只通过依赖升级获得交互规范更新。
- 新增 API 必须先回答：这个能力是否属于 ChatArch CLI 公共规范，且至少适用于两个以上 `chatxxx` 工具？
