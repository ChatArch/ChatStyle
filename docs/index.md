# ChatStyle 文档

ChatStyle 是可复用的 CLI 交互风格和 runtime 包，适合需要统一 prompt、缺参补问、`-i/-I`、TTY 判断、敏感值脱敏和 setup 阶段展示的 Click CLI 项目。

## 核心模块

- `chatstyle.prompt`
- `chatstyle.choice`
- `chatstyle.output`
- `chatstyle.mask`
- `chatstyle.setup`
- `chatstyle.schema`
- `chatstyle.resolve`
- `chatstyle.click`
- `chatstyle.interactive`
- `chatstyle.errors`

## 文档导航

- [模块板块](modules.md)：每个模块负责什么、不负责什么。
- [交互约定](conventions.md)：`-i/-I`、缺参补问、prompt、敏感值和自动化兼容规范。
- [开发规范](development.md)：API、依赖、测试、文档和 workflow 维护规则。
- [Interaction Runtime](interaction-runtime.md)：runtime 边界和下游接入方式。
- 语言切换：通过页面语言菜单进入 English 站点。

## CommandSchema

`CommandSchema` 是 ChatStyle 的核心能力，用于声明 CLI 字段并统一完成默认值、缺参补问、校验和 interactive 策略。

```python
from chatstyle import CommandField, CommandSchema

SCHEMA = CommandSchema(
    name="demo",
    fields=(
        CommandField("name", prompt="name", required=True),
        CommandField("path", prompt="output path", kind="path", default="./out.txt"),
    ),
)
```

## 本地预览

```bash
pip install -e ".[docs]"
mkdocs serve
```
