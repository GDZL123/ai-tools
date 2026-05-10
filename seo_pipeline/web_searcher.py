"""Web search module — fetches current info for "追新" topics."""

from ddgs import DDGS


class WebSearcher:
    def __init__(self, max_results: int = 5):
        self._max_results = max_results

    def search(self, query: str) -> str:
        """Search the web and return formatted results as context text."""
        try:
            results = list(DDGS().text(query, max_results=self._max_results))
        except Exception:
            return ""

        if not results:
            return ""

        parts = []
        for i, r in enumerate(results, 1):
            title = r.get("title", "")
            body = r.get("body", "")
            href = r.get("href", "")
            parts.append(f"[{i}] {title}\n   {body}\n   来源: {href}")

        return "\n\n".join(parts)

    @staticmethod
    def build_context(query: str, max_results: int = 5) -> str:
        """Quick one-shot search returning pre-formatted context."""
        searcher = WebSearcher(max_results)
        return searcher.search(query)
