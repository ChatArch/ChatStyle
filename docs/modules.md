# 模块板块

ChatStyle 按“输入声明、交互策略、用户提示、输出展示、敏感值和 flow 展示”拆分。模块保持通用，不包含 ChatTool 业务逻辑。

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

- `render_heading()`：渲染通用标题。
- `render_note()`：渲染弱提示。
- `render_status()`：渲染业务中立的 info/success/warning/error/skip 状态。
- `render_info()` / `render_success()` / `render_warning()` / `render_error()`：常用状态快捷入口。
- `render_suggested_commands()`：打印建议用户手动执行的命令，但不执行。
- `render_priority_chain()`：展示配置或解析优先级链。
- `render_key_values()` / `render_summary()`：展示稳定对齐的键值摘要。
- `render_list()` / `render_table()`：展示通用列表和纯文本表格。
- `render_error_block()`：展示包含详情和 usage 的错误块。

实现原则：

- Rich 可用时使用 Rich 增强标题和提示。
- Rich 不可用时 fallback 到 Click。
- 输出 helper 只负责表现，不解析业务错误，不执行命令。

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

## Flow Display

相关模块：

- `chatstyle.flow`

用途：

- `render_flow_start()`：展示一个多步骤 CLI 流程开始。
- `render_stage()`：展示当前阶段。
- `render_progress_step()`：展示进行中的步骤。
- `render_success()` / `render_warning()` / `render_failure()` / `render_skip()`：展示通用结果。
- `render_plan()` / `render_dry_run()`：展示计划和预演步骤。
- `render_commands()`：展示建议用户手动执行的命令。
- `render_config_priority()` / `render_config_sources()`：展示配置优先级和来源摘要。

边界：

- `flow` 不执行安装、系统命令或远端调用。
- `flow` 不检测依赖、不写配置。
- setup 类需求通过通用 `flow` / `output` 组合实现，不单独作为核心模块。
