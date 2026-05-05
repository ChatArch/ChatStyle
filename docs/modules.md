# 模块板块

ChatStyle 按“输入声明、交互策略、用户提示、输出展示、敏感值和 setup 展示”拆分。模块保持通用，不包含 ChatTool 业务逻辑。

## Command Schema Runtime

相关模块：

- `chatstyle.schema`
- `chatstyle.resolve`
- `chatstyle.click`

用途：

- 用 `CommandField` 描述 CLI 字段。
- 用 `CommandSchema` 组织命令输入。
- 用 `CommandConstraint` 表达跨字段约束。
- 用 `resolve_command_inputs()` 合并显式参数、默认值、interactive 补问和校验。
- 用 `add_interactive_option()` 给 Click 命令统一接入 `--interactive/--no-interactive` 与 `-i/-I`。

适用场景：

- 新 CLI 命令有可恢复缺参。
- 参数默认值需要和 prompt 展示保持一致。
- 命令需要统一支持 `-i` 强制交互和 `-I` 禁止交互。
- 需要字段级 validator 或跨字段 constraint。

## Interactive Policy

相关模块：

- `chatstyle.interactive`
- `chatstyle.errors`
- `chatstyle.constants`

用途：

- 判断 TTY 是否可用。
- 归一化 Click 默认 interactive 参数。
- 计算是否需要 prompt。
- 提供统一 `-i/-I` 文案和 no-TTY 错误文案。

边界：

- 策略只处理通用 CLI 行为。
- 不判断某个业务命令是否真的应该安装、写配置或访问远端服务。

## Prompt And Choice

相关模块：

- `chatstyle.prompt`
- `chatstyle.choice`

用途：

- `ask_text()`：文本输入。
- `ask_path()`：路径输入。
- `ask_confirm()`：确认输入。
- `ask_select()`：单选。
- `ask_checkbox()`：多选。
- `ask_checkbox_with_controls()`：带全选控制的多选。
- `create_choice()` 和 `get_separator()`：统一构造 choice 和分隔符。

实现原则：

- `questionary` 可用时使用更好的交互体验。
- `questionary` 不可用时 fallback 到 Click 文本输入。
- `prompt_toolkit` 相关能力延迟导入。
- 用户取消应转成 Click 可处理的中断行为。

## Output Style

相关模块：

- `chatstyle.output`

用途：

- 渲染标题。
- 渲染说明提示。
- 未来承载 status、summary、table、key-value 等通用展示 helper。

实现原则：

- Rich 可用时使用 Rich。
- Rich 不可用时 fallback 到 Click。
- 输出 helper 只负责表现，不解析业务错误。

## Mask And Sensitive Input

相关模块：

- `chatstyle.mask`

用途：

- `mask_secret()`：敏感值脱敏。
- `format_current_secret()`：生成 `current: ****` 风格提示。
- `prompt_sensitive_value()`：敏感输入，空输入保留旧值。

适用场景：

- token
- password
- API key
- app secret
- webhook secret

## Setup Display

相关模块：

- `chatstyle.setup`

用途：

- setup 开始、阶段、成功、警告和失败展示。
- 打印需要用户手动执行的建议命令。
- 展示配置来源优先级。

边界：

- 不执行安装。
- 不检测依赖。
- 不写配置。
- 只提供 setup 流程中的可复用展示方式。
