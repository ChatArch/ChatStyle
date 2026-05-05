<div align="center">
    <a href="https://pypi.python.org/pypi/chatstyle">
        <img src="https://img.shields.io/pypi/v/chatstyle.svg" alt="PyPI version" />
    </a>
    <a href="https://github.com/ChatArch/ChatStyle/actions/workflows/ci.yml">
        <img src="https://github.com/ChatArch/ChatStyle/actions/workflows/ci.yml/badge.svg" alt="Tests" />
    </a>
    <a href="https://chatarch.github.io/ChatStyle">
        <img src="https://img.shields.io/badge/docs-mkdocs-blue.svg" alt="Documentation" />
    </a>
</div>

<div align="center">

[English](README.en.md) | [简体中文](README.md)
</div>

# ChatStyle

ChatStyle 是从 ChatTool 实践中独立出来的 CLI 交互风格与运行时工具包。它提供 prompt、choice、output、flow、mask、interactive 策略和 CommandSchema runtime，让新的 CLI 项目可以复用统一的缺参补问、`-i/-I`、TTY 判断、默认值和校验流程。

当前版本仍是 `0.1.0`，用于本地开发和后续发版准备。

## 能力

- `chatstyle.prompt`：文本、路径、确认、单选、多选 prompt。
- `chatstyle.choice`：choice、separator 和 questionary fallback 适配。
- `chatstyle.output`：标题、提示、状态、建议命令、优先级链和 Rich/click fallback 展示。
- `chatstyle.mask`：敏感值脱敏和敏感输入。
- `chatstyle.flow`：流程阶段、结果、建议命令和配置优先级展示。
- `chatstyle.setup`：setup 场景兼容 wrapper，底层委托到通用 flow/output。
- `chatstyle.schema` / `chatstyle.resolve`：声明式命令输入 schema 与补问解析。
- `chatstyle.click`：Click 的 `-i/-I` option 接入。
- `chatstyle.interactive` / `chatstyle.errors`：TTY、interactive 策略和错误 helper。

## 板块

### Command Schema Runtime

`schema`、`resolve` 和 `click` 组成声明式命令输入层。它负责字段声明、默认值、缺参补问、字段校验、跨字段约束和 `-i/-I` 接入。

### Prompt And Choice

`prompt` 和 `choice` 提供文本输入、路径输入、确认、单选、多选、全选控制和 choice/separator 构造。`questionary`、`prompt_toolkit` 延迟导入，不安装时 fallback 到 Click。

### Output And Flow

`output` 负责通用标题、提示、状态、建议命令和优先级链展示，Rich 可用时使用 Rich，不可用时 fallback 到 Click。`flow` 负责多步骤 CLI 流程的阶段、成功、警告、失败展示。`setup` 只保留为 setup 场景 wrapper，不作为核心抽象。

### Mask And Interactive Policy

`mask` 负责敏感值脱敏和敏感输入。`interactive`、`errors`、`constants` 负责 TTY 判断、interactive 状态、共享文案和错误展示。

## 安装

本地开发：

```bash
pip install -e ".[dev]"
```

项目依赖：

```toml
dependencies = ["chatstyle"]
```

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

```bash
pip install -e ".[docs]"
mkdocs serve
```

文档使用 `mkdocs-static-i18n` 的 suffix 模式：

- 中文默认站点使用 `docs/*.md`。
- 英文站点使用 `docs/*.en.md`，构建后位于 `/en/`。
- Material 语言切换由 i18n plugin 生成。

更多内容：

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
