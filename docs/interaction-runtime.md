# 交互 Runtime

`chatstyle` 抽取 ChatArch CLI 中最通用的交互运行时能力，同时保持通用、轻量、可被 ChatTool 之外的 Click CLI 项目复用。

## Runtime 边界

ChatStyle 负责“如何收集、校验和展示通用 CLI 输入”，不负责“业务命令应该做什么”。

包含：

- Click 命令的 `-i/-I` 接入。
- TTY 可用性判断。
- 缺参补问策略。
- prompt、choice、confirm 和 checkbox 原语。
- 默认值、敏感值、字段校验和跨字段约束。
- 通用输出、flow 阶段展示和建议命令展示。

不包含：

- ChatTool 或其他项目的业务流程。
- 具体配置文件格式和写入逻辑。
- 远端 API 调用、安装逻辑或环境检测。
- 业务错误解析和业务恢复策略。

## 模块映射

- `chatstyle.schema`：声明 `CommandField`、`CommandSchema` 和 `CommandConstraint`。
- `chatstyle.resolve`：合并显式参数、默认值、interactive prompt 和校验。
- `chatstyle.click`：提供 `add_interactive_option()` 等 Click 接入 helper。
- `chatstyle.interactive`：TTY 检测、interactive 模式归一化和 prompt 决策。
- `chatstyle.errors`：面向 Click 的通用 abort 和错误 helper。
- `chatstyle.prompt`：text、path、confirm、select、checkbox prompt 原语。
- `chatstyle.choice`：choice、separator 和 questionary adapter。
- `chatstyle.mask`：敏感值脱敏、当前值提示和敏感输入。
- `chatstyle.output`：标题、提示、状态、建议命令、优先级链和 Rich/click fallback 展示。
- `chatstyle.flow`：流程阶段、结果和建议命令展示。
- `chatstyle.setup`：setup 场景兼容 wrapper。
- `chatstyle.constants`：共享 `-i/-I` 文案、`BACK_VALUE` 和 checkbox indicator。

更多职责说明见 [模块板块](modules.md)，行为规范见 [交互约定](conventions.md)，维护规则见 [开发规范](development.md)。

## CommandSchema 流程

推荐下游项目使用同一个入口完成输入收集：

1. 用 `CommandField` 声明字段。
2. 用 `CommandSchema` 组织字段和约束。
3. Click option 保持 `required=False`，让 recoverable 缺参进入 resolver。
4. 用 `@add_interactive_option` 接入 `-i/-I`。
5. 在 callback 中调用 `resolve_command_inputs()`。
6. resolver 返回完整 values 后，再进入业务逻辑。

```python
import click

from chatstyle import CommandField, CommandSchema, add_interactive_option, resolve_command_inputs

SCHEMA = CommandSchema(
    name="demo",
    fields=(
        CommandField("name", prompt="name", required=True),
        CommandField("output", prompt="output path", kind="path", default="./out.txt"),
    ),
)


@click.command()
@click.option("--name", required=False)
@click.option("--output", required=False)
@add_interactive_option
def demo(name, output, interactive):
    values = resolve_command_inputs(
        schema=SCHEMA,
        provided={"name": name, "output": output},
        interactive=interactive,
        usage="Usage: demo [--name TEXT] [--output PATH] [-i|-I]",
    )
    click.echo(values["output"])
```

## Interactive 三态

- `interactive=True`：强制交互，来自 `-i` 或 `--interactive`。
- `interactive=False`：禁止交互，来自 `-I` 或 `--no-interactive`。
- `interactive=None`：自动模式，只有缺少可恢复参数且 TTY 可用时才 prompt。

非 TTY 环境必须快速失败，不能阻塞等待输入。自动化脚本应优先传齐参数或使用 `-I` 禁用 prompt。

## 依赖策略

- `click` 是核心依赖。
- `questionary`、`prompt_toolkit`、`rich` 是可选依赖。
- 可选依赖必须延迟导入。
- 未安装可选依赖时，公共 API 必须仍可导入，核心流程必须有 Click fallback。

## 下游接入建议

- 将 ChatStyle 作为外部依赖，而不是复制源码。
- 保持业务逻辑在项目自己的 command/service 层。
- 只把通用字段收集、prompt、mask 和展示逻辑放到 ChatStyle 层。
- 兼容期 facade 可以委托到 `chatstyle`，但不应维护第二套实现。
