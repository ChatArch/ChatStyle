# 快速开始

本文演示下游项目如何把 ChatStyle 接入一个新的 Click CLI，并在项目内封装新的交互接口。示例保持业务无关，适合作为 `chattool pypi init` 生成项目后的起点。

## 安装依赖

本地开发 ChatStyle 时：

```bash
pip install -e /home/rexwzh/workspace/core/ChatStyle
```

下游项目发布依赖时：

```toml
dependencies = [
  "click>=8.0",
  "chatstyle>=0.1.0",
]
```

## 添加一个新的 CLI 命令

推荐用 `CommandSchema` 描述可恢复输入，把 Click option 保持为非 required，再交给 `resolve_command_inputs()` 统一处理缺参补问、默认值、校验、`-i/-I` 和非 TTY 行为。

完整新增路径建议按这个顺序做：

1. 在 Click 层声明非 required 的 option / argument，只负责接收显式输入。
2. 用 `CommandField` 描述每个字段的 prompt 文案、类型、默认值、是否敏感、是否 required、校验函数。
3. 用 `CommandConstraint` 描述跨字段规则，例如“remote 模式必须提供 token”。
4. 给命令加 `@add_interactive_option`，统一接入 `--interactive/--no-interactive` 和 `-i/-I`。
5. 在 callback 里调用 `resolve_command_inputs()`，把 Click 收到的值、schema、interactive 和 usage 交给 ChatStyle。
6. 只在 resolver 返回完整 values 之后执行业务逻辑；网络请求、文件写入和领域判断不要放进 ChatStyle。

```python
# src/demoapp/cli.py
from __future__ import annotations

import click

from chatstyle import (
    CommandConstraint,
    CommandField,
    CommandSchema,
    add_interactive_option,
    render_success,
    resolve_command_inputs,
)


def _validate_name(value, _values):
    if len(value) < 2:
        return "name must contain at least 2 characters"
    return None


def _require_token_for_remote(values):
    if values.get("mode") == "remote" and not values.get("token"):
        return "token is required when mode is remote"
    return None


CREATE_SCHEMA = CommandSchema(
    name="create",
    fields=(
        CommandField("name", prompt="Project name", required=True, validator=_validate_name),
        CommandField("path", prompt="Output path", kind="path", default="./demo"),
        CommandField("mode", prompt="Mode", kind="select", choices=("local", "remote"), default="local"),
        CommandField("token", prompt="API token", sensitive=True, prompt_if_missing=False),
        CommandField("yes", prompt="Continue", kind="confirm", default=True),
    ),
    constraints=(CommandConstraint(_require_token_for_remote),),
)


@click.group()
def cli():
    pass


@cli.command()
@click.option("--name")
@click.option("--path")
@click.option("--mode")
@click.option("--token")
@click.option("--yes/--no", default=None)
@add_interactive_option
def create(name, path, mode, token, yes, interactive):
    values = resolve_command_inputs(
        schema=CREATE_SCHEMA,
        provided={"name": name, "path": path, "mode": mode, "token": token, "yes": yes},
        interactive=interactive,
        usage="Usage: demo create [--name TEXT] [--path PATH] [--mode local|remote] [-i|-I]",
    )
    render_success(f"Created {values['name']} at {values['path']}")
```

运行方式：

```bash
demo create --name alpha -I
demo create -i
demo create --mode remote --token "$TOKEN"
```

## 回退逻辑在哪里

ChatStyle 有多层 fallback，分别解决不同问题：

| 层级 | 位置 | 负责内容 |
| --- | --- | --- |
| 值来源 fallback | `chatstyle.input.resolve.resolve_command_inputs()` | 显式参数缺失时使用 `CommandField.default` / `default_factory`；缺失字段是否补问由 `required` / `prompt_if_missing` 决定。 |
| interactive 策略 fallback | `chatstyle.core.interactive.resolve_interactive_mode()` | `interactive=None` 是自动模式：只有 TTY 可用且存在可恢复缺参或初始校验错误时才 prompt；`-I` 禁用 prompt；`-i` 强制 prompt。 |
| 非 TTY fallback | `chatstyle.input.resolve.resolve_command_inputs()` + `chatstyle.core.errors` | 非 TTY 不阻塞；有默认值的字段可以继续使用默认值，无默认值的 required 字段快速报错并附 usage。 |
| TUI 依赖 fallback | `chatstyle.tui.prompt` | `questionary` / `prompt_toolkit` 不存在时，`ask_select()`、`ask_checkbox()` 等回退到 Click 文本输入。 |
| 输出 fallback | `chatstyle.render.output` | `rich` 不存在时，标题、状态、表格、建议命令等回退到 `click.echo()`。 |
| 业务封装 fallback | 下游项目自己的 `ui.py` / `config.py` | 环境变量、配置文件、已有 token 等业务优先级应在下游项目封装，再作为 `provided` 或 `default_factory` 传给 ChatStyle。 |

注意 `required=True` 不等于“没有默认值”。没有默认值且 required 的字段一定需要用户提供或 prompt；有默认值的 required 字段表示“显式输入缺失时，TTY 自动模式也应该进入 prompt，让用户确认或覆盖默认值”。在 `-I` 或非 TTY 场景下，默认值仍可作为自动化 fallback。

## 添加多选参数

`checkbox` 字段适合插件、模板、feature flags 等多选项：

```python
FEATURE_SCHEMA = CommandSchema(
    name="features",
    fields=(
        CommandField(
            "features",
            prompt="Select features",
            kind="checkbox",
            choices=("docs", "tests", "ci"),
            default=("tests",),
            prompt_if_missing=True,
        ),
    ),
)
```

## 封装新的交互接口

下游项目可以在自己的模块中组合 ChatStyle 原语，形成业务语义更明确的接口。封装层可以知道业务含义，但 ChatStyle 本身不应该知道。

```python
# src/demoapp/ui.py
from __future__ import annotations

from chatstyle import (
    create_choice,
    get_separator,
    mask_secret,
    prompt_sensitive_value,
    render_key_values,
    render_stage,
)
from chatstyle.tui import ask_select


def ask_environment(default="dev"):
    value = ask_select(
        "Environment",
        [
            create_choice("Development", "dev", checked=default == "dev"),
            create_choice("Production", "prod", checked=default == "prod"),
            get_separator(),
            create_choice("Cancel", "cancel"),
        ],
    )
    return value


def ask_api_token(current_token=None):
    return prompt_sensitive_value("API token", current_token)


def render_config_preview(config):
    render_stage("Config preview")
    safe_config = {**config, "token": mask_secret(config.get("token"))}
    render_key_values(safe_config)
```

## 推荐约定

- recoverable 参数不要在 Click 层设置 `required=True`。
- 自动化脚本使用 `-I`，人工修复和初始化使用 `-i`。
- sensitive 字段只进入 password prompt，输出必须先 `mask_secret()`。
- 默认值优先在 schema 的 `default` / `default_factory` 中表达；业务配置优先级在下游项目解析后再传入 ChatStyle。
- 需要强制用户确认默认值时，用 `required=True` 加默认值；只想缺失时静默使用默认值时，不要设 required。
- 下游项目可以封装 `ask_xxx()` / `render_xxx()`，但业务逻辑、网络请求和文件写入不放进 ChatStyle。
- 长流程使用 `chatstyle.render` 展示阶段、计划、dry-run 和建议命令。
