from .llm_client import LLMClient
from .prompt_manager import PromptManager
from .config import Config


class SectionGenerator:
    def __init__(self, client: LLMClient, prompts: PromptManager, config: Config):
        self._client = client
        self._prompts = prompts
        self._config = config.generation

    def generate_intro(self, keyword: str, title: str,
                       tone: str = "",
                       web_context: str = "") -> str:
        user_prompt = self._prompts.render(
            "intro", tone=tone,
            keyword=keyword,
            title=title,
        )
        if web_context:
            user_prompt += f"\n\n--- 以下是最新网络搜索结果，确保引言中的事实引用准确 ---\n{web_context}"
        return self._client.chat(user_prompt)

    def generate_section(self, section_heading: str, keyword: str, title: str,
                         previous_sections: dict[str, str],
                         section_index: int, total_sections: int,
                         tone: str = "",
                         web_context: str = "") -> str:
        previous_text = self._build_context(previous_sections, section_heading)

        user_prompt = self._prompts.render(
            "section", tone=tone,
            section_heading=section_heading,
            keyword=keyword,
            title=title,
            section_index=str(section_index),
            total_sections=str(total_sections),
            previous_sections_text=previous_text,
            min_chars=str(self._config.min_chars_per_section),
            max_chars=str(self._config.max_chars_per_section),
        )
        if web_context:
            user_prompt += f"\n\n--- 以下是最新网络搜索结果，请优先使用其中的真实数据、价格、版本号 ---\n{web_context}"
        return self._client.chat(user_prompt)

    def generate_conclusion(self, keyword: str, title: str,
                            full_body: str, tone: str = "") -> str:
        """Use the section template with a special heading for conclusion."""
        user_prompt = self._prompts.render(
            "section", tone=tone,
            section_heading="总结与建议",
            keyword=keyword,
            title=title,
            section_index="最后",
            total_sections="最后",
            previous_sections_text=full_body,
            min_chars="200",
            max_chars="600",
        )
        return self._client.chat(user_prompt)

    def _build_context(self, completed: dict[str, str],
                       current_heading: str) -> str:
        """Build previous-sections context text, summarizing if too long."""
        if not completed:
            return "（这是第一节正文，前面只有引言）"

        MAX_CHARS = 8000
        parts = []
        total = 0
        for heading, text in completed.items():
            chunk = f"## {heading}\n{text}"
            total += len(chunk)
            parts.append(chunk)

        full = "\n\n".join(parts)
        if total <= MAX_CHARS:
            return full

        # Truncation: keep last 2 sections in full, summarize the rest
        if len(parts) <= 2:
            return full[:MAX_CHARS] + "\n\n（上文已截断）"

        recent = parts[-2:]
        earlier_headings = list(completed.keys())[:-2]
        summary = "前面已覆盖的主题：" + "、".join(earlier_headings)
        return summary + "\n\n---\n\n" + "\n\n".join(recent)
