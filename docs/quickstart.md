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
- 下游项目可以封装 `ask_xxx()` / `render_xxx()`，但业务逻辑、网络请求和文件写入不放进 ChatStyle。
- 长流程使用 `chatstyle.render` 展示阶段、计划、dry-run 和建议命令。
