import json
from pathlib import Path
from datetime import datetime

from .config import Config
from .llm_client import LLMClient
from .prompt_manager import PromptManager
from .csv_manager import CSVManager
from .title_generator import TitleGenerator
from .outline_generator import OutlineGenerator
from .section_generator import SectionGenerator
from .assembler import Assembler
from .formatter import Formatter
from .web_searcher import WebSearcher


class Pipeline:
    def __init__(self, config: Config):
        self._config = config
        # Initialize all modules
        prompts = PromptManager(config.paths.prompt_dir)
        system_prompt = prompts.render(
            "system",
            language=config.generation.language,
            min_chars=str(config.generation.min_chars_per_section),
            max_chars=str(config.generation.max_chars_per_section),
        )
        client = LLMClient(config, system_prompt)

        self._csv = CSVManager(config.paths.input_csv)
        self._titles = TitleGenerator(client, prompts, config)
        self._outlines = OutlineGenerator(client, prompts, config)
        self._sections = SectionGenerator(client, prompts, config)
        self._assembler = Assembler()
        self._formatter = Formatter(config.paths.output_dir)
        self._client = client
        self._state_dir = Path(config.paths.state_dir)

    def run(self, single_keyword: str | None = None):
        if single_keyword:
            keyword_data = {
                "keyword": single_keyword,
                "search_volume": "N/A",
                "difficulty": "N/A",
                "category": "手动测试",
                "status": "pending",
            }
            self._process_one(keyword_data)
        else:
            pending = self._csv.get_pending_keywords()
            if not pending:
                print("没有待处理的关键词。")
                return
            print(f"共 {len(pending)} 个待处理关键词\n")
            for i, kw in enumerate(pending, 1):
                print(f"[{i}/{len(pending)}] 处理: {kw['keyword']}")
                self._process_one(kw)
                print()

        print(f"\n完成！总计调用 API {self._client.total_calls} 次，"
              f"消耗 token {self._client.total_tokens}。")

    def process_batch(self):
        """Process all pending keywords (alias for run)."""
        self.run()

    def _process_one(self, kw: dict):
        keyword = kw["keyword"]
        state_file = self._state_dir / f"{self._slugify(keyword)}.json"

        # Check for checkpoint
        if state_file.exists():
            state = json.loads(state_file.read_text("utf-8"))
            title = state["title"]
            outline = state["outline"]
            completed = state.get("completed_sections", {})
            heading = state.get("remaining_headings", [])
            intro = completed.pop("__intro__", "")
            web_context = state.get("web_context", "")
            tone = state.get("tone", "tech")
            category = state.get("category", "通用")
            print(f"  [续传] 从断点恢复 ({state['status']})")
        else:
            self._csv.update_status(keyword, "in_progress")

            # Step 0: Determine tone & web search
            category = kw.get("category", "通用")
            tone = self._get_tone(category)
            needs_search = True  # 所有关键词都联网，提供最新数据
            web_context = ""
            if needs_search:
                print(f"  联网搜索...")
                web_context = WebSearcher.build_context(keyword, max_results=5)
                if web_context:
                    print(f"  搜索到 {len(web_context)} 字符")
                else:
                    print(f"  未获取到搜索结果，继续生成")

            # Step 1: Titles
            print(f"  生成标题...")
            titles = self._titles.generate(kw)
            title = titles[0]
            print(f"  选定: {title}")

            # Step 2: Outline
            print(f"  生成大纲...")
            outline = self._outlines.generate(keyword, title, category,
                                               web_context=web_context)
            print(f"  大纲 ({len(outline)} 节):")
            for h in outline:
                print(f"    - {h}")

            completed = {}
            # Save checkpoint before generating sections
            self._save_checkpoint(state_file, keyword, title, outline, completed,
                                  "section_0", outline.copy(), web_context)
            heading = list(outline)  # copy

        # Step 3: Generate sections
        total = len(outline)
        if "__intro__" not in [s.get("__intro__") for s in [{}]]:
            # Always generate intro if not already done
            if "intro" not in completed and "__intro__" not in completed:
                print(f"  生成引言...")
                intro = self._sections.generate_intro(keyword, title,
                                                       tone=tone,
                                                       web_context=web_context)
                completed["__intro__"] = intro
                self._save_checkpoint(state_file, keyword, title, outline, completed,
                                      "intro_done", [], web_context)

        # Determine remaining headings
        remaining = heading if heading else list(outline)
        for i, h in enumerate(remaining):
            if h in completed:
                continue
            idx = outline.index(h) + 1 if h in outline else i + 1
            print(f"  生成 [{idx}/{total}] {h}...")
            section = self._sections.generate_section(
                h, keyword, title, completed, idx, total,
                tone=tone, web_context=web_context
            )
            completed[h] = section

            # Update remaining for checkpoint
            still_remaining = [x for x in remaining if x not in completed]
            self._save_checkpoint(state_file, keyword, title, outline, completed,
                                  f"section_{len(completed)}", still_remaining, web_context)

        # Generate conclusion
        body_for_conclusion = self._build_body_for_conclusion(completed)
        print(f"  生成总结...")
        conclusion = self._sections.generate_conclusion(keyword, title, body_for_conclusion,
                                                         tone=tone)

        # Step 4 & 5: Assemble and save
        intro_text = completed.pop("__intro__", "")
        article = self._assembler.assemble(title, intro_text, completed, conclusion)
        output_path = self._formatter.format_and_save(
            article, kw, title, self._config.llm.model
        )
        print(f"  已保存: {output_path}")

        # Also save Hugo-compatible copy
        hugo_path = self._formatter.save_to_hugo(
            article, title, keyword, category,
            self._config.paths.hugo_content_dir
        )
        if hugo_path:
            print(f"  Hugo: {hugo_path}")

        # Cleanup
        self._csv.update_status(keyword, "done",
                                generated_title=title, output_file=output_path)
        if state_file.exists():
            state_file.unlink()

    def _save_checkpoint(self, path: Path, keyword: str, title: str,
                         outline: list, completed: dict[str, str],
                         status: str, remaining: list,
                         web_context: str = ""):
        state = {
            "keyword": keyword,
            "title": title,
            "outline": outline,
            "completed_sections": completed,
            "remaining_headings": remaining,
            "status": status,
            "web_context": web_context,
            "tone": tone if 'tone' in dir() else "tech",
            "category": category if 'category' in dir() else "通用",
            "timestamp": datetime.now().isoformat(),
        }
        path.write_text(json.dumps(state, ensure_ascii=False, indent=2), "utf-8")

    def _build_body_for_conclusion(self, completed: dict[str, str]) -> str:
        parts = []
        for heading, content in completed.items():
            if heading == "__intro__":
                continue
            parts.append(f"## {heading}\n{content}")
        return "\n\n".join(parts)

    @staticmethod
    def _get_tone(category: str) -> str:
        """Map category to prompt tone. '跨领域' categories use 'lifestyle'."""
        if "跨领域" in category:
            return "lifestyle"
        return "tech"

    @staticmethod
    def _slugify(text: str) -> str:
        import re
        slug = text.lower().strip()
        slug = re.sub(r"[^\w\s一-鿿-]", "", slug)
        slug = re.sub(r"[-\s]+", "-", slug)
        return slug.strip("-")[:60]

    def show_status(self):
        summary = self._csv.status_summary()
        print(f"关键词状态:")
        print(f"  总计: {summary['total']}")
        print(f"  待处理: {summary['pending']}")
        print(f"  进行中: {summary['in_progress']}")
        print(f"  已完成: {summary['done']}")
        print(f"  错误: {summary['error']}")
