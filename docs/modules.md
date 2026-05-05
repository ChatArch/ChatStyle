# 模块板块

ChatStyle 按“输入声明、终端交互、输出展示、敏感值处理、底层策略、组合模式”拆分。模块保持通用，不包含 ChatTool 业务逻辑。

## `chatstyle.input`

负责 CLI 输入声明、解析和 Click 集成：

- `CommandField`：描述单个 CLI 字段，包括 `required`、`default`、`kind`、validator 等。
- `CommandSchema`：组织一个命令的输入契约。
- `CommandConstraint`：表达跨字段约束。
- `resolve_command_inputs()`：合并显式参数、默认值、interactive 补问和校验。
- `add_interactive_option()`：给 Click 命令统一接入 `--interactive/--no-interactive` 与 `-i/-I`。

语义约定：

- 没有默认值且命令运行必须需要的字段，应声明为 `required=True`。
- 有默认值的字段也可以声明为 `required=True`；这表示用户未显式提供时，TTY 自动模式会进入 prompt，并把默认值作为 prompt default。
- 非 TTY 或 `-I` 场景下，有默认值的字段可直接使用默认值；无默认值的 required 字段报错。

## `chatstyle.tui`

负责终端输入原语：

- `ask_text()`：文本输入。
- `ask_path()`：路径输入。
- `ask_confirm()`：确认输入。
- `ask_select()`：单选。
- `ask_checkbox()`：多选。
- `ask_checkbox_with_controls()`：带全选控制的多选。
- `create_choice()` / `get_separator()`：统一构造 choice 和分隔符。

`questionary` 和 `prompt_toolkit` 延迟导入；不可用时 fallback 到 Click。

## `chatstyle.render`

负责业务中立的输出和流程展示：

- `render_heading()` / `render_note()`：标题和弱提示。
- `render_status()` 以及 `render_info()` / `render_success()` / `render_warning()` / `render_error()`：状态输出。
- `render_suggested_commands()`：打印建议用户手动执行的命令，但不执行。
- `render_priority_chain()`：展示配置或解析优先级链。
- `render_key_values()` / `render_summary()`：展示稳定对齐的键值摘要。
- `render_list()` / `render_table()`：展示通用列表和纯文本表格。
- `render_flow_start()` / `render_stage()` / `render_plan()` / `render_dry_run()`：展示多步骤流程。
- `render_config_priority()` / `render_config_sources()`：展示配置优先级和来源摘要。

setup 类需求通过通用 `render` helper 组合实现，不单独作为核心模块。

## `chatstyle.security`

负责敏感值处理：

- `mask_secret()`：敏感值脱敏。
- `format_current_secret()`：生成 `current: ****` 风格提示。
- `prompt_sensitive_value()`：敏感输入，空输入保留旧值。

适用于 token、password、API key、app secret、webhook secret 等。

## `chatstyle.core`

负责底层策略、常量和错误：

- TTY 检测。
- interactive 三态解析。
- `-i/-I` help 文案。
- no-TTY 错误文案。
- `BACK_VALUE` 和 checkbox indicator。
- Click 友好的错误 helper。

## `chatstyle.patterns`

负责跨模块组合模式：

- `resolve_value()`：按优先级选择第一个可用值。
- `prompt_text_value()`：文本值缺失时补问，并支持 fallback。
- `prompt_sensitive_value_with_mask()`：敏感值缺失时补问，并展示自定义 mask。
