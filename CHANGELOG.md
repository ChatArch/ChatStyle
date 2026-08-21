# Changelog

## 2026-08-21

- 新增通用 Click 命令树 runtime：`render_click_tree()`、`tree_callback()` 和 `add_tree_option()`。
- `add_tree_option()` 标准接入 `--tree` 与 `--tree-brief`：默认 tree 保留参数签名，brief 省略参数签名，仅显示节点和说明。
- 将该能力导出到 `chatstyle.input` 和顶层 `chatstyle`，供 ChatArch 下游 Click CLI 复用。

## 2026-08-04

- `CHATARCH_AUTO_PROMPT=0/false/no/off` 现在由 ChatStyle 统一关闭自动补问；显式 `-i` 仍可强制当前命令交互。
- 导出 `AUTO_PROMPT_ENV_VAR` 与 `auto_prompt_enabled()`，并为 CommandSchema、TTY 与显式 interactive 覆盖补充回归测试。
- PyPI 发布 workflow 改用现有 Trusted Publisher/OIDC，不再读取长期 PyPI token secret。
- 将 MkDocs、README、Preview Docs、PyPI Documentation 和仓库 About 统一到 `https://arch.gh.wzhecnu.cn/ChatStyle/`，并补齐双语语言切换与首页导航。

## 2026-05-05

- 初始化 ChatStyle 独立 runtime 骨架，收纳 Click-oriented interactive policy、CommandSchema、shared resolver 和 prompt primitives。
- 新增 `chatstyle.input`、`chatstyle.tui`、`chatstyle.render`、`chatstyle.security`、`chatstyle.core`。
- 增强 `chatstyle.tui`，支持 text、path、confirm、select、checkbox 和 checkbox-with-controls。
- 增强 `chatstyle.security`，支持敏感值 mask、当前值提示和敏感输入保留旧值。
- 将 `CommandSchema` runtime 明确为核心能力，导出 `CommandField`、`CommandSchema`、`CommandConstraint`、`resolve_command_inputs()` 和 `add_interactive_option()`。
- 补充 README / README.en、mkdocs 文档、模块说明、开发规范、CI、docs deploy 和 PR preview workflow。
- 补充 ChatArch 基础库定位、项目级 `AGENTS.md` 开发规范、交互约定和下游接入规范。
- 将默认文档对齐为中文入口，并补齐 `.en.md` 英文镜像文档。
- 新增 `mkdocs-static-i18n` 文档依赖，支持中文默认站点和 `/en/` 英文站点切换。
- 新增通用 flow/output 渲染 API，避免为 setup 场景维护专门抽象。
- 增加 runtime、prompt fallback、flow display、Click integration 和 schema resolution 测试。
