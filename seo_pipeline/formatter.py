import re
from pathlib import Path
from datetime import date


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

    def _slugify(self, title: str) -> str:
        slug = title.lower().strip()
        # Remove special chars, keep Chinese/alphanumeric/spaces/hyphens
        slug = re.sub(r"[^\w\s一-鿿-]", "", slug)
        slug = re.sub(r"[-\s]+", "-", slug)
        slug = slug.strip("-")
        return slug[:80] if len(slug) > 80 else slug
