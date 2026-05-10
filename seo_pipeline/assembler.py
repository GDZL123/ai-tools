import re


class Assembler:
    def assemble(self, title: str, intro: str, sections: dict[str, str],
                 conclusion: str) -> str:
        """Assemble all parts into a complete Markdown article."""
        # Intro as styled blockquote — title is in frontmatter, no duplicate H1
        intro_block = "\n> ".join(intro.strip().splitlines())
        parts = [f"> {intro_block}\n\n"]

        for i, (heading, content) in enumerate(sections.items()):
            if i > 0:
                parts.append("\n---\n")
            parts.append(f"## {heading}\n{content}")

        parts.append("\n---\n")
        parts.append(f"## 总结\n{conclusion}")

        article = "\n\n".join(parts)

        # Normalize excess blank lines (max 2 consecutive)
        article = re.sub(r"\n{4,}", "\n\n\n", article)

        return article
