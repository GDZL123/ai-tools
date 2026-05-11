import re
from pathlib import Path
from datetime import date


# Map CSV categories to 3 main site sections
_CATEGORY_TO_SECTION: dict[str, str] = {
    "AI编程工具": "deploy",
    "AI本地部署": "deploy",
    "AI Agent": "deploy",
    "AI写作工具": "empower",
    "AI办公效率": "empower",
    "AI音视频": "empower",
    "Prompt工程": "empower",
    "AI绘图工具": "create",
}


def _map_category(cat: str) -> str:
    """Map a CSV category to one of: deploy, empower, create."""
    for key, section in _CATEGORY_TO_SECTION.items():
        if key in cat:
            return section
    return "empower"


class Formatter:
    def __init__(self, output_dir: str):
        self._output_dir = Path(output_dir)
        self._output_dir.mkdir(parents=True, exist_ok=True)

    def format_and_save(self, article_md: str, keyword_data: dict,
                        title: str, model: str = "deepseek-chat") -> str:
        slug = self._slugify(title)
        word_count = len(article_md.replace("\n", "").replace(" ", ""))

        frontmatter = (
            f"---\n"
            f'title: "{title}"\n'
            f'slug: "{slug}"\n'
            f'keyword: "{keyword_data["keyword"]}"\n'
            f'category: "{keyword_data.get("category", "通用")}"\n'
            f'date: "{date.today().isoformat()}"\n'
            f'search_volume: {keyword_data.get("search_volume", "N/A")}\n'
            f'difficulty: "{keyword_data.get("difficulty", "N/A")}"\n'
            f'word_count: {word_count}\n'
            f'generated_by: "{model}"\n'
            f"---\n\n"
        )

        full_content = frontmatter + article_md
        filepath = self._output_dir / f"{slug}.md"

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(full_content)

        return str(filepath.resolve())

    def save_to_hugo(self, article_md: str, title: str, keyword: str,
                     category: str, hugo_content_dir: str) -> str | None:
        """Save article in Hugo-compatible TOML format to Hugo content dir."""
        if not hugo_content_dir:
            return None

        posts_dir = Path(hugo_content_dir)
        posts_dir.mkdir(parents=True, exist_ok=True)

        # Generate a clean English filename
        slug = self._slugify(title)[:50]
        filename = f"{slug}.md"
        filepath = posts_dir / filename

        # Map CSV category to site section tag
        section_tag = _map_category(category)

        # Hugo TOML frontmatter — avoids Hugo v0.161 YAML edge cases
        today = date.today().isoformat()
        hugo_content = (
            f"+++\n"
            f"title = '{title}'\n"
            f"date = '{today}'\n"
            f"draft = false\n"
            f"tags = ['{section_tag}']\n"
            f"+++\n\n"
            f"{article_md}"
        )

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(hugo_content)

        return str(filepath.resolve())

    def _slugify(self, title: str) -> str:
        slug = title.lower().strip()
        # Remove special chars, keep Chinese/alphanumeric/spaces/hyphens
        slug = re.sub(r"[^\w\s一-鿿-]", "", slug)
        slug = re.sub(r"[-\s]+", "-", slug)
        slug = slug.strip("-")
        return slug[:80] if len(slug) > 80 else slug
