# ChatStyle Agent Guide

ChatStyle 是 ChatArch 体系下的基础 CLI 交互 runtime。任何修改都必须优先保证它能被 ChatTool 之外的 Click CLI 项目复用。

## 项目定位

- canonical package：`chatstyle`
- 代码目录：`src/chatstyle/`
- 文档目录：`docs/`，使用 mkdocs-material 构建
- 测试目录：`tests/`
- 当前版本：`0.1.1`，发布前保持 tag 与版本一致

## 核心原则

- 保持通用：不要引入 ChatTool、ChatArch 某个业务项目、第三方 API 的业务语义。
- 保持轻量：`click` 是核心依赖；`questionary`、`prompt_toolkit`、`rich` 必须保持可选并延迟导入。
- 保持稳定：顶层 `chatstyle.__init__` 只导出稳定公共 API；下划线 helper 不承诺长期兼容。
- 保持可测试：新增公开行为必须补测试；prompt fallback、CommandSchema、mask 和 Click 集成是重点。
- 保持文档同步：公开行为变化必须同步 README、mkdocs docs、date-based `CHANGELOG.md`。
- 保持单一来源：ChatStyle 是 canonical runtime；下游项目只能依赖或委托，不应复制第二套实现。

## 禁止事项

- 不要把 ChatTool 的业务命令、配置路径、远端 API 或产品文案写入 `src/chatstyle/`。
- 不要在 Click 层把 recoverable 参数设置为 `required=True` 后再尝试补问。
- 不要新增会破坏无可选依赖环境的 import-time 依赖。
- 不要在日志、异常、summary 或测试快照里输出原始 secret。
- 不要把 changelog 改成 release 分组；当前项目按日期记录。
- 不要 bump `0.1.0`，除非任务明确进入正式发版。

## 模块职责

- `schema`：声明 `CommandField`、`CommandSchema`、`CommandConstraint`。
- `resolve`：合并显式参数、默认值、interactive prompt 和校验。
- `click`：提供 `add_interactive_option()`，统一 `-i/-I`。
- `interactive`：TTY 检测、interactive 参数归一化、是否 prompt 的策略判断。
- `errors`：Click-facing 通用错误 helper。
- `constants`：共享文案、`BACK_VALUE`、checkbox indicator。
- `prompt`：text/path/confirm/select/checkbox prompt 原语。
- `choice`：choice、separator 和 questionary adapter。
- `output`：标题、提示和 Rich/click fallback 展示。
- `mask`：敏感值脱敏、当前值提示和敏感输入。
- `flow`：流程阶段、计划、dry-run、建议命令和配置优先级说明。

## 交互约定

- recoverable missing args 应通过 `CommandSchema` 进入统一补问流程。
- `-i` 表示强制进入当前命令的交互流程。
- `-I` 表示完全禁止交互；参数不足时必须快速失败。
- 非 TTY 环境不得阻塞等待输入；错误要可读且包含下一步提示或 usage。
- prompt 展示的默认值必须和实际执行默认值一致。
- sensitive 字段必须隐藏输入；展示当前值时必须 mask。
- 空 sensitive 输入表示保留旧值时，必须明确写在 prompt 文案里。
- `ask_select()` / `ask_checkbox()` 无可选项时应返回可处理的空结果或 `BACK_VALUE`，不得崩溃为业务异常。
- 用户取消应转成 Click 可处理的 abort 行为。

## 输出约定

- 通用标题、说明、状态和流程阶段提示优先使用 `chatstyle.render`。
- Rich 可用时可以增强展示；Rich 不可用时必须有纯 Click fallback。
- output helper 只负责表现，不解析业务错误。
- flow helper 只展示阶段、建议命令和配置优先级，不执行安装、不检测依赖、不写配置。

## 开发流程

1. 先确认新增能力是否属于通用 CLI runtime。
2. 修改 `src/chatstyle/`。
3. 补或更新 `tests/`。
4. 同步 README、`docs/` 和 `CHANGELOG.md`。
5. 运行验证：

```bash
python -m pytest -q
mkdocs build --strict
python -m build
```

## 文档维护

- `README.md`：中文默认入口，包含 badges、安装、模块概览和最小示例。
- `README.en.md`：英文入口。
- `docs/index.md`：中文文档首页。
- 默认文档使用中文；英文镜像文件使用 `.en.md` 后缀，并由 `mkdocs-static-i18n` 生成 `/en/`。
- `docs/modules.md`：板块和职责边界。
- `docs/conventions.md`：交互约定和行为规范。
- `docs/development.md`：开发和维护规范。
- `docs/interaction-runtime.md`：runtime 边界和下游接入说明。

## 下游接入约定

- ChatTool、ChatArch 其他项目和 `cli-style` 模板应把 `chatstyle` 作为外部依赖。
- 迁移期兼容入口可以保留，但实现应委托到 `chatstyle`。
- 下游项目只负责业务默认值来源、配置读写和业务执行。
- 通用 prompt、mask、flow 展示、`-i/-I` 和 CommandSchema 行为应回到 ChatStyle 维护。

## Workflow 规范

- CI 必须覆盖测试、包构建和 mkdocs build。
- docs deploy 使用 mkdocs GitHub Pages。
- PR preview 使用 mike 部署 dev 预览。
- 涉及 gh-pages 写入的 workflow 必须配置：
  - `git config user.name github-actions[bot]`
  - `git config user.email 41898282+github-actions[bot]@users.noreply.github.com`
