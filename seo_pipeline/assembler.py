import re


class Assembler:
    def assemble(self, title: str, intro: str, sections: dict[str, str],
                 conclusion: str) -> str:
        """Assemble all parts into a complete Markdown article."""
        parts = [f"# {title}\n", intro]

        for heading, content in sections.items():
            parts.append(f"## {heading}\n{content}")

        parts.append(f"## 总结\n{conclusion}")

        article = "\n\n".join(parts)

        # Normalize excess blank lines (max 1 consecutive)
        article = re.sub(r"\n{3,}", "\n\n", article)

        return article
