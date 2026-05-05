# 交互约定

本文定义 ChatStyle 作为 ChatArch 基础 CLI runtime 时必须保持的交互规范。

## Interactive 模式

ChatStyle 统一使用三态 interactive：

- `interactive is True`：强制交互，对应 `-i` 或 `--interactive`。
- `interactive is False`：禁止交互，对应 `-I` 或 `--no-interactive`。
- `interactive is None`：自动模式，缺少可恢复参数且 TTY 可用时进入交互。

约定：

- `-i` 只能进入当前命令的交互流程，不应跳到无关全局向导。
- `-I` 必须保证脚本和 CI 不会被 prompt 阻塞。
- 非 TTY 下不得自动 prompt。
- 强制交互但没有 TTY 时，必须使用统一 no-TTY 错误。

## 缺参补问

推荐使用 `CommandSchema` 描述可恢复参数：

```python
from chatstyle import CommandField, CommandSchema

SCHEMA = CommandSchema(
    name="demo",
    fields=(
        CommandField("name", prompt="name", required=True),
        CommandField("output", prompt="output path", kind="path", default="./out.txt"),
    ),
)
```

约定：

- recoverable 参数不要在 Click 层写成 `required=True`，否则 callback 前会被 Click 拦截。
- 默认值应来自 `default` 或 `default_factory`，并和 prompt 展示保持一致。
- `prompt_if_missing=True` 用于“即使有缓存默认值，也希望用户确认或刷新”的字段。
- 字段级校验放在 `validator`。
- 跨字段校验放在 `CommandConstraint`。

## Prompt 类型

字段类型和 prompt 映射：

- `text`：`ask_text()`
- `path`：`ask_path()`
- `select`：`ask_select()`
- `confirm`：`ask_confirm()`
- `checkbox`：`ask_checkbox()`
- `int`：先按文本/default 收集，再转 `int`
- `float`：先按文本/default 收集，再转 `float`

约定：

- prompt 文案应短、明确、无业务歧义。
- select/checkbox 的候选项应可读，并用 value 承载机器值。
- 无可选项时不得抛出业务异常；应返回空结果或 `BACK_VALUE`，由上层流程处理。
- 用户取消应转成 Click abort。

## 敏感值

敏感字段包括 token、password、API key、app secret、webhook secret 等。

约定：

- 输入时使用 `password=True` 或 `prompt_sensitive_value()`。
- 展示时必须使用 `mask_secret()`。
- 展示旧值时使用 `current: <masked>` 形式。
- 空输入表示保留旧值时，prompt 文案必须明确包含 `enter to keep` 或等价表达。
- 不要把原始 secret 写入日志、异常或普通 summary。

## 输出和流程

约定：

- 通用标题和说明使用 `chatstyle.output`。
- 流程阶段展示使用 `chatstyle.flow`。
- 长流程命令至少区分 start、stage、success、warning、failure。
- 涉及 sudo 或高风险命令时，默认只打印建议命令，不直接执行。
- 配置来源优先级应在 flow 输出或文档中清晰说明。

## 自动化兼容

所有交互能力都必须兼容脚本和 CI：

- 支持显式参数完整表达意图。
- 支持 `-I` 禁用 prompt。
- 非 TTY 下错误应快速返回。
- 错误信息应包含缺失项或 usage，方便自动化定位。
