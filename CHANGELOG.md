# Changelog

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
