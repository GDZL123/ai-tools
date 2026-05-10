from .llm_client import LLMClient
from .prompt_manager import PromptManager
from .config import Config


class OutlineGenerator:
    def __init__(self, client: LLMClient, prompts: PromptManager, config: Config):
        self._client = client
        self._prompts = prompts
        self._config = config.generation

    def generate(self, keyword: str, title: str, category: str,
                 web_context: str = "") -> list[str]:
        user_prompt = self._prompts.render(
            "outline",
            keyword=keyword,
            title=title,
            category=category,
            target_chars=str(self._config.target_total_chars),
        )
        if web_context:
            user_prompt += f"\n\n--- 以下是最新网络搜索结果，请参考其中的事实和数据来校正大纲 ---\n{web_context}"

        response = self._client.chat(user_prompt)

        headings = []
        for line in response.strip().splitlines():
            cleaned = line.strip().lstrip("0123456789.、-•·# ").strip()
            if cleaned and len(cleaned) >= 3:
                headings.append(cleaned)

        if not headings:
            raise RuntimeError(f"大纲生成失败：API返回格式无法解析。原始响应:\n{response[:500]}")

        if len(headings) < 3:
            print(f"  [警告] 大纲仅 {len(headings)} 个标题，建议5-8个")

        return headings
