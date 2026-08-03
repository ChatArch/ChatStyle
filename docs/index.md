# ChatStyle 文档

ChatStyle 是 ChatArch 的可复用 CLI 交互规范与运行时。它为 Click CLI 统一输入 schema、缺参补问、`-i/-I`、TTY 判断、敏感值处理和流程输出；下游包应依赖这些公共原语，而不是复制第二套交互实现。

## 按场景选择

| 目标 | 入口 |
| --- | --- |
| 第一次把 ChatStyle 接入 Click 命令 | [快速开始](quickstart.md) |
| 选择输入、终端、输出或安全模块 | [模块板块](modules.md) |
| 对齐 `-i/-I`、自动补问和脚本行为 | [交互约定](conventions.md) |
| 理解高层 schema 与低层 interactive resolver 边界 | [交互运行时](interaction-runtime.md) |
| 修改公共 API、测试或发布流程 | [开发规范](development.md) |
| 阅读包的设计目标与取舍 | [设计草案](design.md) |

## 文档入口

<div class="grid cards" markdown>

- **快速接入**

    从安装、`CommandSchema`、Click option 到最小命令，建立一条可以直接复用的接入路径。

    [打开快速开始](quickstart.md)

- **交互规范**

    查看自动补问、显式 `-i/-I`、非 TTY、敏感输入和自动化环境的统一行为。

    [打开交互约定](conventions.md)

- **模块与边界**

    按 `input`、`tui`、`render`、`security`、`core` 和 `patterns` 选择稳定接口。

    [打开模块板块](modules.md)

- **维护与发布**

    了解 API 稳定性、依赖边界、测试矩阵、MkDocs 和 Trusted Publisher gate。

    [打开开发规范](development.md)

</div>

## 运行时边界

<div class="grid cards" markdown>

- **高层命令输入**

    `resolve_command_inputs()` 负责默认值、同构校验和可恢复缺参补问。自动模式统一遵守 `CHATARCH_AUTO_PROMPT=0/false/no/off`；显式 `-i` 仍优先。

- **低层 interactive resolver**

    `resolve_interactive_mode()` 保留显式 opt-in 的环境策略，使已有 adapter 可以控制确认流程，而不会被高层自动补问策略意外改变。

- **非交互自动化**

    CI、脚本和 Agent 调用应传 `-I`；缺少 required 值时快速失败，机器输出不能混入 prompt chatter。

- **敏感数据**

    密码、token 和 secret 只通过敏感 prompt/脱敏 helper 处理，文档、日志和异常不得回显原值。

</div>

## 最小 Schema

```python
from chatstyle import CommandField, CommandSchema

SCHEMA = CommandSchema(
    name="demo",
    fields=(
        CommandField("name", prompt="name", required=True),
        CommandField(
            "path",
            prompt="output path",
            kind="path",
            default="./out.txt",
        ),
    ),
)
```

本地构建文档：

```bash
pip install -e ".[docs]"
mkdocs build --strict
```
