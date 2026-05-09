from .llm_client import LLMClient
from .prompt_manager import PromptManager
from .config import Config


class TitleGenerator:
    def __init__(self, client: LLMClient, prompts: PromptManager, config: Config):
        self._client = client
        self._prompts = prompts
        self._config = config.generation

    def generate(self, keyword_data: dict) -> list[str]:
        user_prompt = self._prompts.render(
            "title",
            count=str(self._config.title_count),
            keyword=keyword_data["keyword"],
            search_volume=str(keyword_data.get("search_volume", "N/A")),
            difficulty=str(keyword_data.get("difficulty", "N/A")),
            category=str(keyword_data.get("category", "通用")),
        )

        response = self._client.chat(user_prompt)

        titles = []
        for line in response.strip().splitlines():
            cleaned = line.strip().lstrip("0123456789.、-•· ").strip('"').strip("'").strip()
            if cleaned and len(cleaned) >= 4:
                titles.append(cleaned)

        if not titles:
            raise RuntimeError(f"标题生成失败：API 返回格式无法解析。原始响应:\n{response[:500]}")

        return titles[:self._config.title_count]
