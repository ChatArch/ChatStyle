# Development Guide

ChatStyle 是独立的 CLI 交互 runtime。实现必须保持通用、轻量、可测试，并能被 ChatTool 之外的 Click CLI 项目复用。

## 模块边界

- 通用交互能力放在 `src/chatstyle/`。
- 产品命令、业务语义和第三方 API 解析不得进入 ChatStyle。
- `CommandSchema` runtime 是核心能力，负责字段声明、补问、校验和 interactive 策略。
- `prompt` / `output` / `setup` / `mask` 只负责通用表现，不负责业务决策。

## 依赖策略

- `click` 是核心依赖。
- `questionary`、`prompt_toolkit`、`rich` 保持可选并延迟导入。
- 新增硬依赖前必须确认它是 runtime 契约必需，而不是某个项目的体验优化。

## API 设计

- 顶层 `chatstyle.__init__` 只导出稳定、面向用户的 API。
- 下划线 helper 可用于兼容层，但不承诺长期公开契约。
- 函数参数优先使用简单类型，避免引入业务对象。
- CLI 错误应保持可读、可操作。
- 新 API 应先确认是否能被多个 Click CLI 复用；只服务单个业务命令的能力不进入 ChatStyle。

## 交互规范

- `-i` 强制当前命令交互；`-I` 禁止 prompt 并服务脚本/CI。
- recoverable 缺参通过 `CommandSchema` 统一补问，不在 Click option 上设置 `required=True`。
- 非 TTY 环境不得阻塞等待输入。
- sensitive 字段输入必须隐藏，展示必须脱敏。
- prompt 文案保持短、明确、业务中立。

## 测试

- 新增公开 API 必须补测试。
- 重点覆盖 prompt fallback、mask、CommandSchema 解析和 Click 集成。
- 可选依赖相关测试应能在未安装可选依赖时稳定运行。

## 文档和变更记录

- README 负责最短说明和最小示例。
- 默认文档使用中文；英文镜像文件使用 `.en.md` 后缀。
- `docs/index.md` 是中文用户入口，`docs/index.en.md` 是英文入口。
- `docs/modules.md` 说明板块和职责边界。
- `docs/conventions.md` 说明交互约定。
- `docs/development.md` 说明维护规则。
- `docs/interaction-runtime.md` 说明 runtime 边界和下游接入方式。
- 公开行为变化必须同步 README、docs 和 `CHANGELOG.md`。
- `CHANGELOG.md` 按日期记录，不按 release 分组。

## Workflow

- CI 至少运行测试、构建包和 mkdocs build。
- docs deploy 使用 mkdocs GitHub Pages。
- PR preview 使用 mike 部署 dev 预览。
- 写入 gh-pages 的 workflow 必须配置 git identity：
  - `github-actions[bot]`
  - `41898282+github-actions[bot]@users.noreply.github.com`
