from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_DOCS = "https://arch.gh.wzhecnu.cn/ChatStyle/"


def test_docs_public_surfaces_share_the_canonical_url():
    mkdocs = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    preview = (ROOT / ".github" / "workflows" / "preview.yaml").read_text(
        encoding="utf-8"
    )
    readmes = "\n".join(
        (ROOT / name).read_text(encoding="utf-8")
        for name in ("README.md", "README.en.md")
    )

    assert f"site_url: {CANONICAL_DOCS}" in mkdocs
    assert f'Documentation = "{CANONICAL_DOCS}"' in pyproject
    assert CANONICAL_DOCS in readmes
    assert "https://arch.gh.wzhecnu.cn/${repo}/dev/" in preview
    assert "https://arch.gh.wzhecnu.cn/${repo.repo}/dev/" in preview
    assert "chatarch.github.io/ChatStyle" not in "\n".join(
        (mkdocs, preview, readmes)
    )


def test_mkdocs_has_bilingual_switch_and_mirrored_nav_pages():
    mkdocs = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")

    assert "fallback_to_default: true" in mkdocs
    assert "alternate:" in mkdocs
    assert "link: /ChatStyle/" in mkdocs
    assert "link: /ChatStyle/en/" in mkdocs
    assert "site_name: ChatStyle Documentation" in mkdocs

    for page in (
        "index",
        "design",
        "quickstart",
        "modules",
        "conventions",
        "development",
        "interaction-runtime",
    ):
        assert (ROOT / "docs" / f"{page}.md").is_file()
        assert (ROOT / "docs" / f"{page}.en.md").is_file()


def test_docs_home_uses_non_linear_navigation_cards():
    for name in ("index.md", "index.en.md"):
        source = (ROOT / "docs" / name).read_text(encoding="utf-8")
        assert '<div class="grid cards" markdown>' in source
        assert "CHATARCH_AUTO_PROMPT" in source
        assert "interaction-runtime.md" in source
