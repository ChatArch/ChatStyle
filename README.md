<div align="center">
    <a href="https://pypi.python.org/pypi/chatstyle">
        <img src="https://img.shields.io/pypi/v/chatstyle.svg" alt="PyPI 版本" />
    </a>
    <a href="https://github.com/ChatArch/ChatStyle/actions/workflows/ci.yml">
        <img src="https://github.com/ChatArch/ChatStyle/actions/workflows/ci.yml/badge.svg" alt="测试" />
    </a>
    <a href="https://arch.gh.wzhecnu.cn/ChatStyle/">
        <img src="https://img.shields.io/badge/docs-mkdocs-blue.svg" alt="文档" />
    </a>
</div>

<div align="center">

[英文版](README.en.md) | [简体中文](README.md)
</div>

# ChatStyle

ChatStyle 是从 ChatTool 实践中独立出来的 CLI 交互风格与运行时工具包。它提供 prompt、choice、output、flow、mask、interactive 策略和 CommandSchema runtime，让新的 CLI 项目可以复用统一的缺参补问、`-i/-I`、TTY 判断、默认值和校验流程。

当前版本是 `0.1.1`。

## 能力

- `chatstyle.input`：命令输入声明、缺参补问解析和 Click `-i/-I` 接入。
- `chatstyle.tui`：文本、路径、确认、单选、多选 prompt，以及 choice/separator 适配。
- `chatstyle.render`：标题、提示、状态、建议命令、表格、列表、摘要和多步骤 flow 展示。
- `chatstyle.security`：敏感值脱敏、当前值提示和敏感输入。
- `chatstyle.core`：TTY、interactive 三态策略、共享常量和错误 helper。
- `chatstyle.patterns`：跨模块组合模式，例如多来源值解析、文本/敏感值补问。

## 代码结构

ChatStyle 按使用职能组织代码，避免把所有 runtime 文件平铺在顶层。顶层 `chatstyle` 仍提供常用 API 聚合入口；需要按职能导入时，使用下面的子包。

```text
src/chatstyle/
├── __init__.py          # 常用 public API 聚合入口，例如 CommandSchema、ask_text、render_success
├── input/               # CLI 输入声明、解析和 Click 集成
│   ├── schema.py        # CommandField / CommandSchema / CommandConstraint
│   ├── resolve.py       # resolve_command_inputs：缺参补问、默认值、校验、TTY 策略
│   └── click.py         # add_interactive_option：统一 -i/-I option
├── tui/                 # 终端交互输入原语
│   ├── prompt.py        # text/path/confirm/select/checkbox prompt
│   └── choice.py        # choice、separator、questionary adapter
├── render/              # 业务中立的输出和流程展示
│   ├── output.py        # heading、note、status、table、summary、suggested commands
│   └── flow.py          # stage、plan、dry-run、config priority/source
├── security/            # 敏感值处理
│   └── mask.py          # mask_secret、current secret hint、secret prompt
├── core/                # 底层策略和共享常量
│   ├── constants.py     # -i/-I 文案、BACK_VALUE、checkbox indicator
│   ├── interactive.py   # TTY 检测和 interactive 三态解析
│   └── errors.py        # Click 友好的错误 helper
└── patterns.py          # 跨模块组合模式：多来源值解析、文本/敏感值补问
```

推荐导入方式：

```python
from chatstyle import CommandField, CommandSchema, resolve_command_inputs
from chatstyle.input import add_interactive_option
from chatstyle.tui import ask_select
from chatstyle.render import render_success
from chatstyle.security import mask_secret
```

## 板块

### Command Schema Runtime

`schema`、`resolve` 和 `click` 组成声明式命令输入层。它负责字段声明、默认值、缺参补问、字段校验、跨字段约束和 `-i/-I` 接入。

### Prompt And Choice

`prompt` 和 `choice` 提供文本输入、路径输入、确认、单选、多选、全选控制和 choice/separator 构造。`questionary`、`prompt_toolkit` 延迟导入，不安装时 fallback 到 Click。

### Output And Flow

`output` 负责通用标题、提示、状态、建议命令、表格、列表、摘要和优先级链展示，Rich 可用时使用 Rich，不可用时 fallback 到 Click。`flow` 负责多步骤 CLI 流程的阶段、成功、警告、失败、计划和 dry-run 展示。setup 类需求通过通用 flow/output 组合实现，不单独作为核心模块。

### Mask And Interactive Policy

`mask` 负责敏感值脱敏和敏感输入。`interactive`、`errors`、`constants` 负责 TTY 判断、interactive 状态、共享文案和错误展示。CommandSchema 自动模式统一遵守 `CHATARCH_AUTO_PROMPT`；值为 `0`、`false`、`no` 或 `off` 时不自动补问，显式 `-i` 仍优先。

## 安装

本地开发：

```bash
pip install -e ".[dev]"
```

项目依赖：

```toml
dependencies = ["chatstyle"]
```

可选 TUI 增强依赖：

```toml
dependencies = ["chatstyle[tui]"]
```

核心包只强依赖 Click。`rich`、`questionary`、`prompt_toolkit` 用于增强展示和选择体验；未安装时会 fallback 到 Click 文本交互。

## 最小示例

```python
import click

from chatstyle import (
    CommandField,
    CommandSchema,
    add_interactive_option,
    resolve_command_inputs,
)


DEMO_SCHEMA = CommandSchema(
    name="demo",
    fields=(
        CommandField("name", prompt="name", required=True),
        CommandField("output", prompt="output path", kind="path", default="./out.txt"),
        CommandField("token", prompt="token", sensitive=True, prompt_if_missing=True),
    ),
)


@click.command()
@click.option("--name", required=False)
@click.option("--output", required=False)
@click.option("--token", required=False)
@add_interactive_option
def demo(name, output, token, interactive):
    values = resolve_command_inputs(
        schema=DEMO_SCHEMA,
        provided={"name": name, "output": output, "token": token},
        interactive=interactive,
        usage="Usage: demo [--name TEXT] [--output PATH] [--token TEXT] [-i|-I]",
    )
    click.echo(f"run demo for {values['name']} -> {values['output']}")
```

## 文档

正式文档：<https://arch.gh.wzhecnu.cn/ChatStyle/>

```bash
pip install -e ".[docs]"
mkdocs serve
```

文档使用 `mkdocs-static-i18n` 的 suffix 模式：

- 中文默认站点使用 `docs/*.md`。
- 英文站点使用 `docs/*.en.md`，构建后位于 `/en/`。
- Material 语言切换由 i18n plugin 生成。

更多内容：

- `docs/quickstart.md`：添加新 CLI 和封装新交互接口的快速开始。
- `docs/modules.md`：模块板块和职责边界。
- `docs/conventions.md`：交互约定和行为规范。
- `docs/development.md`：开发规范和维护规则。
- `docs/interaction-runtime.md`：runtime 边界与下游用法。

## 本地检查

```bash
python -m pytest -q
python -m build
mkdocs build --strict
```
