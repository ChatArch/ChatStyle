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
